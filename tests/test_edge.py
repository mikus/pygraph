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
def test_edge_creation_with_default_weight():
    """Test edge creation with default weight."""
    # This import will fail initially because Edge class doesn't exist yet
    from src.pygraph.edge import Edge

    edge = Edge(source="A", target="B")

    # Default weight should be 1.0 according to design
    assert edge.weight == 1.0
    assert edge.source == "A"
    assert edge.target == "B"
    assert not edge.metadata


@pytest.mark.unit
def test_edge_creation_with_custom_weight():
    """Test edge creation with custom weight."""
    from src.pygraph.edge import Edge

    edge = Edge(source="A", target="B", weight=5.5)

    assert edge.weight == 5.5
    assert edge.source == "A"
    assert edge.target == "B"
    assert not edge.metadata


@pytest.mark.unit
def test_edge_creation_with_metadata():
    """Test edge creation with metadata."""
    from src.pygraph.edge import Edge

    metadata = {"type": "highway", "speed_limit": 65}
    edge = Edge(source="A", target="B", weight=2.0, metadata=metadata)

    assert edge.weight == 2.0
    assert edge.source == "A"
    assert edge.target == "B"
    assert edge.metadata == metadata


@pytest.mark.unit
def test_edge_equality():
    """Test edge equality comparison."""
    from src.pygraph.edge import Edge

    edge1 = Edge(source="A", target="B", weight=1.0)
    edge2 = Edge(source="A", target="B", weight=1.0)
    edge3 = Edge(source="A", target="B", weight=2.0)
    edge4 = Edge(source="B", target="A", weight=1.0)

    # Edges with same source, target, and weight should be equal
    assert edge1 == edge2

    # Edges with different weights should not be equal
    assert edge1 != edge3

    # Edges with different source/target should not be equal
    assert edge1 != edge4


@pytest.mark.unit
def test_edge_hash():
    """Test edge hash for use in sets and dictionaries."""
    from src.pygraph.edge import Edge

    edge1 = Edge(source="A", target="B", weight=1.0)
    edge2 = Edge(source="A", target="B", weight=1.0)
    edge3 = Edge(source="A", target="B", weight=2.0)

    # Equal edges should have same hash
    assert hash(edge1) == hash(edge2)

    # Edges should be usable in sets
    edge_set = {edge1, edge2, edge3}
    assert len(edge_set) == 2  # edge1 and edge2 are equal, so only 2 unique edges

    # Edges should be usable as dictionary keys
    edge_dict = {edge1: "value1", edge3: "value2"}
    assert len(edge_dict) == 2


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


if __name__ == "__main__":
    pytest.main([__file__])
