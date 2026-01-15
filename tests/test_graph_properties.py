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


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=0, max_size=20, unique=True),
    new_vertex=st.integers(),
)
def test_property_vertex_addition_increases_count(vertices, new_vertex):
    """Property: Vertex addition increases vertex count.

    Feature: graph-library, Property 3: For any graph and any hashable vertex
    not already in the graph, adding the vertex should increase the vertex count
    by exactly one.

    **Validates: Requirements B1.1**

    This test verifies that when a new vertex (not already present) is added to
    a graph, the vertex count increases by exactly one. The test uses random
    lists of initial vertices and a random new vertex to ensure the property
    holds across all valid inputs.
    """
    # Create a new graph
    graph = Graph()

    # Add initial vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    initial_count = graph.num_vertices()

    # Property: Adding new vertex should increase count by exactly 1
    if new_vertex not in vertices:
        graph.add_vertex(new_vertex)
        final_count = graph.num_vertices()
        assert final_count == initial_count + 1, (
            f"Adding new vertex should increase count by 1. "
            f"Initial: {initial_count}, Final: {final_count}, "
            f"New vertex: {new_vertex}, Existing vertices: {vertices}"
        )

        # Verify the new vertex is actually in the graph
        assert new_vertex in graph.vertices(), f"New vertex {new_vertex} should be in graph vertices"


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=1, max_size=20, unique=True),
    duplicate_vertex=st.integers(),
)
def test_property_duplicate_vertex_idempotency(vertices, duplicate_vertex):
    """Property: Duplicate vertex addition is idempotent.

    Feature: graph-library, Property 4: For any graph and any vertex already
    in the graph, adding the vertex again should not change the graph state
    (vertex count, edge count, or structure).

    **Validates: Requirements B1.2**

    This test verifies that adding a vertex that already exists in the graph
    is an idempotent operation - it has no effect on the graph state. The
    vertex count, edge count, and overall structure should remain unchanged.
    """
    # Create a new graph
    graph = Graph()

    # Add initial vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Choose a vertex that exists in the graph
    existing_vertex = vertices[0] if vertices else duplicate_vertex
    if existing_vertex not in vertices:
        # If duplicate_vertex is not in vertices, add it first
        graph.add_vertex(duplicate_vertex)
        existing_vertex = duplicate_vertex

    # Capture initial state
    initial_vertex_count = graph.num_vertices()
    initial_edge_count = graph.num_edges()
    initial_vertices = graph.vertices().copy()
    initial_edges = graph.edges().copy()

    # Property: Adding existing vertex should be idempotent (no change)
    graph.add_vertex(existing_vertex)

    # Verify state is unchanged
    final_vertex_count = graph.num_vertices()
    final_edge_count = graph.num_edges()
    final_vertices = graph.vertices()
    final_edges = graph.edges()

    assert final_vertex_count == initial_vertex_count, (
        f"Vertex count should not change when adding existing vertex. "
        f"Initial: {initial_vertex_count}, Final: {final_vertex_count}, "
        f"Existing vertex: {existing_vertex}"
    )

    assert final_edge_count == initial_edge_count, (
        f"Edge count should not change when adding existing vertex. "
        f"Initial: {initial_edge_count}, Final: {final_edge_count}, "
        f"Existing vertex: {existing_vertex}"
    )

    assert final_vertices == initial_vertices, (
        f"Vertex set should not change when adding existing vertex. "
        f"Initial: {initial_vertices}, Final: {final_vertices}, "
        f"Existing vertex: {existing_vertex}"
    )

    assert final_edges == initial_edges, (
        f"Edge set should not change when adding existing vertex. "
        f"Initial: {initial_edges}, Final: {final_edges}, "
        f"Existing vertex: {existing_vertex}"
    )


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=1, max_size=10, unique=True),
    vertex_to_remove=st.integers(),
)
def test_property_vertex_removal_removes_edges(vertices, vertex_to_remove):
    """Property: Vertex removal removes incident edges.

    Feature: graph-library, Property 5: For any graph and any vertex in the graph,
    removing the vertex should decrease the vertex count by one and remove all
    edges incident to that vertex.

    **Validates: Requirements B1.3**

    This test verifies that when a vertex is removed from a graph, all edges
    that are incident to (connected to) that vertex are also removed. The
    vertex count should decrease by exactly one, and no edges should remain
    that reference the removed vertex.

    Note: This test currently focuses on vertex removal. Edge testing will be
    added when add_edge method is implemented in later tasks.
    """
    # Skip if we don't have any vertices
    if len(vertices) == 0:
        return

    # Create a new graph
    graph = Graph()

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Choose a vertex to remove that exists in the graph
    if vertex_to_remove not in vertices:
        vertex_to_remove = vertices[0]

    # Capture initial state
    initial_vertex_count = graph.num_vertices()
    initial_edge_count = graph.num_edges()

    # Property: Removing vertex should decrease vertex count by 1 and remove incident edges
    try:
        graph.remove_vertex(vertex_to_remove)

        final_vertex_count = graph.num_vertices()
        final_edge_count = graph.num_edges()

        # Verify vertex count decreased by 1
        assert final_vertex_count == initial_vertex_count - 1, (
            f"Vertex count should decrease by 1 when removing vertex. "
            f"Initial: {initial_vertex_count}, Final: {final_vertex_count}, "
            f"Removed vertex: {vertex_to_remove}"
        )

        # Verify the removed vertex is no longer in the graph
        assert (
            vertex_to_remove not in graph.vertices()
        ), f"Removed vertex {vertex_to_remove} should not be in graph vertices"

        # Verify no edges reference the removed vertex (when edges are implemented)
        for edge in graph.edges():
            assert (
                edge.source != vertex_to_remove
            ), f"Edge {edge} should not have removed vertex {vertex_to_remove} as source"
            assert (
                edge.target != vertex_to_remove
            ), f"Edge {edge} should not have removed vertex {vertex_to_remove} as target"

        # For now, since we don't have edges, edge count should remain 0
        assert final_edge_count == initial_edge_count, (
            f"Edge count should remain unchanged when no edges exist. "
            f"Initial: {initial_edge_count}, Final: {final_edge_count}"
        )

    except AttributeError:
        # Expected: remove_vertex method doesn't exist yet (RED phase)
        # This test should fail until the method is implemented
        pytest.fail("remove_vertex method not implemented yet (expected in RED phase)")
