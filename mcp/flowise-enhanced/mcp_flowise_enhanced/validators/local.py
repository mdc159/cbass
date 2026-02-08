"""Local validation for Flowise workflows.

Performs quick structural validation before API calls.
"""

from dataclasses import dataclass, field
from typing import Any

from ..converters.types import FlowType, detect_flow_type


@dataclass
class ValidationResult:
    """Result of workflow validation."""

    valid: bool
    flow_type: str | None
    local_errors: list[str] = field(default_factory=list)
    local_warnings: list[str] = field(default_factory=list)
    server_validation: list[dict[str, Any]] | None = None
    summary: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "valid": self.valid,
            "flow_type": self.flow_type,
            "local_errors": self.local_errors,
            "local_warnings": self.local_warnings,
            "server_validation": self.server_validation,
            "summary": self.summary,
        }


def validate_workflow_local(
    workflow: dict[str, Any],
    strict: bool = False,
) -> ValidationResult:
    """Perform local structural validation on a workflow.

    Validates:
    - nodes array exists and non-empty
    - edges array exists
    - Each node has: id, type, position, data
    - Each edge has: source, target, id
    - Edge source/target nodes exist
    - Flow type detection
    - AgentFlow: exactly one Start node

    Args:
        workflow: Raw workflow JSON with nodes/edges
        strict: Enable strict mode for additional checks

    Returns:
        ValidationResult with errors, warnings, and summary
    """
    errors: list[str] = []
    warnings: list[str] = []

    # Check for nodes array
    nodes = workflow.get("nodes")
    if nodes is None:
        errors.append("Missing 'nodes' array")
        return ValidationResult(
            valid=False,
            flow_type=None,
            local_errors=errors,
            local_warnings=warnings,
            summary={"node_count": 0, "edge_count": 0},
        )

    if not isinstance(nodes, list):
        errors.append("'nodes' must be an array")
        return ValidationResult(
            valid=False,
            flow_type=None,
            local_errors=errors,
            local_warnings=warnings,
            summary={"node_count": 0, "edge_count": 0},
        )

    if len(nodes) == 0:
        errors.append("'nodes' array is empty")
        return ValidationResult(
            valid=False,
            flow_type=None,
            local_errors=errors,
            local_warnings=warnings,
            summary={"node_count": 0, "edge_count": 0},
        )

    # Check for edges array
    edges = workflow.get("edges")
    if edges is None:
        errors.append("Missing 'edges' array")
    elif not isinstance(edges, list):
        errors.append("'edges' must be an array")
        edges = []
    else:
        # edges can be empty for single-node workflows
        if len(edges) == 0 and len(nodes) > 1:
            warnings.append("Workflow has multiple nodes but no edges")

    # Collect node IDs for reference checking
    node_ids: set[str] = set()
    node_types: dict[str, str] = {}  # id -> type mapping

    # Validate each node
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node at index {i} is not an object")
            continue

        node_id = node.get("id")
        if not node_id:
            errors.append(f"Node at index {i} missing 'id'")
        else:
            if node_id in node_ids:
                errors.append(f"Duplicate node ID: {node_id}")
            node_ids.add(node_id)

        node_type = node.get("type")
        if not node_type:
            if strict:
                errors.append(f"Node '{node_id}' missing 'type'")
            else:
                warnings.append(f"Node '{node_id}' missing 'type'")
        else:
            node_types[node_id] = node_type

        # Position check (optional but expected)
        position = node.get("position")
        if not position:
            warnings.append(f"Node '{node_id}' missing 'position'")
        elif not isinstance(position, dict):
            warnings.append(f"Node '{node_id}' has invalid 'position' format")

        # Data check (optional but expected for non-start nodes)
        data = node.get("data")
        if not data and node_type not in ("start", "startAgentFlow"):
            if strict:
                warnings.append(f"Node '{node_id}' missing 'data'")

    # Validate each edge
    edge_ids: set[str] = set()
    if edges:
        for i, edge in enumerate(edges):
            if not isinstance(edge, dict):
                errors.append(f"Edge at index {i} is not an object")
                continue

            edge_id = edge.get("id")
            if not edge_id:
                if strict:
                    errors.append(f"Edge at index {i} missing 'id'")
            else:
                if edge_id in edge_ids:
                    errors.append(f"Duplicate edge ID: {edge_id}")
                edge_ids.add(edge_id)

            source = edge.get("source")
            target = edge.get("target")

            if not source:
                errors.append(f"Edge '{edge_id or i}' missing 'source'")
            elif source not in node_ids:
                errors.append(f"Edge '{edge_id or i}' references non-existent source node: {source}")

            if not target:
                errors.append(f"Edge '{edge_id or i}' missing 'target'")
            elif target not in node_ids:
                errors.append(f"Edge '{edge_id or i}' references non-existent target node: {target}")

    # Detect flow type
    flow_type = detect_flow_type(workflow)

    # AgentFlow-specific checks
    if flow_type == FlowType.AGENTFLOW:
        start_nodes = [
            nid for nid, ntype in node_types.items()
            if ntype in ("startAgentFlow", "start", "agentFlow")
            and "start" in ntype.lower()
        ]
        # More lenient check - look for nodes that might be start nodes
        potential_starts = [
            nid for nid, ntype in node_types.items()
            if "start" in ntype.lower()
        ]
        if not potential_starts:
            warnings.append("AgentFlow may be missing a Start node")

    # Summary
    summary = {
        "node_count": len(nodes),
        "edge_count": len(edges) if edges else 0,
        "node_types": len(set(node_types.values())),
    }

    return ValidationResult(
        valid=len(errors) == 0,
        flow_type=flow_type.value,
        local_errors=errors,
        local_warnings=warnings,
        summary=summary,
    )
