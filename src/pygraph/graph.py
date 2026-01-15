"""Graph data structure implementation.

This module provides the main Graph class that supports both directed and undirected
graphs with optional weights. The implementation uses modern Python 3.14+ features
including PEP 695 type parameter syntax.

The Graph class supports two internal representations:
- Adjacency list (default): Efficient for sparse graphs
- Adjacency matrix: Efficient for dense graphs or frequent edge queries

The Graph class delegates to representation classes that implement the
GraphRepresentation protocol, allowing flexible switching between representations.
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import Literal

from pygraph.edge import Edge
from pygraph.exceptions import VertexNotFoundError
from pygraph.representations import AdjacencyList, AdjacencyMatrix, GraphRepresentation


class Graph[V: Hashable]:
    """A graph data structure supporting directed/undirected and weighted/unweighted graphs.

    The Graph class provides a flexible implementation that can be configured as:
    - Directed or undirected
    - Weighted or unweighted
    - Using adjacency list or adjacency matrix representation

    The class delegates to representation classes (AdjacencyList or AdjacencyMatrix)
    that handle the low-level storage and manipulation of graph data.

    Type Parameters:
        V: The vertex type, must be hashable

    Args:
        directed: Whether the graph is directed (default: False)
        weighted: Whether the graph supports edge weights (default: True)
        representation: Internal representation to use (default: "adjacency_list")

    Example:
        >>> graph = Graph[str](directed=True, weighted=True)
        >>> graph.add_vertex("a")
        >>> graph.add_vertex("b")
        >>> graph.add_edge("a", "b", weight=5.0)
    """

    # Class constants for valid representations
    _VALID_REPRESENTATIONS = {"adjacency_list", "adjacency_matrix"}

    def __init__(
        self,
        directed: bool = False,
        weighted: bool = True,
        representation: Literal["adjacency_list", "adjacency_matrix"] = "adjacency_list",
    ) -> None:
        """Initialize a new graph with the specified configuration.

        Args:
            directed: Whether the graph is directed (default: False)
            weighted: Whether the graph supports edge weights (default: True)
            representation: Internal representation to use (default: "adjacency_list")

        Raises:
            ValueError: If representation is not valid
        """
        # Validate representation parameter
        if representation not in self._VALID_REPRESENTATIONS:
            raise ValueError(
                f"Invalid representation '{representation}'. "
                f"Must be one of: {', '.join(sorted(self._VALID_REPRESENTATIONS))}"
            )

        self._directed = directed
        self._weighted = weighted
        self._representation = representation

        # Delegate to appropriate representation class
        self._repr: GraphRepresentation[V] = self._create_representation(representation, directed)

    def _create_representation(self, representation: str, directed: bool) -> GraphRepresentation[V]:
        """Create the appropriate representation instance.

        Args:
            representation: The representation type
            directed: Whether the graph is directed

        Returns:
            The representation instance
        """
        if representation == "adjacency_list":
            return AdjacencyList[V](directed)
        return AdjacencyMatrix[V](directed)

    # Configuration Properties

    @property
    def directed(self) -> bool:
        """Whether the graph is directed."""
        return self._directed

    @property
    def weighted(self) -> bool:
        """Whether the graph supports edge weights."""
        return self._weighted

    @property
    def representation(self) -> str:
        """The internal representation type."""
        return self._representation

    # Basic Graph Operations

    def add_vertex(self, vertex: V) -> None:
        """Add a vertex to the graph.

        This operation is idempotent - adding an existing vertex has no effect.

        Args:
            vertex: The vertex to add (must be hashable)

        Raises:
            TypeError: If vertex is not hashable

        Examples:
            >>> graph = Graph[str]()
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> len(graph.vertices())
            2
            >>> graph.add_vertex("A")  # Idempotent - no effect
            >>> len(graph.vertices())
            2
            >>> graph.add_vertex([1, 2])  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            TypeError: Vertex must be hashable, got list: [1, 2]
        """
        self._validate_vertex_hashable(vertex)
        self._repr.add_vertex(vertex)

    def remove_vertex(self, vertex: V) -> None:
        """Remove a vertex from the graph.

        This operation removes the vertex and all edges incident to it.
        If the vertex doesn't exist, raises VertexNotFoundError.

        Args:
            vertex: The vertex to remove

        Raises:
            VertexNotFoundError: If vertex is not in the graph

        Examples:
            >>> graph = Graph[str]()
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> len(graph.vertices())
            2
            >>> graph.remove_vertex("A")
            >>> len(graph.vertices())
            1
            >>> "A" in graph.vertices()
            False
            >>> graph.remove_vertex("nonexistent")  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            VertexNotFoundError: Vertex nonexistent not found in graph
        """
        if not self._repr.has_vertex(vertex):
            available = sorted(self._repr.get_vertices()) if self._repr.get_vertices() else "none"
            raise VertexNotFoundError(f"Vertex '{vertex}' not found in graph. Available vertices: {available}")

        self._repr.remove_vertex(vertex)

    def _validate_vertex_hashable(self, vertex: V) -> None:
        """Validate that a vertex is hashable.

        Args:
            vertex: The vertex to validate

        Raises:
            TypeError: If vertex is not hashable
        """
        try:
            hash(vertex)
        except TypeError as e:
            raise TypeError(f"Vertex must be hashable, got {type(vertex).__name__}: {vertex}") from e

    # Query Methods

    def vertices(self) -> set[V]:
        """Get all vertices in the graph.

        Returns:
            Set of all vertices in the graph

        Examples:
            >>> graph = Graph[str]()
            >>> graph.vertices()
            set()
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> sorted(graph.vertices())
            ['A', 'B']
        """
        return self._repr.get_vertices()

    def edges(self) -> set[Edge[V]]:
        """Get all edges in the graph.

        Returns:
            Set of all edges in the graph
        """
        return set(self._repr.get_edges())

    def num_vertices(self) -> int:
        """Get the number of vertices in the graph.

        Returns:
            Number of vertices in the graph

        Examples:
            >>> graph = Graph[str]()
            >>> graph.num_vertices()
            0
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.num_vertices()
            2
            >>> graph.remove_vertex("A")
            >>> graph.num_vertices()
            1
        """
        return len(self.vertices())

    def num_edges(self) -> int:
        """Get the number of edges in the graph.

        Returns:
            Number of edges in the graph
        """
        return len(self.edges())

    # Protocol Implementation

    def to_graph(self) -> Graph[V]:
        """Convert to a Graph representation (GraphLike protocol).

        Returns:
            Self (Graph is already a graph)
        """
        return self
