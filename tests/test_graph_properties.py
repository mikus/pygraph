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


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=2, max_size=10, unique=True),
    edge_index=st.integers(min_value=0, max_value=100),
    weight=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
)
def test_property_edge_addition_increases_count(vertices, edge_index, weight):
    """Property: Edge addition increases edge count.

    Feature: graph-library, Property 6: For any graph and any new edge (between
    existing vertices), adding the edge should increase the edge count by exactly one.

    **Validates: Requirements B2.1**

    This test verifies that when a new edge (not already present) is added to
    a graph between two existing vertices, the edge count increases by exactly one.
    The test uses random lists of vertices and random edge selections to ensure
    the property holds across all valid inputs.
    """
    # Skip if we don't have at least 2 vertices
    if len(vertices) < 2:
        return

    # Create a new graph
    graph = Graph()

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Select two different vertices for the edge
    source_idx = edge_index % len(vertices)
    target_idx = (edge_index + 1) % len(vertices)
    source = vertices[source_idx]
    target = vertices[target_idx]

    # Ensure source and target are different
    if source == target:
        if len(vertices) > 1:
            target = vertices[(target_idx + 1) % len(vertices)]
        else:
            return  # Skip if we can't create a valid edge

    # Capture initial state
    initial_edge_count = graph.num_edges()
    initial_vertex_count = graph.num_vertices()

    # Property: Adding new edge should increase edge count by exactly 1
    try:
        graph.add_edge(source, target, weight=weight)

        final_edge_count = graph.num_edges()
        final_vertex_count = graph.num_vertices()

        # Verify edge count increased by 1
        assert final_edge_count == initial_edge_count + 1, (
            f"Adding new edge should increase count by 1. "
            f"Initial: {initial_edge_count}, Final: {final_edge_count}, "
            f"Edge: ({source}, {target}), Weight: {weight}"
        )

        # Verify vertex count is unchanged
        assert final_vertex_count == initial_vertex_count, (
            f"Adding edge should not change vertex count. "
            f"Initial: {initial_vertex_count}, Final: {final_vertex_count}"
        )

        # Verify the edge exists in the graph
        assert graph.has_edge(source, target), f"Edge ({source}, {target}) should exist in graph"

    except AttributeError:
        # Expected: add_edge method doesn't exist yet (RED phase)
        # This test should fail until the method is implemented
        pytest.fail("add_edge method not implemented yet (expected in RED phase)")


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=2, max_size=10, unique=True),
    edge_index=st.integers(min_value=0, max_value=100),
    weight=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
    metadata=st.dictionaries(
        keys=st.text(min_size=1, max_size=5),
        values=st.one_of(st.text(), st.integers()),
        max_size=3,
    ),
)
def test_property_duplicate_edge_idempotency(vertices, edge_index, weight, metadata):
    """Property: Duplicate edge addition is idempotent.

    Feature: graph-library, Property 7: For any graph and any edge already
    in the graph, adding the edge again should not change the graph state
    (vertex count, edge count, or structure).

    **Validates: Requirements B2.3**

    This test verifies that adding an edge that already exists in the graph
    is an idempotent operation - it has no effect on the graph state. The
    edge count, vertex count, and overall structure should remain unchanged.
    """
    # Skip if we don't have at least 2 vertices
    if len(vertices) < 2:
        return

    # Create a new graph
    graph = Graph()

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Select two different vertices for the edge
    source_idx = edge_index % len(vertices)
    target_idx = (edge_index + 1) % len(vertices)
    source = vertices[source_idx]
    target = vertices[target_idx]

    # Ensure source and target are different
    if source == target:
        if len(vertices) > 1:
            target = vertices[(target_idx + 1) % len(vertices)]
        else:
            return  # Skip if we can't create a valid edge

    # Property: Adding duplicate edge should be idempotent (no change)
    try:
        # Add the edge first time
        graph.add_edge(source, target, weight=weight, metadata=metadata)

        # Capture state after first addition
        initial_vertex_count = graph.num_vertices()
        initial_edge_count = graph.num_edges()
        initial_vertices = graph.vertices().copy()
        initial_edges = graph.edges().copy()

        # Add the same edge again (duplicate)
        graph.add_edge(source, target, weight=weight, metadata=metadata)

        # Verify state is unchanged
        final_vertex_count = graph.num_vertices()
        final_edge_count = graph.num_edges()
        final_vertices = graph.vertices()
        final_edges = graph.edges()

        assert final_vertex_count == initial_vertex_count, (
            f"Vertex count should not change when adding duplicate edge. "
            f"Initial: {initial_vertex_count}, Final: {final_vertex_count}, "
            f"Edge: ({source}, {target})"
        )

        assert final_edge_count == initial_edge_count, (
            f"Edge count should not change when adding duplicate edge. "
            f"Initial: {initial_edge_count}, Final: {final_edge_count}, "
            f"Edge: ({source}, {target})"
        )

        assert final_vertices == initial_vertices, (
            f"Vertex set should not change when adding duplicate edge. "
            f"Initial: {initial_vertices}, Final: {final_vertices}"
        )

        assert final_edges == initial_edges, (
            f"Edge set should not change when adding duplicate edge. " f"Initial: {initial_edges}, Final: {final_edges}"
        )

    except AttributeError:
        # Expected: add_edge method doesn't exist yet (RED phase)
        # This test should fail until the method is implemented
        pytest.fail("add_edge method not implemented yet (expected in RED phase)")


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=2, max_size=10, unique=True),
    edge_index=st.integers(min_value=0, max_value=100),
    weight=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
)
def test_property_edge_removal_preserves_vertices(vertices, edge_index, weight):
    """Property: Edge removal preserves vertices.

    Feature: graph-library, Property 8: For any graph and any edge in the graph,
    removing the edge should decrease the edge count by one but not change the
    vertex count.

    **Validates: Requirements B2.4**

    This test verifies that when an edge is removed from a graph, the vertices
    that were connected by that edge remain in the graph. Only the edge itself
    is removed, not the vertices it connects.
    """
    # Skip if we don't have at least 2 vertices
    if len(vertices) < 2:
        return

    # Create a new graph
    graph = Graph()

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Select two different vertices for the edge
    source_idx = edge_index % len(vertices)
    target_idx = (edge_index + 1) % len(vertices)
    source = vertices[source_idx]
    target = vertices[target_idx]

    # Ensure source and target are different
    if source == target:
        if len(vertices) > 1:
            target = vertices[(target_idx + 1) % len(vertices)]
        else:
            return  # Skip if we can't create a valid edge

    # Property: Removing edge should preserve vertices
    try:
        # Add the edge
        graph.add_edge(source, target, weight=weight)

        # Capture state after adding edge
        initial_vertex_count = graph.num_vertices()
        initial_edge_count = graph.num_edges()
        initial_vertices = graph.vertices().copy()

        # Remove the edge
        graph.remove_edge(source, target)

        # Verify edge count decreased by 1
        final_edge_count = graph.num_edges()
        assert final_edge_count == initial_edge_count - 1, (
            f"Edge count should decrease by 1 when removing edge. "
            f"Initial: {initial_edge_count}, Final: {final_edge_count}, "
            f"Edge: ({source}, {target})"
        )

        # Verify vertex count is unchanged
        final_vertex_count = graph.num_vertices()
        assert final_vertex_count == initial_vertex_count, (
            f"Vertex count should not change when removing edge. "
            f"Initial: {initial_vertex_count}, Final: {final_vertex_count}, "
            f"Edge: ({source}, {target})"
        )

        # Verify vertices are unchanged
        final_vertices = graph.vertices()
        assert final_vertices == initial_vertices, (
            f"Vertex set should not change when removing edge. " f"Initial: {initial_vertices}, Final: {final_vertices}"
        )

        # Verify both vertices still exist
        assert source in graph.vertices(), f"Source vertex {source} should still exist after edge removal"
        assert target in graph.vertices(), f"Target vertex {target} should still exist after edge removal"

        # Verify the edge no longer exists
        assert not graph.has_edge(source, target), f"Edge ({source}, {target}) should not exist after removal"

    except AttributeError:
        # Expected: add_edge or remove_edge method doesn't exist yet (RED phase)
        # This test should fail until the methods are implemented
        pytest.fail("add_edge or remove_edge method not implemented yet (expected in RED phase)")


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=2, max_size=10, unique=True),
    edge_index=st.integers(min_value=0, max_value=100),
    weight=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
)
def test_property_directed_edge_distinction(vertices, edge_index, weight):
    """Property: Directed edges are distinct.

    Feature: graph-library, Property 10: For any directed graph, adding edge (u,v)
    does not imply that edge (v,u) exists. The two edges are distinct and must be
    added separately.

    **Validates: Requirements B2.8**

    This test verifies that in a directed graph, edges have direction. Adding an
    edge from u to v does not automatically create an edge from v to u. The graph
    must distinguish between (u,v) and (v,u) as separate edges.
    """
    # Skip if we don't have at least 2 vertices
    if len(vertices) < 2:
        return

    # Create a DIRECTED graph
    graph = Graph(directed=True)

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Select two different vertices for the edge
    source_idx = edge_index % len(vertices)
    target_idx = (edge_index + 1) % len(vertices)
    source = vertices[source_idx]
    target = vertices[target_idx]

    # Ensure source and target are different
    if source == target:
        if len(vertices) > 1:
            target = vertices[(target_idx + 1) % len(vertices)]
        else:
            return  # Skip if we can't create a valid edge

    # Property: In directed graph, (u,v) doesn't imply (v,u) exists
    try:
        # Add edge from source to target
        graph.add_edge(source, target, weight=weight)

        # Verify the forward edge exists
        assert graph.has_edge(source, target), f"Edge ({source}, {target}) should exist"

        # Verify the reverse edge does NOT exist
        # pylint: disable-next=arguments-out-of-order
        assert not graph.has_edge(target, source), (
            f"In directed graph, edge ({source}, {target}) should not imply " f"edge ({target}, {source}) exists"
        )

        # Verify edge count is 1 (only the forward edge)
        assert graph.num_edges() == 1, (
            f"Directed graph should have exactly 1 edge after adding ({source}, {target}), " f"got {graph.num_edges()}"
        )

        # Now add the reverse edge explicitly
        graph.add_edge(target, source, weight=weight)  # pylint: disable=arguments-out-of-order

        # Verify both edges now exist
        assert graph.has_edge(source, target), f"Forward edge ({source}, {target}) should still exist"
        # pylint: disable-next=arguments-out-of-order
        assert graph.has_edge(
            target, source
        ), f"Reverse edge ({target}, {source}) should now exist"  # pylint: disable=arguments-out-of-order

        # Verify edge count is 2 (both directions)
        assert graph.num_edges() == 2, (
            f"Directed graph should have exactly 2 edges after adding both directions, " f"got {graph.num_edges()}"
        )

    except AttributeError:
        # Expected: add_edge or has_edge method doesn't exist yet (RED phase)
        # This test should fail until the methods are implemented
        pytest.fail("add_edge or has_edge method not implemented yet (expected in RED phase)")


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=1, max_size=10, unique=True),
    directed=st.booleans(),
    edge_pairs=st.lists(
        st.tuples(st.integers(min_value=0, max_value=9), st.integers(min_value=0, max_value=9)),
        min_size=0,
        max_size=15,
    ),
)
def test_property_neighbors_and_degree_consistency(vertices, directed, edge_pairs):
    """Property: Neighbors and degree consistency.

    Feature: graph-library, Property 12: For any graph and any vertex in the graph,
    the degree of the vertex should equal the number of neighbors.

    **Validates: Requirements B3.1, B3.2**

    This test verifies that the degree() method returns a value consistent with
    the number of neighbors returned by neighbors(). For undirected graphs, degree
    equals the number of neighbors. For directed graphs, out_degree equals the
    number of neighbors (outgoing edges).
    """
    # Skip if we don't have any vertices
    if len(vertices) == 0:
        return

    # Create a graph with the specified directedness
    graph = Graph(directed=directed)

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Add edges based on edge_pairs
    for source_idx, target_idx in edge_pairs:
        # Map indices to actual vertices
        source = vertices[source_idx % len(vertices)]
        target = vertices[target_idx % len(vertices)]

        # Skip self-loops for this test
        if source == target:
            continue

        # Add edge if both vertices exist
        try:
            graph.add_edge(source, target, weight=1.0)
        except Exception:  # pylint: disable=broad-except
            # Skip if edge addition fails for any reason
            continue

    # Property: For each vertex, degree should equal number of neighbors
    try:
        for vertex in vertices:
            # Get neighbors and degree
            neighbors_set = graph.neighbors(vertex)
            degree_value = graph.degree(vertex)

            # Property: degree equals number of neighbors
            assert len(neighbors_set) == degree_value, (
                f"For vertex {vertex}, degree ({degree_value}) should equal "
                f"number of neighbors ({len(neighbors_set)}). "
                f"Neighbors: {neighbors_set}, "
                f"Directed: {directed}"
            )

            # Additional consistency checks
            # For undirected graphs, each neighbor should have this vertex as a neighbor
            if not directed:
                for neighbor in neighbors_set:
                    neighbor_neighbors = graph.neighbors(neighbor)
                    assert vertex in neighbor_neighbors, (
                        f"In undirected graph, if {neighbor} is neighbor of {vertex}, "
                        f"then {vertex} should be neighbor of {neighbor}"
                    )

    except AttributeError:
        # Expected: neighbors() or degree() method doesn't exist yet (RED phase)
        # This test should fail until the methods are implemented
        pytest.fail("neighbors() or degree() method not implemented yet (expected in RED phase)")


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=2, max_size=10, unique=True),
    edge_pairs=st.lists(
        st.tuples(st.integers(min_value=0, max_value=9), st.integers(min_value=0, max_value=9)),
        min_size=0,
        max_size=15,
    ),
)
def test_property_in_degree_and_out_degree(vertices, edge_pairs):
    """Property: In-degree and out-degree relationship.

    Feature: graph-library, Property 15: For any directed graph and any vertex,
    the sum of in_degree and out_degree equals the total number of edges incident
    to that vertex.

    **Validates: Requirements B3.7**

    This test verifies that for directed graphs, the in_degree (number of incoming
    edges) plus the out_degree (number of outgoing edges) equals the total number
    of edges connected to a vertex. This property only applies to directed graphs.
    """
    # Skip if we don't have at least 2 vertices
    if len(vertices) < 2:
        return

    # Create a DIRECTED graph (property only applies to directed graphs)
    graph = Graph(directed=True)

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Add edges based on edge_pairs
    for source_idx, target_idx in edge_pairs:
        # Map indices to actual vertices
        source = vertices[source_idx % len(vertices)]
        target = vertices[target_idx % len(vertices)]

        # Skip self-loops for this test
        if source == target:
            continue

        # Add edge if both vertices exist
        try:
            graph.add_edge(source, target, weight=1.0)
        except Exception:  # pylint: disable=broad-except
            # Skip if edge addition fails for any reason
            continue

    # Property: For each vertex in directed graph, in_degree + out_degree = total incident edges
    try:
        for vertex in vertices:
            # Get in-degree and out-degree
            in_deg = graph.in_degree(vertex)
            out_deg = graph.out_degree(vertex)

            # Count actual incident edges manually for verification
            incident_edges = 0
            for edge in graph.edges():
                if vertex in (edge.source, edge.target):
                    incident_edges += 1

            # Property: in_degree + out_degree should equal total incident edges
            assert in_deg + out_deg == incident_edges, (
                f"For vertex {vertex} in directed graph, "
                f"in_degree ({in_deg}) + out_degree ({out_deg}) = {in_deg + out_deg} "
                f"should equal total incident edges ({incident_edges})"
            )

            # Additional consistency checks
            # in_degree should equal number of edges where vertex is target
            expected_in_degree = sum(1 for edge in graph.edges() if edge.target == vertex)
            assert in_deg == expected_in_degree, (
                f"in_degree ({in_deg}) should equal number of incoming edges ({expected_in_degree}) "
                f"for vertex {vertex}"
            )

            # out_degree should equal number of edges where vertex is source
            expected_out_degree = sum(1 for edge in graph.edges() if edge.source == vertex)
            assert out_deg == expected_out_degree, (
                f"out_degree ({out_deg}) should equal number of outgoing edges ({expected_out_degree}) "
                f"for vertex {vertex}"
            )

    except AttributeError:
        # Expected: in_degree() or out_degree() method doesn't exist yet (RED phase)
        # This test should fail until the methods are implemented
        pytest.fail("in_degree() or out_degree() method not implemented yet (expected in RED phase)")


