"""Property-based tests for Edge class.

This module contains property-based tests for the Edge class, focusing on
correctness properties that should hold for all valid edge instances.

These tests are part of the RED phase of TDD - they should FAIL initially
because the Edge class doesn't exist yet.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

# Import will fail initially - this is expected for TDD RED phase
# pylint: disable=import-outside-toplevel


@pytest.mark.property
@given(
    source=st.text(min_size=1, max_size=10),
    target=st.text(min_size=1, max_size=10),
    weight=st.floats(min_value=-1000.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=100)
def test_edge_weight_preservation(source, target, weight):
    """Property: Edge weights are preserved.

    Feature: pygraph, Property 9: For any edge with weight W, retrieving the edge returns weight W

    This test verifies that when an edge is created with a specific weight,
    that weight is preserved and can be retrieved correctly.

    Validates: Requirements B2.5
    """
    # This import will fail initially because Edge class doesn't exist yet
    # This is expected behavior for TDD RED phase
    from src.pygraph.edge import Edge

    # Create an edge with the given weight
    edge = Edge(source=source, target=target, weight=weight)

    # Property: The edge should preserve the weight exactly
    assert edge.weight == weight

    # Additional property: The edge should preserve source and target
    assert edge.source == source
    assert edge.target == target


@pytest.mark.property
@given(
    source=st.integers(),
    target=st.integers(),
    weight=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
    metadata=st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=st.one_of(st.text(), st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
    ),
)
@settings(max_examples=100)
def test_edge_metadata_preservation(source, target, weight, metadata):
    """Property: Edge metadata is preserved.

    Feature: pygraph, Property 11: For any edge with metadata, retrieving the edge returns the same metadata

    This test verifies that when an edge is created with metadata,
    that metadata is preserved and can be retrieved correctly.

    Validates: Requirements B2.9
    """
    # This import will fail initially because Edge class doesn't exist yet
    # This is expected behavior for TDD RED phase
    from src.pygraph.edge import Edge

    # Create an edge with the given metadata
    edge = Edge(source=source, target=target, weight=weight, metadata=metadata)

    # Property: The edge should preserve the metadata exactly
    assert edge.metadata == metadata

    # Additional properties: The edge should preserve all other fields
    assert edge.source == source
    assert edge.target == target
    assert edge.weight == weight


@pytest.mark.unit
@pytest.mark.parametrize(
    "weight,metadata,expected_weight,expected_metadata",
    [
        (None, None, 1.0, {}),  # Default weight
        (5.5, None, 5.5, {}),  # Custom weight
        (2.0, {"type": "highway", "speed_limit": 65}, 2.0, {"type": "highway", "speed_limit": 65}),  # With metadata
    ],
    ids=["default_weight", "custom_weight", "with_metadata"],
)
def test_edge_creation(weight, metadata, expected_weight, expected_metadata):
    """Test edge creation with various parameters (consolidated test)."""
    from src.pygraph.edge import Edge

    # Create edge with appropriate parameters
    if weight is None and metadata is None:
        edge = Edge(source="A", target="B")
    elif metadata is None:
        edge = Edge(source="A", target="B", weight=weight)
    else:
        edge = Edge(source="A", target="B", weight=weight, metadata=metadata)

    assert edge.weight == expected_weight
    assert edge.source == "A"
    assert edge.target == "B"
    assert edge.metadata == expected_metadata


@pytest.mark.unit
def test_edge_equality_and_hash():
    """Test edge equality, hash, and set/dict behavior (consolidated test)."""
    from src.pygraph.edge import Edge

    edge1 = Edge(source="A", target="B", weight=1.0)
    edge2 = Edge(source="A", target="B", weight=1.0)
    edge3 = Edge(source="A", target="B", weight=2.0)
    edge4 = Edge(source="B", target="A", weight=1.0)

    # Test equality
    assert edge1 == edge2
    assert edge1 != edge3
    assert edge1 != edge4

    # Test hash
    assert hash(edge1) == hash(edge2)

    # Test set behavior
    edge_set = {edge1, edge2, edge3}
    assert len(edge_set) == 2  # edge1 and edge2 are equal

    # Test dict behavior
    edge_dict = {edge1: "value1", edge3: "value2"}
    assert len(edge_dict) == 2

    # Test metadata doesn't affect equality/hash
    edge_with_meta1 = Edge("A", "B", weight=1.0, metadata={"color": "red"})
    edge_with_meta2 = Edge("A", "B", weight=1.0, metadata={"color": "blue"})
    edge_no_meta = Edge("A", "B", weight=1.0, metadata={})

    assert edge_with_meta1 == edge_with_meta2
    assert edge_with_meta1 == edge_no_meta
    assert hash(edge_with_meta1) == hash(edge_with_meta2)
    assert len({edge_with_meta1, edge_with_meta2, edge_no_meta}) == 1

    # But metadata is still accessible and different
    assert edge_with_meta1.metadata != edge_with_meta2.metadata
    assert edge_with_meta1.metadata["color"] == "red"
    assert edge_with_meta2.metadata["color"] == "blue"


@pytest.mark.unit
def test_edge_non_hashable_vertices_raise_error():
    """Test that non-hashable vertices raise TypeError."""
    from src.pygraph.edge import Edge

    # Test with non-hashable source
    with pytest.raises(TypeError, match="Edge vertices must be hashable"):
        Edge(source=["A"], target="B")  # List is not hashable

    # Test with non-hashable target
    with pytest.raises(TypeError, match="Edge vertices must be hashable"):
        Edge(source="A", target={"B": 1})  # Dict is not hashable

    # Test with both non-hashable
    with pytest.raises(TypeError, match="Edge vertices must be hashable"):
        Edge(source=["A"], target=["B"])  # Both lists are not hashable


@pytest.mark.unit
def test_edge_directed_vs_undirected_equality():
    """Test that directed and undirected edges have different equality behavior."""
    from src.pygraph.edge import Edge

    # Directed edges: order matters
    directed_ab = Edge("A", "B", weight=1.0, directed=True)
    directed_ba = Edge("B", "A", weight=1.0, directed=True)
    assert directed_ab != directed_ba
    assert hash(directed_ab) != hash(directed_ba)
    assert len({directed_ab, directed_ba}) == 2

    # Undirected edges: order doesn't matter
    undirected_ab = Edge("A", "B", weight=1.0, directed=False)
    undirected_ba = Edge("B", "A", weight=1.0, directed=False)
    assert undirected_ab == undirected_ba
    assert hash(undirected_ab) == hash(undirected_ba)
    assert len({undirected_ab, undirected_ba}) == 1

    # Directed and undirected edges are not equal even with same vertices
    assert directed_ab != undirected_ab


@pytest.mark.unit
def test_edge_helper_methods():
    """Test Edge helper methods (has_vertex, other_vertex)."""
    from src.pygraph.edge import Edge

    edge = Edge("A", "B", weight=2.0, directed=False)

    # Test has_vertex
    assert edge.has_vertex("A")
    assert edge.has_vertex("B")
    assert not edge.has_vertex("C")

    # Test other_vertex
    assert edge.other_vertex("A") == "B"
    assert edge.other_vertex("B") == "A"

    # Test other_vertex with invalid vertex
    with pytest.raises(ValueError, match="Vertex .* is not part of this edge"):
        edge.other_vertex("C")


@pytest.mark.unit
def test_edge_undirected_non_comparable_vertices():
    """Test undirected edges with non-comparable vertices use hash-based ordering.

    This tests the fallback behavior when vertices are hashable but not comparable.
    The edge should still normalize to canonical order using hash values.
    """
    from src.pygraph.edge import Edge

    # Create custom non-comparable but hashable class
    class NonComparable:
        """A hashable but non-comparable type."""

        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return hash(self.value)

        def __eq__(self, other):
            return isinstance(other, NonComparable) and self.value == other.value

        def __repr__(self):
            return f"NonComparable({self.value})"

    # Create two non-comparable vertices
    vertex_a = NonComparable("A")
    vertex_b = NonComparable("B")

    # Create undirected edges in both orders
    edge_ab = Edge(vertex_a, vertex_b, weight=1.0, directed=False)
    edge_ba = Edge(vertex_b, vertex_a, weight=1.0, directed=False)

    # Both edges should be normalized to the same canonical order
    # They should be equal and have the same hash
    assert edge_ab == edge_ba
    assert hash(edge_ab) == hash(edge_ba)

    # They should be the same edge in a set
    assert len({edge_ab, edge_ba}) == 1


@pytest.mark.unit
def test_edge_undirected_self_loop():
    """Test undirected edge where source equals target (self-loop).

    Self-loops should not be normalized since source == target.
    """
    from src.pygraph.edge import Edge

    # Create a self-loop
    edge = Edge("A", "A", weight=1.0, directed=False)

    # Source and target should remain the same
    assert edge.source == "A"
    assert edge.target == "A"

    # Should be hashable and usable in sets
    edge_set = {edge}
    assert len(edge_set) == 1


if __name__ == "__main__":
    pytest.main([__file__])
