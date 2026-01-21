"""Flow type detection for Flowise workflows."""

from enum import Enum
from typing import Any


class FlowType(str, Enum):
    """Flowise flow types."""

    CHATFLOW = "CHATFLOW"
    AGENTFLOW = "AGENTFLOW"
    MULTIAGENT = "MULTIAGENT"
    ASSISTANT = "ASSISTANT"
    TOOL = "TOOL"


def detect_flow_type(workflow: dict[str, Any]) -> FlowType:
    """Detect the flow type from workflow JSON.

    Ported from wrap_flowise.ps1 Get-FlowType function.

    Args:
        workflow: Raw workflow JSON with nodes array

    Returns:
        FlowType enum value
    """
    nodes = workflow.get("nodes", [])

    for node in nodes:
        node_type = node.get("type", "")
        # AgentFlow nodes have type="agentFlow" or type="iteration"
        if node_type in ("agentFlow", "iteration"):
            return FlowType.AGENTFLOW

    return FlowType.CHATFLOW


def is_raw_flow_file(data: dict[str, Any]) -> bool:
    """Check if JSON is a raw flow file (not wrapped, not a tool).

    Ported from wrap_flowise.ps1 Test-IsRawFlowFile function.

    Args:
        data: JSON data to check

    Returns:
        True if this is a raw flow file
    """
    # Already wrapped (has flowData field)
    if "flowData" in data:
        return False

    # Tool file (has func, schema)
    if "func" in data and "schema" in data:
        return False

    # Raw flow file (has nodes array)
    if "nodes" in data:
        return True

    return False


def is_tool_file(data: dict[str, Any]) -> bool:
    """Check if JSON is a Flowise custom tool definition.

    Ported from wrap_flowise.ps1 Test-IsToolFile function.

    Args:
        data: JSON data to check

    Returns:
        True if this is a tool file
    """
    return all(key in data for key in ("func", "schema", "name"))
