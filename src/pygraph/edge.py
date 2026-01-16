"""Edge dataclass for representing graph edges with weights and metadata.

This module provides the Edge dataclass that represents connections between
vertices in a graph, including support for weights and arbitrary metadata.
"""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Edge[V: Hashable]:
    """Represents an edge in a graph with weight and metadata.

    An edge connects two vertices (source and target) and can optionally
    include a numerical weight and arbitrary metadata dictionary.

    For directed edges, source and target have meaning and order matters.
    For undirected edges, the vertices are stored in canonical order
    (sorted) so that Edge(A, B) and Edge(B, A) are automatically equal.

    The edge uses dataclass default equality and hashing, but normalizes
    undirected edges in __post_init__ to ensure order-independent comparison.

    **Important**: While the edge fields are immutable, the metadata dictionary
    itself is mutable and can be modified after creation. This allows algorithms
    to annotate edges with additional information. Since metadata is excluded
    from equality/hash comparison, modifying it won't affect the edge's behavior
    in sets or as dictionary keys.

    Args:
        source: The source vertex (must be hashable and comparable for undirected edges)
        target: The target vertex (must be hashable and comparable for undirected edges)
        weight: Numerical weight of the edge (default: 1.0)
        metadata: Dictionary of arbitrary metadata (default: empty dict)
                 Note: Mutable and not included in equality/hash comparison
        directed: Whether this is a directed edge (default: True)

    Examples:
        >>> # Create a directed edge
        >>> edge = Edge(source="A", target="B", directed=True)
        >>> edge.weight
        1.0

        >>> # Directed edges are order-sensitive
        >>> edge1 = Edge("A", "B", directed=True)
        >>> edge2 = Edge("B", "A", directed=True)
        >>> edge1 == edge2
        False

        >>> # Undirected edges are order-insensitive (automatically normalized)
        >>> edge1 = Edge("A", "B", directed=False)
        >>> edge2 = Edge("B", "A", directed=False)
        >>> edge1 == edge2
        True
        >>> hash(edge1) == hash(edge2)
        True
        >>> # Both are normalized to the same canonical form
        >>> edge1.source, edge1.target
        ('A', 'B')
        >>> edge2.source, edge2.target
        ('A', 'B')

        >>> # Create a weighted edge
        >>> edge = Edge(source="A", target="B", weight=5.5)
        >>> edge.weight
        5.5

        >>> # Create an edge with metadata
        >>> metadata = {"type": "highway", "speed_limit": 65}
        >>> edge = Edge(source="A", target="B", weight=2.0, metadata=metadata)
        >>> edge.metadata["type"]
        'highway'

        >>> # Edges are hashable and can be used in sets
        >>> edge1 = Edge("A", "B", 1.0, directed=False)
        >>> edge2 = Edge("B", "A", 1.0, directed=False)
        >>> {edge1, edge2}  # Only one edge in set for undirected
        {Edge(source='A', target='B', weight=1.0, metadata={}, directed=False)}

        >>> # Metadata doesn't affect equality
        >>> edge3 = Edge("A", "B", 1.0, {"extra": "data"}, directed=False)
        >>> edge1 == edge3  # Same vertices, weight, directedness
        True
    """

    source: V
    target: V
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)
    directed: bool = True

    def __post_init__(self) -> None:
        """Validate and normalize edge data after initialization.

        For undirected edges, normalizes the source and target to canonical order
        (smaller vertex first) so that Edge(A, B) and Edge(B, A) are identical.
        """
        # Ensure source and target are hashable
        try:
            hash(self.source)
            hash(self.target)
        except TypeError as e:
            raise TypeError(f"Edge vertices must be hashable: {e}") from e

        # For undirected edges, normalize to canonical order
        if not self.directed and self.source != self.target:
            try:
                # Try to compare vertices - if they're comparable, use canonical order
                if self.source > self.target:  # type: ignore[operator]
                    # Swap source and target to maintain canonical order
                    # Use object.__setattr__ because dataclass is frozen
                    temp_source = self.source
                    object.__setattr__(self, "source", self.target)
                    object.__setattr__(self, "target", temp_source)
            except TypeError:
                # Vertices are not comparable - use hash-based ordering as fallback
                if hash(self.source) > hash(self.target):
                    temp_source = self.source
                    object.__setattr__(self, "source", self.target)
                    object.__setattr__(self, "target", temp_source)

    def has_vertex(self, vertex: V) -> bool:
        """Check if vertex is part of this edge.

        Args:
            vertex: The vertex to check

        Returns:
            True if vertex is source or target
        """
        return vertex in (self.source, self.target)

    def other_vertex(self, vertex: V) -> V:
        """Get the other vertex in the edge.

        Args:
            vertex: One vertex of the edge

        Returns:
            The other vertex

        Raises:
            ValueError: If vertex is not part of this edge
        """
        if vertex == self.source:
            return self.target
        if vertex == self.target:
            return self.source
        raise ValueError(f"Vertex {vertex} is not part of this edge")
