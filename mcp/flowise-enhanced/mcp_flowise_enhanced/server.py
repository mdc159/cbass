"""MCP server for Flowise workflow operations.

Provides tools for:
- validate_workflow: Local + server-side validation
- wrap_workflow: Convert raw workflow to ExportData format
- create_chatflow: Create workflow via Flowise API
- import_workflow: Import ExportData via Flowise API
- list_chatflows: List all chatflows
- get_chatflow: Get chatflow details
- create_prediction: Send questions to chatflows and get AI responses
"""

import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .api.client import FlowiseClient
from .converters import wrap_workflow as do_wrap_workflow
from .nodes import NodeSchemaCache, create_edge, create_node_instance
from .validators import validate_workflow_local

# Global schema cache (initialized on first use)
_schema_cache: NodeSchemaCache | None = None


def _get_schema_cache() -> NodeSchemaCache:
    """Get or initialize the global schema cache."""
    global _schema_cache
    if _schema_cache is None:
        _schema_cache = NodeSchemaCache()
    return _schema_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("flowise-enhanced")


def _json_result(data: dict[str, Any]) -> list[TextContent]:
    """Format result as JSON text content."""
    return [TextContent(type="text", text=json.dumps(data, indent=2))]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="validate_workflow",
            description=(
                "Validate a Flowise workflow. Performs local structural validation "
                "(nodes, edges, references) and optionally server-side validation if chatflow_id provided."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "object",
                        "description": "Raw workflow JSON with nodes and edges arrays",
                    },
                    "chatflow_id": {
                        "type": "string",
                        "description": "Optional: chatflow ID to run server-side validation (workflow must be saved first)",
                    },
                    "strict": {
                        "type": "boolean",
                        "description": "Enable strict mode for additional checks",
                        "default": False,
                    },
                },
                "required": ["workflow"],
            },
        ),
        Tool(
            name="wrap_workflow",
            description=(
                "Convert a raw Flowise workflow (nodes/edges) to ExportData format for import. "
                "Auto-detects CHATFLOW vs AGENTFLOW vs Tool. Equivalent to wrap_flowise.ps1."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "object",
                        "description": "Raw workflow JSON (nodes/edges) or tool definition (name/func/schema)",
                    },
                    "name": {
                        "type": "string",
                        "description": "Workflow name (required for raw flows)",
                    },
                    "generate_id": {
                        "type": "boolean",
                        "description": "Generate new UUID for workflow",
                        "default": True,
                    },
                },
                "required": ["workflow"],
            },
        ),
        Tool(
            name="create_chatflow",
            description=(
                "Create a new workflow in Flowise via API. Can accept raw workflow (nodes/edges) "
                "or pre-wrapped format. Optionally validates before creating."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "object",
                        "description": "Workflow data - raw (nodes/edges) or wrapped (flowData)",
                    },
                    "name": {
                        "type": "string",
                        "description": "Workflow name",
                    },
                    "deployed": {
                        "type": "boolean",
                        "description": "Deploy immediately after creation",
                        "default": False,
                    },
                    "validate_first": {
                        "type": "boolean",
                        "description": "Run local validation before creating",
                        "default": True,
                    },
                },
                "required": ["workflow", "name"],
            },
        ),
        Tool(
            name="import_workflow",
            description=(
                "Import workflows/tools via Flowise API using ExportData format. "
                "Use wrap_workflow first if you have raw workflow JSON."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "exportdata": {
                        "type": "object",
                        "description": "Full ExportData structure with 15 arrays (ChatFlow, AgentFlowV2, Tool, etc.)",
                    },
                },
                "required": ["exportdata"],
            },
        ),
        Tool(
            name="list_chatflows",
            description="List all chatflows in Flowise (enhanced version with more details).",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_chatflow",
            description="Get detailed information about a specific chatflow.",
            inputSchema={
                "type": "object",
                "properties": {
                    "chatflow_id": {
                        "type": "string",
                        "description": "The chatflow ID to retrieve",
                    },
                },
                "required": ["chatflow_id"],
            },
        ),
        Tool(
            name="create_prediction",
            description=(
                "Send a question to a Flowise chatflow and get an AI response. "
                "Use list_chatflows to find available chatflow IDs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question or prompt to send to the chatflow",
                    },
                    "chatflow_id": {
                        "type": "string",
                        "description": "The chatflow ID to query (use list_chatflows to find IDs)",
                    },
                    "history": {
                        "type": "array",
                        "description": "Optional conversation history as array of {role, content} objects",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"},
                            },
                        },
                    },
                },
                "required": ["question", "chatflow_id"],
            },
        ),
        Tool(
            name="list_node_types",
            description=(
                "Get catalog of available Flowise node types with basic metadata. "
                "Use to discover what nodes are available for building workflows."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category (e.g., 'Chat Models', 'Agents', 'Tools', 'Memory')",
                    },
                    "search": {
                        "type": "string",
                        "description": "Search nodes by name, label, or description",
                    },
                    "refresh": {
                        "type": "boolean",
                        "description": "Force refresh from API (default: use cache)",
                        "default": False,
                    },
                },
            },
        ),
        Tool(
            name="get_node_schema",
            description=(
                "Get complete schema for a specific Flowise node type. "
                "Returns inputParams, inputAnchors, outputAnchors needed for building nodes."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "Node name (e.g., 'chatOllama', 'toolAgent', 'bufferMemory')",
                    },
                    "summary": {
                        "type": "boolean",
                        "description": "Return simplified summary instead of full schema",
                        "default": False,
                    },
                },
                "required": ["node_name"],
            },
        ),
        Tool(
            name="create_node",
            description=(
                "Build a properly structured Flowise node instance from schema. "
                "Creates a complete node with all required fields for UI rendering."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "Node type name (e.g., 'chatOllama', 'toolAgent')",
                    },
                    "position": {
                        "type": "object",
                        "description": "Node position {x: number, y: number}",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                        },
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Input values to set (e.g., {modelName: 'qwen2.5:latest', temperature: 0.7})",
                    },
                    "node_id": {
                        "type": "string",
                        "description": "Custom node ID (auto-generated if not provided)",
                    },
                    "index": {
                        "type": "integer",
                        "description": "Index for auto-generated ID (e.g., 0 for chatOllama_0)",
                        "default": 0,
                    },
                },
                "required": ["node_name"],
            },
        ),
        Tool(
            name="create_edge",
            description=(
                "Build a properly structured edge connecting two Flowise nodes. "
                "Validates anchor compatibility and generates proper handle IDs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_node": {
                        "type": "object",
                        "description": "Source node instance (from create_node result)",
                    },
                    "target_node": {
                        "type": "object",
                        "description": "Target node instance (from create_node result)",
                    },
                    "target_input": {
                        "type": "string",
                        "description": "Name of input anchor on target (e.g., 'model', 'tools', 'memory')",
                    },
                    "source_output": {
                        "type": "string",
                        "description": "Name of output anchor on source (auto-detected if not provided)",
                    },
                    "validate_only": {
                        "type": "boolean",
                        "description": "Only validate connection, don't create edge",
                        "default": False,
                    },
                },
                "required": ["source_node", "target_node", "target_input"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "validate_workflow":
            return await handle_validate_workflow(arguments)
        elif name == "wrap_workflow":
            return await handle_wrap_workflow(arguments)
        elif name == "create_chatflow":
            return await handle_create_chatflow(arguments)
        elif name == "import_workflow":
            return await handle_import_workflow(arguments)
        elif name == "list_chatflows":
            return await handle_list_chatflows(arguments)
        elif name == "get_chatflow":
            return await handle_get_chatflow(arguments)
        elif name == "create_prediction":
            return await handle_create_prediction(arguments)
        elif name == "list_node_types":
            return await handle_list_node_types(arguments)
        elif name == "get_node_schema":
            return await handle_get_node_schema(arguments)
        elif name == "create_node":
            return await handle_create_node(arguments)
        elif name == "create_edge":
            return await handle_create_edge(arguments)
        else:
            return _json_result({"error": f"Unknown tool: {name}"})
    except Exception as e:
        logger.exception(f"Error handling tool {name}")
        return _json_result({"error": str(e), "tool": name})


async def handle_validate_workflow(args: dict[str, Any]) -> list[TextContent]:
    """Handle validate_workflow tool call."""
    workflow = args.get("workflow", {})
    chatflow_id = args.get("chatflow_id")
    strict = args.get("strict", False)

    # Run local validation
    result = validate_workflow_local(workflow, strict=strict)

    # Optionally run server validation
    if chatflow_id and result.valid:
        try:
            client = FlowiseClient()
            server_result = client.validate_chatflow(chatflow_id)
            result.server_validation = server_result
            # Check if server found issues
            if server_result:
                for item in server_result:
                    if item.get("issues"):
                        result.valid = False
                        break
        except Exception as e:
            result.server_validation = [{"error": str(e)}]

    return _json_result(result.to_dict())


async def handle_wrap_workflow(args: dict[str, Any]) -> list[TextContent]:
    """Handle wrap_workflow tool call."""
    workflow = args.get("workflow", {})
    name = args.get("name")
    generate_id = args.get("generate_id", True)

    result = do_wrap_workflow(workflow, name=name, generate_id=generate_id)
    return _json_result(result)


async def handle_create_chatflow(args: dict[str, Any]) -> list[TextContent]:
    """Handle create_chatflow tool call."""
    workflow = args.get("workflow", {})
    name = args.get("name", "Unnamed Workflow")
    deployed = args.get("deployed", False)
    validate_first = args.get("validate_first", True)

    result: dict[str, Any] = {"success": False}

    # Optionally validate first
    if validate_first:
        # Check if raw workflow or already wrapped
        if "nodes" in workflow and "flowData" not in workflow:
            validation = validate_workflow_local(workflow)
            result["validation_result"] = validation.to_dict()
            if not validation.valid:
                result["error"] = "Validation failed - see validation_result"
                return _json_result(result)

    # Wrap if needed
    if "nodes" in workflow and "flowData" not in workflow:
        wrap_result = do_wrap_workflow(workflow, name=name, generate_id=True)
        if not wrap_result.get("success"):
            result["error"] = wrap_result.get("error", "Failed to wrap workflow")
            return _json_result(result)
        chatflow_data = wrap_result["wrapped"]
    else:
        # Already wrapped or has flowData
        chatflow_data = workflow
        if name:
            chatflow_data["name"] = name

    # Add deployed flag
    chatflow_data["deployed"] = deployed

    # Create via API
    try:
        client = FlowiseClient()
        api_response = client.create_chatflow(chatflow_data)
        result["success"] = True
        result["chatflow_id"] = api_response.get("id")
        result["api_response"] = api_response
    except Exception as e:
        result["error"] = str(e)

    return _json_result(result)


async def handle_import_workflow(args: dict[str, Any]) -> list[TextContent]:
    """Handle import_workflow tool call."""
    exportdata = args.get("exportdata", {})

    result: dict[str, Any] = {"success": False}

    # Count items
    counts = {
        "chatflows": len(exportdata.get("ChatFlow", [])),
        "agentflows": len(exportdata.get("AgentFlowV2", [])),
        "tools": len(exportdata.get("Tool", [])),
    }

    if sum(counts.values()) == 0:
        result["error"] = "ExportData is empty - no items to import"
        return _json_result(result)

    try:
        client = FlowiseClient()
        api_response = client.import_data(exportdata)
        result["success"] = True
        result["imported"] = counts
        result["api_response"] = api_response
    except Exception as e:
        result["error"] = str(e)

    return _json_result(result)


async def handle_list_chatflows(args: dict[str, Any]) -> list[TextContent]:
    """Handle list_chatflows tool call."""
    try:
        client = FlowiseClient()
        chatflows = client.list_chatflows()

        # Format for readability
        summary = []
        for cf in chatflows:
            summary.append({
                "id": cf.get("id"),
                "name": cf.get("name"),
                "type": cf.get("type", "CHATFLOW"),
                "deployed": cf.get("deployed", False),
                "createdDate": cf.get("createdDate"),
            })

        return _json_result({
            "success": True,
            "count": len(chatflows),
            "chatflows": summary,
        })
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


async def handle_get_chatflow(args: dict[str, Any]) -> list[TextContent]:
    """Handle get_chatflow tool call."""
    chatflow_id = args.get("chatflow_id")

    if not chatflow_id:
        return _json_result({"success": False, "error": "chatflow_id is required"})

    try:
        client = FlowiseClient()
        chatflow = client.get_chatflow(chatflow_id)
        return _json_result({
            "success": True,
            "chatflow": chatflow,
        })
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


async def handle_create_prediction(args: dict[str, Any]) -> list[TextContent]:
    """Handle create_prediction tool call."""
    question = args.get("question")
    chatflow_id = args.get("chatflow_id")
    history = args.get("history")

    if not question:
        return _json_result({"success": False, "error": "question is required"})
    if not chatflow_id:
        return _json_result({"success": False, "error": "chatflow_id is required"})

    try:
        client = FlowiseClient()
        response = client.create_prediction(
            chatflow_id=chatflow_id,
            question=question,
            history=history,
        )

        # Extract the text response
        result: dict[str, Any] = {"success": True}

        if isinstance(response, dict):
            # Standard response format
            result["text"] = response.get("text", response.get("response", str(response)))
            if "sourceDocuments" in response:
                result["sourceDocuments"] = response["sourceDocuments"]
        else:
            # String response
            result["text"] = str(response)

        return _json_result(result)
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


async def handle_list_node_types(args: dict[str, Any]) -> list[TextContent]:
    """Handle list_node_types tool call."""
    category = args.get("category")
    search = args.get("search")
    refresh = args.get("refresh", False)

    try:
        cache = _get_schema_cache()

        # Get schemas based on filters
        if search:
            schemas = cache.search(search)
        elif category:
            schemas = cache.get_by_category(category)
        else:
            schemas = cache.get_all_schemas(force_refresh=refresh)

        # Format for readability - return summary info
        nodes = []
        for schema in schemas:
            nodes.append({
                "name": schema.get("name"),
                "label": schema.get("label"),
                "category": schema.get("category"),
                "description": schema.get("description", "")[:100],
                "version": schema.get("version"),
                "baseClasses": schema.get("baseClasses", []),
            })

        # Get available categories for reference
        categories = cache.get_categories()

        return _json_result({
            "success": True,
            "count": len(nodes),
            "nodes": nodes,
            "available_categories": categories,
        })
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


async def handle_get_node_schema(args: dict[str, Any]) -> list[TextContent]:
    """Handle get_node_schema tool call."""
    node_name = args.get("node_name")
    summary = args.get("summary", False)

    if not node_name:
        return _json_result({"success": False, "error": "node_name is required"})

    try:
        cache = _get_schema_cache()
        schema = cache.get_schema(node_name)

        if not schema:
            return _json_result({
                "success": False,
                "error": f"Node '{node_name}' not found",
                "hint": "Use list_node_types to see available nodes",
            })

        if summary:
            return _json_result({
                "success": True,
                "schema": cache.get_summary(schema),
            })

        return _json_result({
            "success": True,
            "schema": schema,
        })
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


async def handle_create_node(args: dict[str, Any]) -> list[TextContent]:
    """Handle create_node tool call."""
    node_name = args.get("node_name")
    position = args.get("position")
    inputs = args.get("inputs")
    node_id = args.get("node_id")
    index = args.get("index", 0)

    if not node_name:
        return _json_result({"success": False, "error": "node_name is required"})

    try:
        cache = _get_schema_cache()
        schema = cache.get_schema(node_name)

        if not schema:
            return _json_result({
                "success": False,
                "error": f"Node '{node_name}' not found",
                "hint": "Use list_node_types to see available nodes",
            })

        node = create_node_instance(
            schema=schema,
            node_id=node_id,
            position=position,
            inputs=inputs,
            index=index,
        )

        return _json_result({
            "success": True,
            "node": node,
            "node_id": node.get("id"),
            "usage_hint": "Pass this node to create_edge to connect it to other nodes",
        })
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


async def handle_create_edge(args: dict[str, Any]) -> list[TextContent]:
    """Handle create_edge tool call."""
    source_node = args.get("source_node")
    target_node = args.get("target_node")
    target_input = args.get("target_input")
    source_output = args.get("source_output")
    validate_only = args.get("validate_only", False)

    if not source_node:
        return _json_result({"success": False, "error": "source_node is required"})
    if not target_node:
        return _json_result({"success": False, "error": "target_node is required"})
    if not target_input:
        return _json_result({"success": False, "error": "target_input is required"})

    try:
        # Import validate_connection from builder
        from .nodes.builder import validate_connection

        # Always validate first
        validation = validate_connection(
            source_node=source_node,
            target_node=target_node,
            target_input=target_input,
            source_output=source_output,
        )

        if validate_only:
            return _json_result({
                "success": True,
                "validation": validation,
            })

        if not validation.get("valid"):
            return _json_result({
                "success": False,
                "error": validation.get("error", "Connection not valid"),
                "validation": validation,
            })

        edge = create_edge(
            source_node=source_node,
            target_node=target_node,
            target_input=target_input,
            source_output=source_output,
        )

        return _json_result({
            "success": True,
            "edge": edge,
            "validation": validation,
        })
    except ValueError as e:
        return _json_result({"success": False, "error": str(e)})
    except Exception as e:
        return _json_result({"success": False, "error": str(e)})


def main():
    """Run the MCP server."""
    import asyncio

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
