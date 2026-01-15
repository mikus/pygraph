"""Property-based tests for Graph class.

This module contains property-based tests that verify the correctness properties
defined in the design document. These tests use Hypothesis to generate random
inputs and verify that the Graph class behaves correctly across all inputs.

These tests follow the TDD methodology:
- RED phase: Tests are written first and should FAIL (Graph class doesn't exist yet)
- GREEN phase: Implement Graph class to make tests pass
- REFACTOR phase: Improve implementation while keeping tests green
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from pygraph.graph import Graph


@pytest.mark.property
@settings(max_examples=100)
@given(
    directed=st.booleans(),
    weighted=st.booleans(),
    representation=st.sampled_from(["adjacency_list", "adjacency_matrix"]),
)
def test_property_empty_graph_creation(directed, weighted, representation):
    """Property: New graphs are empty.

    Feature: graph-library, Property 1: For any newly created graph
    (regardless of type), the graph should have zero vertices and zero edges.

    **Validates: Requirements A1.4**

    This test verifies that when a Graph is created with any valid configuration,
    it starts with an empty state (no vertices, no edges).
    """
    # Create a new graph with the given configuration
    graph = Graph(directed=directed, weighted=weighted, representation=representation)

    # Property: New graph should have zero vertices and zero edges
    assert len(graph.vertices()) == 0, f"New graph should have 0 vertices, got {len(graph.vertices())}"
    assert len(graph.edges()) == 0, f"New graph should have 0 edges, got {len(graph.edges())}"

    # Additional checks for consistency
    assert graph.num_vertices() == 0, f"num_vertices() should return 0, got {graph.num_vertices()}"
    assert graph.num_edges() == 0, f"num_edges() should return 0, got {graph.num_edges()}"


@pytest.mark.property
@settings(max_examples=100)
@given(
    non_hashable=st.one_of(
        st.lists(st.integers()),  # Lists are not hashable
        st.sets(st.integers()),  # Sets are not hashable
        st.dictionaries(st.text(), st.integers()),  # Dicts are not hashable
    )
)
def test_property_hashable_vertex_requirement(non_hashable):
    """Property: Hashable vertex requirement.

    Feature: graph-library, Property 2: For any attempt to add a non-hashable vertex,
    the operation should raise a TypeError.

    **Validates: Requirements A1.6**

    This test verifies that the Graph class enforces the requirement that all
    vertices must be hashable types. Non-hashable types (lists, sets, dicts)
    should be rejected with a TypeError.
    """
    # Create a new graph
    graph = Graph()

    # Property: Adding non-hashable vertex should raise TypeError
    with pytest.raises(TypeError, match=".*hashable.*"):
        graph.add_vertex(non_hashable)
