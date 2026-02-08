"""Node schema and builder utilities for Flowise workflows.

This module provides:
- NodeSchemaCache: Cached access to Flowise node schemas
- create_node_instance: Build properly structured nodes from schemas
- create_edge: Build edges between nodes with proper handle IDs
"""

from .builder import create_edge, create_node_instance
from .schema import NodeSchemaCache

__all__ = ["NodeSchemaCache", "create_node_instance", "create_edge"]
