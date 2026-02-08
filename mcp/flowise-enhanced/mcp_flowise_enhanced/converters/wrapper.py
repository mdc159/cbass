"""Workflow wrapper to convert raw flows to ExportData format."""

import json
import uuid
from typing import Any

from .types import FlowType, detect_flow_type, is_raw_flow_file, is_tool_file


def create_empty_exportdata() -> dict[str, list]:
    """Create empty ExportData structure with all 15 arrays.

    Ported from wrap_flowise.ps1 New-EmptyExportData function.

    Returns:
        Dict with 15 empty arrays for Flowise import
    """
    return {
        "AgentFlow": [],
        "AgentFlowV2": [],
        "AssistantFlow": [],
        "AssistantCustom": [],
        "AssistantOpenAI": [],
        "AssistantAzure": [],
        "ChatFlow": [],
        "ChatMessage": [],
        "ChatMessageFeedback": [],
        "CustomTemplate": [],
        "DocumentStore": [],
        "DocumentStoreFileChunk": [],
        "Execution": [],
        "Tool": [],
        "Variable": [],
    }


def convert_flow_to_export_format(
    workflow: dict[str, Any],
    name: str,
    generate_id: bool = True,
) -> dict[str, Any]:
    """Convert raw workflow to wrapped format for ExportData.

    Ported from wrap_flowise.ps1 Convert-FlowToExportFormat function.

    Args:
        workflow: Raw workflow JSON with nodes/edges
        name: Workflow name
        generate_id: Whether to generate new UUID (default True)

    Returns:
        Wrapped flow dict with id, name, flowData, type
    """
    flow_type = detect_flow_type(workflow)

    # flowData is the stringified JSON of the workflow
    flow_data = json.dumps(workflow, indent=2)

    return {
        "id": str(uuid.uuid4()) if generate_id else workflow.get("id", str(uuid.uuid4())),
        "name": name,
        "flowData": flow_data,
        "type": flow_type.value,
    }


def convert_tool_to_export_format(tool: dict[str, Any]) -> dict[str, Any]:
    """Convert tool definition to ExportData format.

    Ported from wrap_flowise.ps1 Convert-ToolToExportFormat function.

    Args:
        tool: Tool JSON with name, schema, func, etc.

    Returns:
        Tool dict formatted for ExportData
    """
    return {
        "name": tool.get("name", ""),
        "description": tool.get("description", ""),
        "color": tool.get("color", ""),
        "iconSrc": tool.get("iconSrc", ""),
        "schema": tool.get("schema", ""),
        "func": tool.get("func", ""),
    }


def wrap_workflow(
    workflow: dict[str, Any],
    name: str | None = None,
    generate_id: bool = True,
) -> dict[str, Any]:
    """Wrap a workflow or tool into ExportData format.

    Main entry point that handles detection and conversion.

    Args:
        workflow: Raw workflow JSON or tool JSON
        name: Workflow/tool name (auto-detected from tool if not provided)
        generate_id: Whether to generate new UUID

    Returns:
        Dict with:
            - success: bool
            - detected_type: FlowType string
            - exportdata: Full 15-array ExportData structure
            - wrapped: The wrapped item (flow or tool)
            - error: Error message if success=False
    """
    exportdata = create_empty_exportdata()

    # Detect type and convert
    if is_tool_file(workflow):
        # Tool file
        tool_name = name or workflow.get("name", "Unnamed Tool")
        wrapped = convert_tool_to_export_format(workflow)
        wrapped["name"] = tool_name
        exportdata["Tool"].append(wrapped)

        return {
            "success": True,
            "detected_type": FlowType.TOOL.value,
            "exportdata": exportdata,
            "wrapped": wrapped,
        }

    elif is_raw_flow_file(workflow):
        # Raw flow file (CHATFLOW or AGENTFLOW)
        flow_name = name or "Unnamed Workflow"
        flow_type = detect_flow_type(workflow)
        wrapped = convert_flow_to_export_format(workflow, flow_name, generate_id)

        if flow_type == FlowType.AGENTFLOW:
            exportdata["AgentFlowV2"].append(wrapped)
        else:
            exportdata["ChatFlow"].append(wrapped)

        return {
            "success": True,
            "detected_type": flow_type.value,
            "exportdata": exportdata,
            "wrapped": wrapped,
        }

    elif "flowData" in workflow:
        # Already wrapped - just add to exportdata
        flow_type_str = workflow.get("type", "CHATFLOW")
        flow_name = name or workflow.get("name", "Unnamed Workflow")

        wrapped = {**workflow}
        if name:
            wrapped["name"] = flow_name
        if generate_id:
            wrapped["id"] = str(uuid.uuid4())

        if flow_type_str in ("AGENTFLOW", "MULTIAGENT"):
            exportdata["AgentFlowV2"].append(wrapped)
            detected = FlowType.AGENTFLOW
        else:
            exportdata["ChatFlow"].append(wrapped)
            detected = FlowType.CHATFLOW

        return {
            "success": True,
            "detected_type": detected.value,
            "exportdata": exportdata,
            "wrapped": wrapped,
        }

    else:
        return {
            "success": False,
            "detected_type": None,
            "exportdata": None,
            "wrapped": None,
            "error": "Unknown workflow format: expected nodes array, flowData field, or tool definition",
        }
