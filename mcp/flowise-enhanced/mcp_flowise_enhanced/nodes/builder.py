"""Node and edge builder utilities for Flowise workflows.

Creates properly structured node and edge instances that Flowise UI can render
with full configuration panels.
"""

import uuid
from typing import Any


def _generate_node_id(name: str, index: int = 0) -> str:
    """Generate a node ID in Flowise format.

    Args:
        name: Node name (e.g., 'chatOllama')
        index: Index for multiple nodes of same type

    Returns:
        Node ID like 'chatOllama_0'
    """
    return f"{name}_{index}"


def _build_input_param_id(node_id: str, param_name: str, param_type: str) -> str:
    """Build an input parameter ID.

    Args:
        node_id: Node ID (e.g., 'chatOllama_0')
        param_name: Parameter name (e.g., 'baseUrl')
        param_type: Parameter type (e.g., 'string')

    Returns:
        Input param ID like 'chatOllama_0-input-baseUrl-string'
    """
    return f"{node_id}-input-{param_name}-{param_type}"


def _build_input_anchor_id(node_id: str, anchor_name: str, anchor_type: str) -> str:
    """Build an input anchor ID.

    Args:
        node_id: Node ID
        anchor_name: Anchor name (e.g., 'model')
        anchor_type: Anchor type (e.g., 'BaseChatModel')

    Returns:
        Input anchor ID like 'chatOllama_0-input-model-BaseChatModel'
    """
    return f"{node_id}-input-{anchor_name}-{anchor_type}"


def _build_output_anchor_id(
    node_id: str, anchor_name: str, base_classes: list[str]
) -> str:
    """Build an output anchor ID.

    Args:
        node_id: Node ID
        anchor_name: Anchor name
        base_classes: List of base classes

    Returns:
        Output anchor ID like 'chatOllama_0-output-chatOllama-ChatOllama|BaseChatModel'
    """
    type_str = "|".join(base_classes) if base_classes else anchor_name
    return f"{node_id}-output-{anchor_name}-{type_str}"


# Primitive types that are inputParams (not anchors)
PRIMITIVE_TYPES = {
    "string",
    "number",
    "boolean",
    "password",
    "json",
    "code",
    "date",
    "file",
    "folder",
    "options",
    "multiOptions",
    "asyncOptions",
    "credential",
}


def _is_anchor_type(type_str: str) -> bool:
    """Check if a type string represents an anchor (not a primitive param).

    Args:
        type_str: The type string from the schema

    Returns:
        True if this is an anchor type, False if primitive param
    """
    return type_str.lower() not in PRIMITIVE_TYPES


