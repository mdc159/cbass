"""Flowise API client for interacting with Flowise REST endpoints."""

import json
import os
from typing import Any

import requests


class FlowiseClient:
    """Client for Flowise REST API operations."""

    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
    ):
        """Initialize Flowise client.

        Args:
            endpoint: Flowise API endpoint URL (defaults to FLOWISE_API_ENDPOINT env)
            api_key: Flowise API key (defaults to FLOWISE_API_KEY env)
        """
        self.endpoint = (endpoint or os.environ.get("FLOWISE_API_ENDPOINT", "")).rstrip("/")
        self.api_key = api_key or os.environ.get("FLOWISE_API_KEY", "")

        if not self.endpoint:
            raise ValueError("FLOWISE_API_ENDPOINT must be set")

    def _headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        params: dict | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to Flowise API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path (will be joined with endpoint)
            data: Request body data
            params: Query parameters

        Returns:
            JSON response as dict

        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.endpoint}{path}"

        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            json=data,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        if response.content:
            return response.json()
        return {}

    # Chatflow operations

    def list_chatflows(self) -> list[dict[str, Any]]:
        """List all chatflows."""
        return self._request("GET", "/api/v1/chatflows")

    def get_chatflow(self, chatflow_id: str) -> dict[str, Any]:
        """Get chatflow by ID."""
        return self._request("GET", f"/api/v1/chatflows/{chatflow_id}")

    def create_chatflow(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new chatflow.

        Args:
            data: Chatflow data with name, flowData, type, etc.

        Returns:
            Created chatflow with ID
        """
        return self._request("POST", "/api/v1/chatflows", data=data)

    def update_chatflow(self, chatflow_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing chatflow.

        Args:
            chatflow_id: Chatflow ID to update
            data: Updated chatflow data

        Returns:
            Updated chatflow
        """
        return self._request("PUT", f"/api/v1/chatflows/{chatflow_id}", data=data)

    def delete_chatflow(self, chatflow_id: str) -> dict[str, Any]:
        """Delete a chatflow."""
        return self._request("DELETE", f"/api/v1/chatflows/{chatflow_id}")

    # Validation

    def validate_chatflow(self, chatflow_id: str) -> list[dict[str, Any]]:
        """Run server-side validation on a saved chatflow.

        Args:
            chatflow_id: ID of chatflow to validate

        Returns:
            List of validation results with node IDs and issues
        """
        return self._request("GET", f"/api/v1/validation/{chatflow_id}")

    # Import/Export

    def import_data(self, exportdata: dict[str, Any]) -> dict[str, Any]:
        """Import ExportData format (15-array structure).

        Args:
            exportdata: Full ExportData with ChatFlow, AgentFlowV2, Tool, etc.

        Returns:
            Import result summary
        """
        return self._request("POST", "/api/v1/export-import/import", data=exportdata)

    def export_data(self) -> dict[str, Any]:
        """Export all workspace data in ExportData format."""
        return self._request("POST", "/api/v1/export-import/export")

    # Tools

    def list_tools(self) -> list[dict[str, Any]]:
        """List all custom tools."""
        return self._request("GET", "/api/v1/tools")

    def get_tool(self, tool_id: str) -> dict[str, Any]:
        """Get tool by ID."""
        return self._request("GET", f"/api/v1/tools/{tool_id}")

    # Node schemas

    def list_nodes(self) -> list[dict[str, Any]]:
        """List all available node types with their schemas.

        Returns:
            List of node definitions with inputParams, inputAnchors, outputAnchors
        """
        return self._request("GET", "/api/v1/nodes")

    def get_node(self, name: str) -> dict[str, Any]:
        """Get schema for a specific node type.

        Args:
            name: Node name (e.g., 'chatOllama', 'toolAgent')

        Returns:
            Node definition with full schema
        """
        return self._request("GET", f"/api/v1/nodes/{name}")

    def get_nodes_by_category(self, category: str) -> list[dict[str, Any]]:
        """Get all nodes in a specific category.

        Args:
            category: Category name (e.g., 'Chat Models', 'Agents', 'Tools')

        Returns:
            List of nodes in that category
        """
        return self._request("GET", f"/api/v1/nodes/category/{category}")

    # Predictions

    def create_prediction(
        self,
        chatflow_id: str,
        question: str,
        overrides: dict[str, Any] | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Send a question to a chatflow and get a prediction.

        Args:
            chatflow_id: ID of the chatflow to query
            question: The question or prompt to send
            overrides: Optional config overrides (model, temperature, etc.)
            history: Optional conversation history

        Returns:
            Prediction response with text and optional sourceDocuments
        """
        data: dict[str, Any] = {"question": question}
        if overrides:
            data["overrideConfig"] = overrides
        if history:
            data["history"] = history

        return self._request("POST", f"/api/v1/prediction/{chatflow_id}", data=data)
