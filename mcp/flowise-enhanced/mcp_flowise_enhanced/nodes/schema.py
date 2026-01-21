"""Node schema caching for Flowise node types.

Provides cached access to Flowise node schemas to avoid repeated API calls
and enable efficient node discovery and search.
"""

from typing import Any

from ..api.client import FlowiseClient


class NodeSchemaCache:
    """Caches node schemas to avoid repeated API calls.

    Attributes:
        client: FlowiseClient instance for API requests
    """

    def __init__(self, client: FlowiseClient | None = None):
        """Initialize the schema cache.

        Args:
            client: Optional FlowiseClient instance. If not provided,
                   a new client will be created using environment variables.
        """
        self.client = client or FlowiseClient()
        self._cache: dict[str, dict[str, Any]] = {}
        self._all_schemas: list[dict[str, Any]] = []
        self._categories: list[str] = []
        self._loaded = False

    def _ensure_loaded(self, force_refresh: bool = False) -> None:
        """Ensure schemas are loaded from API.

        Args:
            force_refresh: Force reload even if already cached
        """
        if self._loaded and not force_refresh:
            return

        self._all_schemas = self.client.list_nodes()

        # Build cache indexed by node name
        self._cache = {}
        categories_set: set[str] = set()

        for schema in self._all_schemas:
            name = schema.get("name", "")
            if name:
                self._cache[name] = schema
            # Collect categories
            category = schema.get("category", "")
            if category:
                categories_set.add(category)

        self._categories = sorted(categories_set)
        self._loaded = True

    def get_all_schemas(self, force_refresh: bool = False) -> list[dict[str, Any]]:
        """Get all node schemas.

        Args:
            force_refresh: Force reload from API

        Returns:
            List of all node schemas with full details
        """
        self._ensure_loaded(force_refresh)
        return self._all_schemas

    def get_schema(self, node_name: str) -> dict[str, Any] | None:
        """Get schema for a specific node type.

        Args:
            node_name: Node name (e.g., 'chatOllama', 'toolAgent')

        Returns:
            Full node schema or None if not found
        """
        self._ensure_loaded()

        # First check cache
        if node_name in self._cache:
            return self._cache[node_name]

        # If not in bulk cache, try fetching directly (might be new node)
        try:
            schema = self.client.get_node(node_name)
            if schema:
                self._cache[node_name] = schema
                return schema
        except Exception:
            pass

        return None

    def get_categories(self) -> list[str]:
        """Get list of available node categories.

        Returns:
            Sorted list of category names
        """
        self._ensure_loaded()
        return self._categories

    def get_by_category(self, category: str) -> list[dict[str, Any]]:
        """Get all nodes in a specific category.

        Args:
            category: Category name (e.g., 'Chat Models', 'Agents')

        Returns:
            List of nodes in that category
        """
        self._ensure_loaded()
        return [s for s in self._all_schemas if s.get("category") == category]

    def search(self, query: str) -> list[dict[str, Any]]:
        """Search nodes by name, label, or description.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching node schemas
        """
        self._ensure_loaded()
        query_lower = query.lower()

        results = []
        for schema in self._all_schemas:
            name = schema.get("name", "").lower()
            label = schema.get("label", "").lower()
            description = schema.get("description", "").lower()

            if (
                query_lower in name
                or query_lower in label
                or query_lower in description
            ):
                results.append(schema)

        return results

    def get_summary(
        self,
        schema: dict[str, Any] | None = None,
        node_name: str | None = None,
    ) -> dict[str, Any]:
        """Get a summary of a node schema for display.

        Args:
            schema: Node schema dict, or
            node_name: Node name to look up

        Returns:
            Simplified schema summary with key fields
        """
        if schema is None and node_name:
            schema = self.get_schema(node_name)

        if not schema:
            return {"error": "Node not found"}

        # Split combined inputs array if needed (API format vs workflow format)
        input_params, input_anchors = self._split_inputs(schema)

        return {
            "name": schema.get("name"),
            "label": schema.get("label"),
            "category": schema.get("category"),
            "description": schema.get("description"),
            "baseClasses": schema.get("baseClasses", []),
            "version": schema.get("version"),
            "inputParams": [
                {
                    "name": p.get("name"),
                    "label": p.get("label"),
                    "type": p.get("type"),
                    "optional": p.get("optional", False),
                    "default": p.get("default"),
                }
                for p in input_params
            ],
            "inputAnchors": [
                {
                    "name": a.get("name"),
                    "label": a.get("label"),
                    "type": a.get("type"),
                    "optional": a.get("optional", False),
                    "list": a.get("list", False),
                }
                for a in input_anchors
            ],
            "outputAnchors": [
                {
                    "name": a.get("name"),
                    "label": a.get("label"),
                    "type": a.get("type"),
                }
                for a in schema.get("outputAnchors", [])
            ],
        }

    @staticmethod
    def _split_inputs(schema: dict[str, Any]) -> tuple[list[dict], list[dict]]:
        """Split combined 'inputs' array into params and anchors.

        The Flowise API returns a single 'inputs' array, but we need
        separate inputParams (primitives) and inputAnchors (connections).
        """
        # Primitive types that are inputParams (not anchors)
        primitive_types = {
            "string", "number", "boolean", "password", "json", "code",
            "date", "file", "folder", "options", "multiOptions",
            "asyncOptions", "credential",
        }

        # If schema already has separate arrays, use them
        if "inputParams" in schema and schema.get("inputParams"):
            return schema.get("inputParams", []), schema.get("inputAnchors", [])

        # Split the combined inputs array
        inputs = schema.get("inputs", [])
        params = []
        anchors = []

        for item in inputs:
            item_type = item.get("type", "string")
            if item_type.lower() in primitive_types:
                params.append(item)
            else:
                anchors.append(item)

        return params, anchors
