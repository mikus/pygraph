"""Graph representation implementations.

This module provides concrete implementations of the GraphRepresentation protocol,
including adjacency list and adjacency matrix representations. These classes
handle the low-level storage and manipulation of graph data.
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import Any, Protocol

from pygraph.edge import Edge


class GraphRepresentation[V: Hashable](Protocol):
    """Protocol defining the interface for graph representations."""

    def add_vertex(self, vertex: V) -> bool:
        """Add a vertex. Returns True if added, False if already exists."""

    def remove_vertex(self, vertex: V) -> bool:
        """Remove a vertex and its edges. Returns True if removed."""

    def add_edge(self, source: V, target: V, weight: float = 1.0, metadata: dict[str, Any] | None = None) -> bool:
        """Add an edge. Returns True if added, False if already exists."""

    def remove_edge(self, source: V, target: V) -> bool:
        """Remove an edge. Returns True if removed."""

    def has_vertex(self, vertex: V) -> bool:
        """Check if vertex exists."""

    def has_edge(self, source: V, target: V) -> bool:
        """Check if edge exists."""

    def get_vertices(self) -> set[V]:
        """Get all vertices."""

    def get_edges(self) -> list[Edge[V]]:
        """Get all edges."""

    def get_neighbors(self, vertex: V) -> set[V]:
        """Get adjacent vertices."""

    def get_edge_data(self, source: V, target: V) -> Edge[V] | None:
        """Get edge data if edge exists."""


class AdjacencyList[V: Hashable]:
    """Adjacency list representation using dictionaries.

    This representation is optimal for sparse graphs (few edges relative to vertices).
    It provides O(1) vertex and edge addition, and O(1) neighbor lookup.

    Time Complexity:
    - Add vertex: O(1)
    - Add edge: O(1)
    - Remove vertex: O(degree)
    - Check edge: O(1)
    - Get neighbors: O(1)

    Space Complexity: O(V + E)
    """

    def __init__(self, directed: bool = False):
        """Initialize adjacency list representation.

        Args:
            directed: Whether the graph is directed
        """
        self._directed = directed
        self._adj: dict[V, dict[V, Edge[V]]] = {}

    def add_vertex(self, vertex: V) -> bool:
        """Add a vertex. Returns True if added, False if already exists."""
        if vertex in self._adj:
            return False
        self._adj[vertex] = {}
        return True

    def remove_vertex(self, vertex: V) -> bool:
        """Remove a vertex and its edges. Returns True if removed."""
        if vertex not in self._adj:
            return False

        # Remove all edges to this vertex
        for neighbors in self._adj.values():
            neighbors.pop(vertex, None)

        # Remove the vertex itself
        del self._adj[vertex]
        return True

    def add_edge(self, source: V, target: V, weight: float = 1.0, metadata: dict[str, Any] | None = None) -> bool:
        """Add an edge. Returns True if added, False if already exists."""
        if source not in self._adj or target not in self._adj:
            return False

        if target in self._adj[source]:
            return False  # Edge already exists

        if metadata is None:
            metadata = {}

        edge = Edge(source, target, weight, metadata)
        self._adj[source][target] = edge

        # For undirected graphs, add the reverse edge
        if not self._directed:
            reverse_edge = Edge(target, source, weight, metadata)  # pylint: disable=arguments-out-of-order
            self._adj[target][source] = reverse_edge

        return True

    def remove_edge(self, source: V, target: V) -> bool:
        """Remove an edge. Returns True if removed."""
        if source not in self._adj or target not in self._adj[source]:
            return False

        del self._adj[source][target]

        # For undirected graphs, remove the reverse edge
        if not self._directed and source in self._adj[target]:
            del self._adj[target][source]

        return True

    def has_vertex(self, vertex: V) -> bool:
        """Check if vertex exists."""
        return vertex in self._adj

    def has_edge(self, source: V, target: V) -> bool:
        """Check if edge exists."""
        return source in self._adj and target in self._adj[source]

    def get_vertices(self) -> set[V]:
        """Get all vertices."""
        return set(self._adj.keys())

    def get_edges(self) -> list[Edge[V]]:
        """Get all edges."""
        edges = []
        for neighbors in self._adj.values():
            for edge in neighbors.values():
                edges.append(edge)
        return edges

    def get_neighbors(self, vertex: V) -> set[V]:
        """Get adjacent vertices."""
        if vertex not in self._adj:
            return set()
        return set(self._adj[vertex].keys())

    def get_edge_data(self, source: V, target: V) -> Edge[V] | None:
        """Get edge data if edge exists."""
        if source in self._adj and target in self._adj[source]:
            return self._adj[source][target]
        return None


class AdjacencyMatrix[V: Hashable]:
    """Adjacency matrix representation using 2D array.

    This representation is optimal for dense graphs (many edges) or when
    frequent edge existence checks are needed.

    Time Complexity:
    - Add vertex: O(V²) (matrix resize)
    - Add edge: O(1)
    - Remove vertex: O(V²)
    - Check edge: O(1)
    - Get neighbors: O(V)

    Space Complexity: O(V²)
    """

    def __init__(self, directed: bool = False):
        """Initialize adjacency matrix representation.

        Args:
            directed: Whether the graph is directed
        """
        self._directed = directed
        self._vertex_to_index: dict[V, int] = {}
        self._index_to_vertex: dict[int, V] = {}
        self._matrix: list[list[Edge[V] | None]] = []

    def add_vertex(self, vertex: V) -> bool:
        """Add a vertex. Returns True if added, False if already exists."""
        if vertex in self._vertex_to_index:
            return False

        index = len(self._vertex_to_index)
        self._vertex_to_index[vertex] = index
        self._index_to_vertex[index] = vertex

        # Resize matrix
        for row in self._matrix:
            row.append(None)
        self._matrix.append([None] * (index + 1))

        return True

    def remove_vertex(self, vertex: V) -> bool:
        """Remove a vertex and its edges. Returns True if removed."""
        if vertex not in self._vertex_to_index:
            return False

        index = self._vertex_to_index[vertex]

        # Remove row and column from matrix
        del self._matrix[index]
        for row in self._matrix:
            del row[index]

        # Update vertex mappings
        del self._vertex_to_index[vertex]
        del self._index_to_vertex[index]

        # Shift indices for vertices after the removed one
        for v, i in list(self._vertex_to_index.items()):
            if i > index:
                self._vertex_to_index[v] = i - 1
                self._index_to_vertex[i - 1] = v
                del self._index_to_vertex[i]

        return True

    def add_edge(self, source: V, target: V, weight: float = 1.0, metadata: dict[str, Any] | None = None) -> bool:
        """Add an edge. Returns True if added, False if already exists."""
        if source not in self._vertex_to_index or target not in self._vertex_to_index:
            return False

        source_idx = self._vertex_to_index[source]
        target_idx = self._vertex_to_index[target]

        if self._matrix[source_idx][target_idx] is not None:
            return False  # Edge already exists

        if metadata is None:
            metadata = {}

        edge = Edge(source, target, weight, metadata)
        self._matrix[source_idx][target_idx] = edge

        # For undirected graphs, add the reverse edge
        if not self._directed:
            reverse_edge = Edge(target, source, weight, metadata)  # pylint: disable=arguments-out-of-order
            self._matrix[target_idx][source_idx] = reverse_edge

        return True

    def remove_edge(self, source: V, target: V) -> bool:
        """Remove an edge. Returns True if removed."""
        if source not in self._vertex_to_index or target not in self._vertex_to_index:
            return False

        source_idx = self._vertex_to_index[source]
        target_idx = self._vertex_to_index[target]

        if self._matrix[source_idx][target_idx] is None:
            return False

        self._matrix[source_idx][target_idx] = None

        # For undirected graphs, remove the reverse edge
        if not self._directed:
            self._matrix[target_idx][source_idx] = None

        return True

    def has_vertex(self, vertex: V) -> bool:
        """Check if vertex exists."""
        return vertex in self._vertex_to_index

    def has_edge(self, source: V, target: V) -> bool:
        """Check if edge exists."""
        if source not in self._vertex_to_index or target not in self._vertex_to_index:
            return False

        source_idx = self._vertex_to_index[source]
        target_idx = self._vertex_to_index[target]
        return self._matrix[source_idx][target_idx] is not None

    def get_vertices(self) -> set[V]:
        """Get all vertices."""
        return set(self._vertex_to_index.keys())

    def get_edges(self) -> list[Edge[V]]:
        """Get all edges."""
        edges = []
        for row in self._matrix:
            for edge in row:
                if edge is not None:
                    edges.append(edge)
        return edges

    def get_neighbors(self, vertex: V) -> set[V]:
        """Get adjacent vertices."""
        if vertex not in self._vertex_to_index:
            return set()

        neighbors = set()
        source_idx = self._vertex_to_index[vertex]
        for target_idx, edge in enumerate(self._matrix[source_idx]):
            if edge is not None:
                neighbors.add(self._index_to_vertex[target_idx])

        return neighbors

    def get_edge_data(self, source: V, target: V) -> Edge[V] | None:
        """Get edge data if edge exists."""
        if source not in self._vertex_to_index or target not in self._vertex_to_index:
            return None

        source_idx = self._vertex_to_index[source]
        target_idx = self._vertex_to_index[target]
        return self._matrix[source_idx][target_idx]