@pytest.mark.property
@settings(max_examples=100)
@given(
    directed=st.booleans(),
    weighted=st.booleans(),
    initial_representation=st.sampled_from(["adjacency_list", "adjacency_matrix"]),
    vertices=st.lists(st.integers(), min_size=0, max_size=10, unique=True),
    edge_pairs=st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=9),
            st.integers(min_value=0, max_value=9),
            st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
            st.dictionaries(
                keys=st.text(min_size=1, max_size=5),
                values=st.one_of(st.text(), st.integers()),
                max_size=3,
            ),
        ),
        min_size=0,
        max_size=15,
    ),
)
def test_property_repr_conversion_preserves_graph(directed, weighted, initial_representation, vertices, edge_pairs):
    """Property: Representation conversion preserves graph.

    Feature: graph-library, Property 20: For any graph, converting from adjacency
    list to adjacency matrix (or vice versa) should preserve all vertices, edges,
    weights, and metadata.

    **Validates: Requirements A3.4**

    This test verifies that when a graph's internal representation is converted
    between adjacency list and adjacency matrix, all graph data is preserved:
    - All vertices remain in the graph
    - All edges remain in the graph
    - Edge weights are preserved
    - Edge metadata is preserved
    - Graph properties (directed, weighted) are preserved
    """
    # Skip if we don't have any vertices
    if len(vertices) == 0:
        return

    # Create a graph with the initial representation
    graph = Graph(directed=directed, weighted=weighted, representation=initial_representation)

    # Add vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Add edges based on edge_pairs
    added_edges = []
    for source_idx, target_idx, weight, metadata in edge_pairs:
        # Map indices to actual vertices
        source = vertices[source_idx % len(vertices)]
        target = vertices[target_idx % len(vertices)]

        # Skip self-loops for this test
        if source == target:
            continue

        # Skip if edge already exists (for idempotency)
        if graph.has_edge(source, target):
            continue

        # Add edge
        try:
            graph.add_edge(source, target, weight=weight, metadata=metadata)
            added_edges.append((source, target, weight, metadata))
        except Exception:  # pylint: disable=broad-except
            # Skip if edge addition fails for any reason
            continue

    # Capture initial state before conversion
    initial_vertices = graph.vertices().copy()
    initial_edges = graph.edges().copy()
    initial_vertex_count = graph.num_vertices()
    initial_edge_count = graph.num_edges()
    initial_directed = graph.directed
    initial_weighted = graph.weighted

    # Determine target representation (opposite of initial)
    target_representation = "adjacency_matrix" if initial_representation == "adjacency_list" else "adjacency_list"

    # Property: Converting representation should preserve all graph data
    try:
        # Convert to target representation
        graph.convert_representation(target_representation)

        # Verify representation changed
        assert graph.representation == target_representation, (
            f"Representation should change from {initial_representation} to {target_representation}, "
            f"got {graph.representation}"
        )

        # Verify vertices are preserved
        final_vertices = graph.vertices()
        assert final_vertices == initial_vertices, (
            f"Vertices should be preserved after conversion. " f"Initial: {initial_vertices}, Final: {final_vertices}"
        )

        # Verify vertex count is preserved
        final_vertex_count = graph.num_vertices()
        assert final_vertex_count == initial_vertex_count, (
            f"Vertex count should be preserved after conversion. "
            f"Initial: {initial_vertex_count}, Final: {final_vertex_count}"
        )

        # Verify edges are preserved
        final_edges = graph.edges()
        assert final_edges == initial_edges, (
            f"Edges should be preserved after conversion. " f"Initial: {initial_edges}, Final: {final_edges}"
        )

        # Verify edge count is preserved
        final_edge_count = graph.num_edges()
        assert final_edge_count == initial_edge_count, (
            f"Edge count should be preserved after conversion. "
            f"Initial: {initial_edge_count}, Final: {final_edge_count}"
        )

        # Verify graph properties are preserved
        assert graph.directed == initial_directed, (
            f"Directed property should be preserved. " f"Initial: {initial_directed}, Final: {graph.directed}"
        )

        assert graph.weighted == initial_weighted, (
            f"Weighted property should be preserved. " f"Initial: {initial_weighted}, Final: {graph.weighted}"
        )

        # Verify each edge's weight and metadata are preserved
        for source, target, weight, metadata in added_edges:
            # Check edge still exists
            assert graph.has_edge(source, target), f"Edge ({source}, {target}) should still exist after conversion"

            # Get edge and verify weight and metadata
            edge = graph.get_edge(source, target)
            assert edge.weight == weight, (
                f"Edge ({source}, {target}) weight should be preserved. " f"Expected: {weight}, Got: {edge.weight}"
            )

            assert edge.metadata == metadata, (
                f"Edge ({source}, {target}) metadata should be preserved. "
                f"Expected: {metadata}, Got: {edge.metadata}"
            )

        # Test round-trip conversion (convert back to original representation)
        graph.convert_representation(initial_representation)

        # Verify representation changed back
        assert graph.representation == initial_representation, (
            f"Representation should change back to {initial_representation}, " f"got {graph.representation}"
        )

        # Verify all data is still preserved after round-trip
        assert graph.vertices() == initial_vertices, "Vertices should be preserved after round-trip conversion"

        assert graph.edges() == initial_edges, "Edges should be preserved after round-trip conversion"

        assert (
            graph.num_vertices() == initial_vertex_count
        ), "Vertex count should be preserved after round-trip conversion"

        assert graph.num_edges() == initial_edge_count, "Edge count should be preserved after round-trip conversion"

        # Verify each edge's weight and metadata are still preserved after round-trip
        for source, target, weight, metadata in added_edges:
            assert graph.has_edge(
                source, target
            ), f"Edge ({source}, {target}) should still exist after round-trip conversion"

            edge = graph.get_edge(source, target)
            assert edge.weight == weight, (
                f"Edge ({source}, {target}) weight should be preserved after round-trip. "
                f"Expected: {weight}, Got: {edge.weight}"
            )

            assert edge.metadata == metadata, (
                f"Edge ({source}, {target}) metadata should be preserved after round-trip. "
                f"Expected: {metadata}, Got: {edge.metadata}"
            )

    except AttributeError:
        # Expected: convert_representation method doesn't exist yet (RED phase)
        # This test should fail until the method is implemented
        pytest.fail("convert_representation method not implemented yet (expected in RED phase)")