def _split_inputs(schema: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    """Split the combined 'inputs' array into inputParams and inputAnchors.

    The Flowise API returns a single 'inputs' array, but the workflow JSON
    needs separate 'inputParams' (primitives) and 'inputAnchors' (connections).

    Args:
        schema: Node schema from API

    Returns:
        Tuple of (inputParams, inputAnchors)
    """
    # If schema already has separate arrays, use them
    if "inputParams" in schema or "inputAnchors" in schema:
        return schema.get("inputParams", []), schema.get("inputAnchors", [])

    # Split the combined inputs array
    inputs = schema.get("inputs", [])
    params = []
    anchors = []

    for item in inputs:
        item_type = item.get("type", "string")
        if _is_anchor_type(item_type):
            anchors.append(item)
        else:
            params.append(item)

    return params, anchors


def _estimate_node_height(
    input_params: list[dict], input_anchors: list[dict]
) -> int:
    """Estimate node height based on inputs.

    Args:
        input_params: List of input parameters
        input_anchors: List of input anchors

    Returns:
        Estimated height in pixels
    """
    # Base height
    height = 100

    # Add height for visible input params (non-additionalParams)
    visible_params = [
        p for p in input_params if not p.get("additionalParams", False)
    ]
    height += len(visible_params) * 55

    # Add height for input anchors
    height += len(input_anchors) * 50

    # Minimum height
    return max(height, 143)


def create_node_instance(
    schema: dict[str, Any],
    node_id: str | None = None,
    position: dict[str, float] | None = None,
    inputs: dict[str, Any] | None = None,
    index: int = 0,
) -> dict[str, Any]:
    """Create a complete node instance from a schema.

    Args:
        schema: Full node schema from Flowise API
        node_id: Custom node ID (auto-generated if not provided)
        position: Node position {"x": float, "y": float}
        inputs: Input values to set (merged with defaults)
        index: Index for auto-generated ID (e.g., chatOllama_0, chatOllama_1)

    Returns:
        Complete node structure ready for workflow JSON
    """
    name = schema.get("name", "unknown")
    node_id = node_id or _generate_node_id(name, index)
    position = position or {"x": 200 + (index * 350), "y": 100}

    # Determine node type based on category
    # AgentFlow nodes use "agentFlow", others use "customNode"
    category = schema.get("category", "")
    if category in ["Multi Agents", "Sequential Agents"]:
        node_type = "agentFlow"
    else:
        node_type = "customNode"

    # Split combined inputs array into params and anchors
    schema_params, schema_anchors = _split_inputs(schema)

    # Build inputParams with proper IDs
    input_params = []
    for param in schema_params:
        param_copy = dict(param)
        param_type = param.get("type", "string")
        param_copy["id"] = _build_input_param_id(
            node_id, param.get("name", ""), param_type
        )
        # Ensure display property exists for UI rendering
        if "display" not in param_copy:
            param_copy["display"] = not param_copy.get("additionalParams", False)
        input_params.append(param_copy)

    # Build inputAnchors with proper IDs
    input_anchors = []
    for anchor in schema_anchors:
        anchor_copy = dict(anchor)
        anchor_copy["id"] = _build_input_anchor_id(
            node_id, anchor.get("name", ""), anchor.get("type", "")
        )
        input_anchors.append(anchor_copy)

    # Build outputAnchors with proper IDs
    output_anchors = []
    base_classes = schema.get("baseClasses", [])
    for anchor in schema.get("outputAnchors", []):
        anchor_copy = dict(anchor)
        # Use anchor's own type or fall back to schema baseClasses
        anchor_base = anchor.get("type", "").replace(" ", "").split("|")
        if not anchor_base or anchor_base == [""]:
            anchor_base = base_classes
        anchor_copy["id"] = _build_output_anchor_id(
            node_id, anchor.get("name", name), anchor_base
        )
        # Set type string with pipes
        if base_classes:
            anchor_copy["type"] = " | ".join(base_classes)
        output_anchors.append(anchor_copy)

    # If no output anchors defined in schema, create a default one
    if not output_anchors and base_classes:
        output_anchors.append({
            "id": _build_output_anchor_id(node_id, name, base_classes),
            "name": name,
            "label": schema.get("label", name),
            "description": schema.get("description", ""),
            "type": " | ".join(base_classes),
        })

    # Build inputs dict with defaults
    node_inputs: dict[str, Any] = {}

    # Set defaults from inputParams
    for param in schema_params:
        param_name = param.get("name", "")
        default = param.get("default")
        if default is not None:
            node_inputs[param_name] = default
        else:
            node_inputs[param_name] = ""

    # Set empty strings for input anchors (will be filled by connections)
    for anchor in schema_anchors:
        anchor_name = anchor.get("name", "")
        node_inputs[anchor_name] = ""

    # Override with provided inputs
    if inputs:
        node_inputs.update(inputs)

    # Estimate dimensions
    height = _estimate_node_height(input_params, input_anchors)
    width = 300  # Standard Flowise node width

    # Build the node
    node = {
        "id": node_id,
        "position": position,
        "type": node_type,
        "data": {
            "id": node_id,
            "label": schema.get("label", name),
            "version": schema.get("version", 1),
            "name": name,
            "type": schema.get("type", schema.get("label", name)),
            "baseClasses": base_classes,
            "category": category,
            "description": schema.get("description", ""),
            "inputParams": input_params,
            "inputAnchors": input_anchors,
            "inputs": node_inputs,
            "outputAnchors": output_anchors,
            "outputs": {},
            "selected": False,
        },
        "width": width,
        "height": height,
        "selected": False,
        "positionAbsolute": position,
    }

    return node


def create_edge(
    source_node: dict[str, Any],
    target_node: dict[str, Any],
    target_input: str,
    source_output: str | None = None,
) -> dict[str, Any]:
    """Create an edge between two nodes.

    Args:
        source_node: Source node instance (from create_node_instance)
        target_node: Target node instance
        target_input: Name of input anchor on target (e.g., 'model', 'tools')
        source_output: Name of output anchor on source (auto-detected if not provided)

    Returns:
        Edge structure for workflow JSON

    Raises:
        ValueError: If anchors cannot be found or are incompatible
    """
    source_id = source_node.get("id", "")
    target_id = target_node.get("id", "")

    source_data = source_node.get("data", {})
    target_data = target_node.get("data", {})

    # Find source output anchor
    source_anchors = source_data.get("outputAnchors", [])
    if not source_anchors:
        raise ValueError(f"Source node '{source_id}' has no output anchors")

    # Use first output anchor if not specified
    if source_output:
        source_anchor = next(
            (a for a in source_anchors if a.get("name") == source_output), None
        )
        if not source_anchor:
            raise ValueError(
                f"Source output '{source_output}' not found on node '{source_id}'"
            )
    else:
        source_anchor = source_anchors[0]

    # Find target input anchor
    target_anchors = target_data.get("inputAnchors", [])
    target_anchor = next(
        (a for a in target_anchors if a.get("name") == target_input), None
    )
    if not target_anchor:
        raise ValueError(
            f"Target input '{target_input}' not found on node '{target_id}'"
        )

    # Get handle IDs
    source_handle = source_anchor.get("id", "")
    target_handle = target_anchor.get("id", "")

    if not source_handle or not target_handle:
        raise ValueError("Anchor IDs not properly set on nodes")

    # Build edge ID (Flowise format: source-sourceHandle-target-targetHandle)
    edge_id = f"{source_id}-{source_handle}-{target_id}-{target_handle}"

    edge = {
        "source": source_id,
        "sourceHandle": source_handle,
        "target": target_id,
        "targetHandle": target_handle,
        "type": "buttonedge",
        "id": edge_id,
    }

    return edge


def validate_connection(
    source_node: dict[str, Any],
    target_node: dict[str, Any],
    target_input: str,
    source_output: str | None = None,
) -> dict[str, Any]:
    """Validate that a connection is compatible.

    Args:
        source_node: Source node instance
        target_node: Target node instance
        target_input: Name of input anchor on target
        source_output: Name of output anchor on source (auto-detected if not provided)

    Returns:
        Validation result with 'valid', 'error', and compatibility info
    """
    result: dict[str, Any] = {"valid": False}

    source_data = source_node.get("data", {})
    target_data = target_node.get("data", {})

    # Find source output anchor
    source_anchors = source_data.get("outputAnchors", [])
    if not source_anchors:
        result["error"] = "Source node has no output anchors"
        return result

    if source_output:
        source_anchor = next(
            (a for a in source_anchors if a.get("name") == source_output), None
        )
        if not source_anchor:
            result["error"] = f"Source output '{source_output}' not found"
            return result
    else:
        source_anchor = source_anchors[0]

    # Find target input anchor
    target_anchors = target_data.get("inputAnchors", [])
    target_anchor = next(
        (a for a in target_anchors if a.get("name") == target_input), None
    )
    if not target_anchor:
        result["error"] = f"Target input '{target_input}' not found"
        return result

    # Get types
    source_type = source_anchor.get("type", "")
    target_type = target_anchor.get("type", "")

    # Parse types (can be "Type1 | Type2 | Type3")
    source_types = set(t.strip() for t in source_type.replace("|", " ").split())
    target_types = set(t.strip() for t in target_type.replace("|", " ").split())

    # Check compatibility: source must provide a type that target accepts
    # In Flowise, target type is usually a base class that source should extend
    compatible = bool(source_types & target_types)

    # Also check baseClasses from source node
    source_base = set(source_data.get("baseClasses", []))
    if source_base & target_types:
        compatible = True

    result["valid"] = compatible
    result["source_output"] = source_anchor.get("name")
    result["source_types"] = list(source_types | source_base)
    result["target_input"] = target_input
    result["target_types"] = list(target_types)
    result["compatible"] = compatible

    if not compatible:
        result["error"] = (
            f"Type mismatch: source provides {list(source_types | source_base)}, "
            f"target expects {list(target_types)}"
        )

    return result
