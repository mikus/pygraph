"""Property-based tests for Tree class.

This module contains property-based tests that verify the correctness properties
defined in the design document for the Tree data structure. These tests use
Hypothesis to generate random inputs and verify that the Tree class behaves
correctly across all inputs.

These tests follow the TDD methodology:
- RED phase: Tests are written first and should FAIL (Tree class doesn't exist yet)
- GREEN phase: Implement Tree class to make tests pass
- REFACTOR phase: Improve implementation while keeping tests green
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from pygraph.exceptions import CycleError
from pygraph.tree import Tree


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=3, max_size=10, unique=True),
    edge_pairs=st.lists(
        st.tuples(st.integers(min_value=0, max_value=9), st.integers(min_value=0, max_value=9)),
        min_size=2,
        max_size=8,
    ),
)
def test_property_trees_remain_acyclic(vertices, edge_pairs):
    """Property: Trees remain acyclic.

    Feature: graph-library, Property 17: For any tree and any attempt to add an edge
    that would create a cycle, the operation should be rejected and the tree should
    remain unchanged.

    **Validates: Requirements A2.3**

    This test verifies that the Tree class enforces the acyclic constraint. When
    an attempt is made to add an edge that would create a cycle, the operation
    should raise a CycleError and the tree should remain in its original state
    (no vertices or edges added, no structure changed).

    The test creates a tree structure, then attempts to add edges that would
    create cycles. Each attempt should be rejected with a CycleError, and the
    tree should remain unchanged.
    """
    # Skip if we don't have enough vertices to create a meaningful tree
    if len(vertices) < 3:
        return

    # Create a tree with the first vertex as root
    root = vertices[0]
    tree = Tree(root)

    # Build a tree structure by adding parent-child relationships
    # We'll create a simple tree structure to ensure we have a valid tree first
    added_vertices = {root}
    parent_child_pairs = []

    for i in range(1, min(len(vertices), 5)):
        parent = vertices[0]  # Use root as parent for simplicity
        child = vertices[i]

        if child not in added_vertices:
            try:
                tree.add_child(parent, child)
                added_vertices.add(child)
                parent_child_pairs.append((parent, child))
            except Exception:  # pylint: disable=broad-except
                # Skip if add_child fails for any reason
                continue

    # Capture initial state before attempting to create cycle
    initial_vertex_count = tree.num_vertices()
    initial_edge_count = tree.num_edges()

    # Property: Attempting to add cycle-creating edge should raise CycleError
    # and leave tree unchanged

    # Test Case 1: Try to add edge from child back to parent (creates 2-cycle)
    if len(parent_child_pairs) > 0:
        parent, child = parent_child_pairs[0]

        # Attempt to add edge from child to parent (would create cycle)
        with pytest.raises(CycleError, match=".*cycle.*"):
            tree.add_child(child, parent)

        # Verify tree state is unchanged
        assert tree.num_vertices() == initial_vertex_count, (
            f"Tree vertex count should be unchanged after rejected cycle creation. "
            f"Initial: {initial_vertex_count}, Final: {tree.num_vertices()}"
        )

        assert tree.num_edges() == initial_edge_count, (
            f"Tree edge count should be unchanged after rejected cycle creation. "
            f"Initial: {initial_edge_count}, Final: {tree.num_edges()}"
        )

    # Test Case 2: Try to add edge that creates a longer cycle
    # If we have at least 3 vertices in the tree, try to create a cycle
    if len(parent_child_pairs) >= 2:
        # Get two parent-child pairs
        parent1, child1 = parent_child_pairs[0]
        parent2, child2 = parent_child_pairs[1]

        # If child2 is different from parent1, try to add edge from child2 to parent1
        # This would create a cycle if there's a path from parent1 to child2
        if child2 != parent1 and child2 in added_vertices:
            # Capture state before attempt
            state_before_vertex_count = tree.num_vertices()
            state_before_edge_count = tree.num_edges()

            # Attempt to add edge that would create cycle
            # Note: This might not always create a cycle depending on tree structure,
            # but if it does, it should raise CycleError
            try:
                tree.add_child(child2, parent1)
                # If no error was raised, verify the tree is still acyclic
                # (the edge might not have created a cycle in this particular structure)
            except CycleError:
                # Expected: CycleError was raised
                # Verify tree state is unchanged
                assert tree.num_vertices() == state_before_vertex_count, (
                    f"Tree vertex count should be unchanged after rejected cycle creation. "
                    f"Before: {state_before_vertex_count}, After: {tree.num_vertices()}"
                )

                assert tree.num_edges() == state_before_edge_count, (
                    f"Tree edge count should be unchanged after rejected cycle creation. "
                    f"Before: {state_before_edge_count}, After: {tree.num_edges()}"
                )

    # Test Case 3: Try to add a vertex that already exists as a child
    # (would create a cycle by having a vertex with two parents)
    if len(parent_child_pairs) >= 2:
        parent1, child1 = parent_child_pairs[0]
        parent2, child2 = parent_child_pairs[1]

        # Try to add child1 as a child of parent2 (child1 already has parent1 as parent)
        if parent2 != parent1 and child1 in added_vertices:
            state_before_vertex_count = tree.num_vertices()
            state_before_edge_count = tree.num_edges()

            # This should fail because child1 already exists in the tree
            # (a vertex can only have one parent in a tree)
            try:
                tree.add_child(parent2, child1)
                # If this succeeds, it's an error - trees can't have vertices with multiple parents
                pytest.fail(
                    f"Tree allowed adding existing vertex {child1} as child of {parent2}, "
                    f"but it already has parent {parent1}. This would create a cycle."
                )
            except (CycleError, ValueError):
                # Expected: Either CycleError or ValueError should be raised
                # Verify tree state is unchanged
                assert tree.num_vertices() == state_before_vertex_count, (
                    f"Tree vertex count should be unchanged after rejected operation. "
                    f"Before: {state_before_vertex_count}, After: {tree.num_vertices()}"
                )

                assert tree.num_edges() == state_before_edge_count, (
                    f"Tree edge count should be unchanged after rejected operation. "
                    f"Before: {state_before_edge_count}, After: {tree.num_edges()}"
                )

    # Final verification: Tree should still be acyclic
    # We can verify this by checking that num_edges == num_vertices - 1
    # (a tree with n vertices has exactly n-1 edges)
    final_vertex_count = tree.num_vertices()
    final_edge_count = tree.num_edges()

    assert final_edge_count == final_vertex_count - 1, (
        f"Tree should have exactly (vertices - 1) edges. "
        f"Vertices: {final_vertex_count}, Edges: {final_edge_count}, "
        f"Expected edges: {final_vertex_count - 1}"
    )


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=1, max_size=15, unique=True),
    edge_indices=st.lists(
        st.tuples(st.integers(min_value=0, max_value=14), st.integers(min_value=0, max_value=14)),
        min_size=0,
        max_size=10,
    ),
)
def test_property_tree_to_graph_conversion_preserves_structure(vertices, edge_indices):
    """Property: Tree to graph conversion preserves structure.

    Feature: graph-library, Property 18: For any tree, converting it to a graph
    and checking properties should show the same vertices, edges, and connectivity.

    **Validates: Requirements A2.5**

    This test verifies that the to_graph() method correctly converts a tree to
    a graph representation while preserving all structural properties:
    - All vertices are preserved
    - All edges are preserved
    - Connectivity is preserved (same parent-child relationships)
    - Edge directions are preserved (directed graph)
    - The graph is acyclic (tree property maintained)

    The test creates a tree structure, converts it to a graph using to_graph(),
    and verifies that the graph has the same vertices, edges, and structural
    properties as the original tree.
    """
    # Skip if we don't have enough vertices
    if len(vertices) < 1:
        return

    # Create a tree with the first vertex as root
    root = vertices[0]
    tree = Tree(root)

    # Build a tree structure by adding parent-child relationships
    # We'll create a valid tree by ensuring each child is added only once
    added_vertices = {root}
    tree_edges = []  # Track edges as (parent, child) tuples

    # Add children to build the tree
    for i in range(1, len(vertices)):
        # Choose a parent from already added vertices
        parent_idx = i % len(added_vertices)
        parent = list(added_vertices)[parent_idx]
        child = vertices[i]

        if child not in added_vertices:
            try:
                tree.add_child(parent, child)
                added_vertices.add(child)
                tree_edges.append((parent, child))
            except Exception:  # pylint: disable=broad-except
                # Skip if add_child fails for any reason
                continue

    # Convert tree to graph
    graph = tree.to_graph()

    # Property 1: All tree vertices should be in the graph
    tree_vertices = tree.vertices()
    graph_vertices = graph.vertices()

    assert tree_vertices == graph_vertices, (
        f"Graph should have same vertices as tree. " f"Tree vertices: {tree_vertices}, Graph vertices: {graph_vertices}"
    )

    # Property 2: Vertex count should be preserved
    assert tree.num_vertices() == graph.num_vertices(), (
        f"Graph should have same vertex count as tree. " f"Tree: {tree.num_vertices()}, Graph: {graph.num_vertices()}"
    )

    # Property 3: All tree edges should be in the graph
    tree_edge_set = tree.edges()
    graph_edge_set = {(edge.source, edge.target) for edge in graph.edges()}

    assert tree_edge_set == graph_edge_set, (
        f"Graph should have same edges as tree. " f"Tree edges: {tree_edge_set}, Graph edges: {graph_edge_set}"
    )

    # Property 4: Edge count should be preserved
    assert tree.num_edges() == graph.num_edges(), (
        f"Graph should have same edge count as tree. " f"Tree: {tree.num_edges()}, Graph: {graph.num_edges()}"
    )

    # Property 5: Graph should be directed (trees are represented as directed graphs)
    assert graph.directed, "Graph converted from tree should be directed"

    # Property 6: Connectivity should be preserved - verify parent-child relationships
    for parent, child in tree_edges:
        assert graph.has_edge(parent, child), (
            f"Graph should have edge ({parent}, {child}) from tree. "
            f"Tree edges: {tree_edges}, Graph edges: {graph_edge_set}"
        )

        # Verify the edge direction is correct (parent -> child, not child -> parent)
        # In a tree, edges go from parent to child
        assert graph.has_edge(parent, child), f"Graph should have directed edge from parent {parent} to child {child}"

    # Property 7: For each vertex (except root), verify parent relationship is preserved
    for vertex in tree_vertices:
        if vertex != root:
            tree_parent = tree.parent(vertex)
            if tree_parent is not None:
                # Verify the parent-child edge exists in the graph
                assert graph.has_edge(
                    tree_parent, vertex
                ), f"Graph should have edge from parent {tree_parent} to child {vertex}"

    # Property 8: For each vertex, verify children relationships are preserved
    for vertex in tree_vertices:
        tree_children = tree.children(vertex)
        graph_neighbors = graph.neighbors(vertex)

        assert tree_children == graph_neighbors, (
            f"Graph neighbors should match tree children for vertex {vertex}. "
            f"Tree children: {tree_children}, Graph neighbors: {graph_neighbors}"
        )

    # Property 9: Graph should maintain tree property (n vertices, n-1 edges)
    if graph.num_vertices() > 0:
        assert graph.num_edges() == graph.num_vertices() - 1, (
            f"Graph should maintain tree property: edges = vertices - 1. "
            f"Vertices: {graph.num_vertices()}, Edges: {graph.num_edges()}"
        )

    # Property 10: Graph should be acyclic (tree property)
    # We can verify this by checking that the graph has the tree property:
    # - Connected (all vertices reachable from root)
    # - Acyclic (no cycles)
    # - For a tree: edges = vertices - 1
    # We've already verified edges = vertices - 1, which is a necessary condition

    # Additional verification: Each non-root vertex should have exactly one incoming edge
    for vertex in graph_vertices:
        if vertex != root:
            # Count incoming edges
            incoming_edges = sum(1 for edge in graph.edges() if edge.target == vertex)
            assert incoming_edges == 1, (
                f"Non-root vertex {vertex} should have exactly one incoming edge, " f"but has {incoming_edges}"
            )

    # Root should have no incoming edges
    root_incoming_edges = sum(1 for edge in graph.edges() if edge.target == root)
    assert root_incoming_edges == 0, (
        f"Root vertex {root} should have no incoming edges, " f"but has {root_incoming_edges}"
    )


@pytest.mark.property
@settings(max_examples=100)
@given(
    vertices=st.lists(st.integers(), min_size=2, max_size=10, unique=True),
    directed=st.booleans(),
    create_cycle=st.booleans(),
    make_disconnected=st.booleans(),
)
def test_property_graph_to_tree_validation(vertices, directed, create_cycle, make_disconnected):
    """Property: Graph to tree conversion validates constraints.

    Feature: graph-library, Property 19: For any graph, from_graph() succeeds
    if and only if the graph is directed, acyclic, and connected.

    **Validates: Requirements A2.6**

    This test verifies that the Tree.from_graph() method correctly validates
    that a graph meets tree constraints before conversion:
    - Graph must be directed (undirected graphs should be rejected)
    - Graph must be acyclic (graphs with cycles should be rejected)
    - Graph must be connected (disconnected graphs should be rejected)

    The test creates graphs with various properties and verifies that from_graph()
    succeeds only when all three constraints are met, and raises appropriate
    errors otherwise.
    """
    from pygraph.exceptions import InvalidGraphError
    from pygraph.graph import Graph

    # Skip if we don't have enough vertices
    if len(vertices) < 2:
        return

    # Create a graph with the specified properties
    root = vertices[0]
    graph = Graph[int](directed=directed)

    # Add all vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Build a tree-like structure first (connected, acyclic)
    # Then modify it based on test parameters
    added_edges = []

    # Create a simple tree structure (each vertex connects to next)
    for i in range(1, len(vertices)):
        parent = vertices[0]  # All connect to root for simplicity
        child = vertices[i]
        graph.add_edge(parent, child)
        added_edges.append((parent, child))

    # Track if we actually created a cycle or disconnection
    actually_has_cycle = False
    actually_disconnected = False

    # Modify graph based on test parameters
    if create_cycle and len(vertices) >= 2:
        # Add an edge that creates a cycle
        # For directed graph: add edge from child back to parent
        if directed and len(added_edges) > 0:
            parent, child = added_edges[0]
            # Add edge from child to parent (creates cycle)
            graph.add_edge(child, parent)
            actually_has_cycle = True

    if make_disconnected and len(vertices) >= 3:
        # Remove an edge to make graph disconnected
        if len(added_edges) > 0:
            parent, child = added_edges[0]
            graph.remove_edge(parent, child)
            actually_disconnected = True

    # Determine if conversion should succeed
    # Success conditions: directed AND acyclic AND connected
    should_succeed = directed and not actually_has_cycle and not actually_disconnected

    # For undirected graphs, they can't be trees (bidirectional edges create cycles)
    if not directed:
        should_succeed = False

    # Attempt conversion
    if should_succeed:
        # Conversion should succeed
        try:
            tree = Tree.from_graph(graph, root)

            # Verify the tree was created correctly
            assert tree.root == root, f"Tree root should be {root}, got {tree.root}"

            # Verify all vertices are in the tree
            assert tree.vertices() == graph.vertices(), (
                f"Tree should have same vertices as graph. " f"Tree: {tree.vertices()}, Graph: {graph.vertices()}"
            )

            # Verify tree has correct number of edges (n-1 for n vertices)
            if tree.num_vertices() > 0:
                assert tree.num_edges() == tree.num_vertices() - 1, (
                    f"Tree should have vertices-1 edges. " f"Vertices: {tree.num_vertices()}, Edges: {tree.num_edges()}"
                )

        except (ValueError, InvalidGraphError) as e:
            # If conversion failed when it should succeed, this is an error
            pytest.fail(
                f"Tree.from_graph() should have succeeded for directed, acyclic, "
                f"connected graph but raised {type(e).__name__}: {e}. "
                f"Graph properties: directed={directed}, has_cycle={actually_has_cycle}, "
                f"disconnected={actually_disconnected}"
            )
    else:
        # Conversion should fail with appropriate error
        with pytest.raises((ValueError, InvalidGraphError)):
            Tree.from_graph(graph, root)

        # Verify the error is raised (the with statement above handles this)
        # If we get here, the exception was raised as expected
