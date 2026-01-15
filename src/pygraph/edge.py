"""Edge dataclass for representing graph edges with weights and metadata.

This module provides the Edge dataclass that represents connections between
vertices in a graph, including support for weights and arbitrary metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Hashable


@dataclass(frozen=True)
class Edge[V: Hashable]:
    """Represents an edge in a graph with weight and metadata.

    An edge connects two vertices (source and target) and can optionally
    include a numerical weight and arbitrary metadata dictionary.

    The edge fields (source, target, weight) are immutable (frozen) and the
    edge is hashable. Equality and hashing are based on source, target, and
    weight only - metadata is excluded from comparison to allow edges with
    same structure but different metadata to be considered equal for graph
    operations.

    **Important**: While the edge fields are immutable, the metadata dictionary
    itself is mutable and can be modified after creation. This allows algorithms
    to annotate edges with additional information. Since metadata is excluded
    from equality/hash comparison, modifying it won't affect the edge's behavior
    in sets or as dictionary keys.

    Args:
        source: The source vertex (must be hashable)
        target: The target vertex (must be hashable)
        weight: Numerical weight of the edge (default: 1.0)
        metadata: Dictionary of arbitrary metadata (default: empty dict)
                 Note: Mutable and not included in equality/hash comparison

    Examples:
        >>> # Create a simple unweighted edge
        >>> edge = Edge(source="A", target="B")
        >>> edge.weight
        1.0

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
        >>> edge1 = Edge("A", "B", 1.0)
        >>> edge2 = Edge("A", "B", 1.0)
        >>> edge1 == edge2
        True
        >>> {edge1, edge2}  # Only one edge in set due to equality
        {Edge(source='A', target='B', weight=1.0, metadata={})}

        >>> # Metadata doesn't affect equality
        >>> edge3 = Edge("A", "B", 1.0, {"extra": "data"})
        >>> edge1 == edge3  # Same source, target, weight
        True

        >>> # Metadata can be modified after creation
        >>> edge = Edge("A", "B", 1.0, {"type": "road"})
        >>> edge.metadata["lanes"] = 4  # This works
        >>> edge.metadata
        {'type': 'road', 'lanes': 4}
    """

    source: V
    target: V
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        """Validate edge data after initialization."""
        # Ensure source and target are hashable
        try:
            hash(self.source)
            hash(self.target)
        except TypeError as e:
            raise TypeError(f"Edge vertices must be hashable: {e}") from e
