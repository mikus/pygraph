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
from pygraph.exceptions import EdgeNotFoundError, VertexNotFoundError
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
        self._validate_vertex_exists(vertex, "removal")
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

    def _validate_vertex_exists(self, vertex: V, operation: str = "operation") -> None:
        """Validate that a vertex exists in the graph.

        Args:
            vertex: The vertex to validate
            operation: Description of the operation being performed (for error message)

        Raises:
            VertexNotFoundError: If vertex is not in the graph
        """
        if not self._repr.has_vertex(vertex):
            available = sorted(self._repr.get_vertices()) if self._repr.get_vertices() else "none"
            raise VertexNotFoundError(
                f"Vertex '{vertex}' not found in graph for {operation}. Available vertices: {available}"
            )

    def _validate_edge_vertices(self, source: V, target: V, operation: str = "operation") -> None:
        """Validate that both source and target vertices exist in the graph.

        This is a convenience method for edge operations that need to validate
        both endpoints of an edge.

        Args:
            source: The source vertex to validate
            target: The target vertex to validate
            operation: Description of the operation being performed (for error message)

        Raises:
            VertexNotFoundError: If either source or target vertex is not in the graph
        """
        self._validate_vertex_exists(source, operation)
        self._validate_vertex_exists(target, operation)

    def _validate_edge_exists(self, source: V, target: V) -> None:
        """Validate that an edge exists between two vertices.

        Args:
            source: The source vertex of the edge
            target: The target vertex of the edge

        Raises:
            EdgeNotFoundError: If the edge doesn't exist in the graph
        """
        if not self._repr.has_edge(source, target):
            raise EdgeNotFoundError(f"Edge ('{source}', '{target}') not found in graph")

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

        For undirected graphs, each edge is returned once (not both directions).
        For directed graphs, each directed edge is returned separately.

        Returns:
            Set of all edges in the graph

        Examples:
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> len(graph.edges())
            1
        """
        return self._repr.get_edges()

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

    # Edge Operations

    def add_edge(self, source: V, target: V, weight: float = 1.0, metadata: dict[str, any] | None = None) -> None:
        """Add an edge to the graph.

        This operation is idempotent - adding an existing edge has no effect.
        Both source and target vertices must already exist in the graph.

        For directed graphs, adds an edge from source to target.
        For undirected graphs, adds a bidirectional edge between source and target.

        Args:
            source: The source vertex of the edge
            target: The target vertex of the edge
            weight: The weight of the edge (default: 1.0)
            metadata: Optional metadata dictionary for the edge

        Raises:
            VertexNotFoundError: If source or target vertex is not in the graph

        Examples:
            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_edge("A", "B", weight=5.0)
            >>> graph.has_edge("A", "B")
            True
            >>> graph.has_edge("B", "A")  # Reverse direction doesn't exist
            False

            >>> # Undirected graph
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("X")
            >>> graph.add_vertex("Y")
            >>> graph.add_edge("X", "Y", weight=3.0)
            >>> graph.has_edge("X", "Y")
            True
            >>> graph.has_edge("Y", "X")  # Both directions work
            True

            >>> # Idempotent behavior
            >>> graph.add_edge("X", "Y", weight=3.0)
            >>> graph.num_edges()
            1

            >>> # With metadata
            >>> metadata = {"type": "highway", "lanes": 4}
            >>> graph.add_edge("X", "Y", weight=10.0, metadata=metadata)
        """
        # Validate both vertices exist
        self._validate_edge_vertices(source, target, "edge addition")

        # Add edge through representation (handles idempotency)
        self._repr.add_edge(source, target, weight, metadata or {})

    def remove_edge(self, source: V, target: V) -> None:
        """Remove an edge from the graph.

        This operation removes the edge between source and target vertices.
        The vertices themselves remain in the graph.

        For directed graphs, removes only the edge from source to target.
        For undirected graphs, removes the bidirectional edge between vertices.

        Args:
            source: The source vertex of the edge
            target: The target vertex of the edge

        Raises:
            EdgeNotFoundError: If the edge doesn't exist in the graph
            VertexNotFoundError: If source or target vertex is not in the graph

        Examples:
            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.remove_edge("A", "B")
            >>> graph.has_edge("A", "B")
            False
            >>> # Vertices still exist
            >>> graph.num_vertices()
            2

            >>> # Undirected graph
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("X")
            >>> graph.add_vertex("Y")
            >>> graph.add_edge("X", "Y", weight=1.0)
            >>> graph.remove_edge("X", "Y")
            >>> graph.has_edge("X", "Y")
            False
            >>> graph.has_edge("Y", "X")  # Both directions removed
            False
        """
        # Validate both vertices exist
        self._validate_edge_vertices(source, target, "edge removal")

        # Validate edge exists
        self._validate_edge_exists(source, target)

        # Remove edge through representation
        self._repr.remove_edge(source, target)

    def has_edge(self, source: V, target: V) -> bool:
        """Check if an edge exists between two vertices.

        For directed graphs, checks if edge exists from source to target.
        For undirected graphs, checks if edge exists in either direction.

        Args:
            source: The source vertex of the edge
            target: The target vertex of the edge

        Returns:
            True if the edge exists, False otherwise

        Examples:
            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.has_edge("A", "B")
            False
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.has_edge("A", "B")
            True
            >>> graph.has_edge("B", "A")  # Reverse doesn't exist
            False

            >>> # Undirected graph
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("X")
            >>> graph.add_vertex("Y")
            >>> graph.add_edge("X", "Y", weight=1.0)
            >>> graph.has_edge("X", "Y")
            True
            >>> graph.has_edge("Y", "X")  # Both directions work
            True
        """
        return self._repr.has_edge(source, target)

    def get_edge(self, source: V, target: V) -> Edge[V]:
        """Get the edge between two vertices.

        For directed graphs, retrieves the edge from source to target.
        For undirected graphs, retrieves the edge in either direction (normalized).

        Args:
            source: The source vertex of the edge
            target: The target vertex of the edge

        Returns:
            The Edge object containing source, target, weight, and metadata.
            For undirected graphs, the edge is normalized to canonical form.

        Raises:
            EdgeNotFoundError: If the edge doesn't exist in the graph

        Examples:
            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_edge("A", "B", weight=3.5, metadata={"type": "road"})
            >>> edge = graph.get_edge("A", "B")
            >>> edge.weight
            3.5
            >>> edge.metadata
            {'type': 'road'}
            >>> edge.source
            'A'
            >>> edge.target
            'B'

            >>> # Undirected graph - edges are normalized
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("X")
            >>> graph.add_vertex("Y")
            >>> graph.add_edge("X", "Y", weight=2.0, metadata={"lanes": 2})
            >>> edge1 = graph.get_edge("X", "Y")
            >>> edge2 = graph.get_edge("Y", "X")
            >>> edge1 == edge2  # Same edge (normalized)
            True
            >>> edge1.weight
            2.0
        """
        self._validate_edge_exists(source, target)
        edge_data = self._repr.get_edge_data(source, target)
        return edge_data

    # Analysis Methods

    def neighbors(self, vertex: V) -> set[V]:
        """Get the neighbors of a vertex.

        For directed graphs, returns vertices reachable by outgoing edges.
        For undirected graphs, returns all adjacent vertices.

        Args:
            vertex: The vertex to get neighbors for

        Returns:
            Set of neighboring vertices

        Raises:
            VertexNotFoundError: If vertex is not in the graph

        Examples:
            >>> # Undirected graph
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_vertex("C")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.add_edge("A", "C", weight=1.0)
            >>> sorted(graph.neighbors("A"))
            ['B', 'C']
            >>> sorted(graph.neighbors("B"))
            ['A']

            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_vertex("C")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.add_edge("B", "C", weight=1.0)
            >>> sorted(graph.neighbors("A"))
            ['B']
            >>> sorted(graph.neighbors("B"))
            ['C']
            >>> graph.neighbors("C")
            set()
        """
        self._validate_vertex_exists(vertex, "getting neighbors")
        return self._repr.get_neighbors(vertex)

    def degree(self, vertex: V) -> int:
        """Get the degree of a vertex.

        For undirected graphs, returns the number of edges connected to the vertex.
        For directed graphs, returns the out-degree (number of outgoing edges).

        Args:
            vertex: The vertex to get degree for

        Returns:
            The degree of the vertex

        Raises:
            VertexNotFoundError: If vertex is not in the graph

        Examples:
            >>> # Undirected graph
            >>> graph = Graph[str](directed=False)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_vertex("C")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.add_edge("A", "C", weight=1.0)
            >>> graph.degree("A")
            2
            >>> graph.degree("B")
            1

            >>> # Directed graph (returns out-degree)
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_vertex("C")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.add_edge("B", "C", weight=1.0)
            >>> graph.degree("A")
            1
            >>> graph.degree("C")
            0
        """
        self._validate_vertex_exists(vertex, "getting degree")
        # Degree equals the number of neighbors
        return len(self.neighbors(vertex))

    def in_degree(self, vertex: V) -> int:
        """Get the in-degree of a vertex (number of incoming edges).

        This method only works for directed graphs. For undirected graphs,
        use degree() instead.

        Args:
            vertex: The vertex to get in-degree for

        Returns:
            The in-degree of the vertex (number of incoming edges)

        Raises:
            VertexNotFoundError: If vertex is not in the graph
            ValueError: If graph is not directed

        Examples:
            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_vertex("C")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.add_edge("A", "C", weight=1.0)
            >>> graph.add_edge("B", "C", weight=1.0)
            >>> graph.in_degree("A")
            0
            >>> graph.in_degree("B")
            1
            >>> graph.in_degree("C")
            2
        """
        if not self._directed:
            raise ValueError("in_degree() only works on directed graphs. Use degree() for undirected graphs.")

        self._validate_vertex_exists(vertex, "getting in-degree")

        # Count edges where this vertex is the target
        in_deg = 0
        for edge in self.edges():
            if edge.target == vertex:
                in_deg += 1

        return in_deg

    def out_degree(self, vertex: V) -> int:
        """Get the out-degree of a vertex (number of outgoing edges).

        This method only works for directed graphs. For undirected graphs,
        use degree() instead.

        Args:
            vertex: The vertex to get out-degree for

        Returns:
            The out-degree of the vertex (number of outgoing edges)

        Raises:
            VertexNotFoundError: If vertex is not in the graph
            ValueError: If graph is not directed

        Examples:
            >>> # Directed graph
            >>> graph = Graph[str](directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_vertex("C")
            >>> graph.add_edge("A", "B", weight=1.0)
            >>> graph.add_edge("A", "C", weight=1.0)
            >>> graph.add_edge("B", "C", weight=1.0)
            >>> graph.out_degree("A")
            2
            >>> graph.out_degree("B")
            1
            >>> graph.out_degree("C")
            0
        """
        if not self._directed:
            raise ValueError("out_degree() only works on directed graphs. Use degree() for undirected graphs.")

        self._validate_vertex_exists(vertex, "getting out-degree")

        # For directed graphs, out-degree equals the number of neighbors
        return len(self.neighbors(vertex))

    # Protocol Implementation

    def to_graph(self) -> Graph[V]:
        """Convert to a Graph representation (GraphLike protocol).

        Returns:
            Self (Graph is already a graph)
        """
        return self
