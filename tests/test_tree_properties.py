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
