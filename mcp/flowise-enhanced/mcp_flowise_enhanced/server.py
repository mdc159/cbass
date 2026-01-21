"""MCP server for enhanced Flowise workflow operations.

Provides tools for:
- validate_workflow: Local + server-side validation
- wrap_workflow: Convert raw workflow to ExportData format
- create_chatflow: Create workflow via Flowise API
- import_workflow: Import ExportData via Flowise API
"""

import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .api.client import FlowiseClient
from .converters import wrap_workflow as do_wrap_workflow
from .validators import validate_workflow_local

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


def main():
    """Run the MCP server."""
    import asyncio

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
