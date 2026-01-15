"""Core protocols for the PyGraph library.

This module defines the protocols that enable unified algorithms to work
on both Graph and Tree structures. Using Python 3.14+ PEP 695 type parameter
syntax for clean, modern type definitions.

The protocols defined here are:
- GraphLike[V]: For any structure that can be treated as a graph
- TraversalContainer[T]: For containers used in graph traversal algorithms

These protocols enable the library's unified architecture where:
1. BFS and DFS algorithms work on both Graph and Tree structures
2. Different container implementations (FIFO, LIFO, Priority) enable different traversal strategies
3. Type safety is maintained through generic type parameters

Example:
    >>> from pygraph.protocols import GraphLike, TraversalContainer
    >>>
    >>> def bfs(graph: GraphLike[str], start: str) -> list[str]:
    ...     # This function works on any GraphLike structure (Graph or Tree)
    ...     pass
    >>>
    >>> def traverse_with_container(graph: GraphLike[str],
    ...                           container: TraversalContainer[str]) -> list[str]:
    ...     # Generic traversal using any container strategy
    ...     pass
"""

from collections.abc import Hashable, Iterable, Set
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    # Forward reference to avoid circular imports
    from .graph import Graph


@runtime_checkable
class GraphLike[V: Hashable](Protocol):
    """Protocol for graph-like structures that can be traversed.

    This protocol defines the interface that both Graph and Tree classes
    implement, allowing algorithms like BFS and DFS to work uniformly
    across both structures.

    Type Parameters:
        V: The vertex type, must be hashable

    Methods:
        vertices(): Get all vertices in the structure
        edges(): Get all edges in the structure
        neighbors(vertex): Get adjacent vertices for a given vertex
        has_edge(source, target): Check if an edge exists between two vertices
        to_graph(): Convert to a Graph representation for algorithm use

    Example:
        >>> def traverse(graph_like: GraphLike[str]) -> None:
        ...     for vertex in graph_like.vertices():
        ...         print(f"Vertex: {vertex}")
        ...         for neighbor in graph_like.neighbors(vertex):
        ...             print(f"  -> {neighbor}")
    """

    def vertices(self) -> Set[V]:
        """Get all vertices in the structure.

        Returns:
            A set containing all vertices in the graph-like structure.
        """

    def edges(self) -> Iterable[tuple[V, V]]:
        """Get all edges in the structure.

        Returns:
            An iterable of (source, target) tuples representing edges.
        """

    def neighbors(self, vertex: V) -> Set[V]:
        """Get adjacent vertices for a given vertex.

        Args:
            vertex: The vertex to get neighbors for

        Returns:
            A set of vertices adjacent to the given vertex.

        Raises:
            VertexNotFoundError: If the vertex doesn't exist in the structure.
        """

    def has_edge(self, source: V, target: V) -> bool:
        """Check if an edge exists between two vertices.

        Args:
            source: The source vertex
            target: The target vertex

        Returns:
            True if an edge exists from source to target, False otherwise.
        """

    def to_graph(self) -> "Graph[V]":
        """Convert to a Graph representation.

        This method allows algorithms to work with a unified Graph interface
        regardless of whether the original structure was a Graph or Tree.

        Returns:
            A Graph representation of this structure.
        """


@runtime_checkable
class TraversalContainer[T](Protocol):
    """Protocol for containers used in graph traversal algorithms.

    This protocol defines the interface for containers that control
    the order of vertex visitation in traversal algorithms. Different
    implementations (FIFO queue, LIFO stack, priority queue) enable
    different traversal strategies.

    Type Parameters:
        T: The type of items stored in the container

    Methods:
        push(item): Add an item to the container
        pop(): Remove and return an item from the container
        is_empty(): Check if the container is empty

    Example:
        >>> def generic_traversal(container: TraversalContainer[str]) -> None:
        ...     container.push("start")
        ...     while not container.is_empty():
        ...         current = container.pop()
        ...         print(f"Visiting: {current}")
    """

    def push(self, item: T) -> None:
        """Add an item to the container.

        Args:
            item: The item to add to the container
        """

    def pop(self) -> T:
        """Remove and return an item from the container.

        Returns:
            The next item according to the container's ordering strategy.

        Raises:
            IndexError: If the container is empty.
        """

    def is_empty(self) -> bool:
        """Check if the container is empty.

        Returns:
            True if the container has no items, False otherwise.
        """


# Export protocols for convenient importing
__all__ = [
    "GraphLike",
    "TraversalContainer",
]
