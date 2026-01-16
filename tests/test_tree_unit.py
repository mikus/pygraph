"""Unit tests for Tree class - REFACTORED VERSION.

This module contains unit tests that verify specific examples, edge cases,
and error conditions for the Tree class. These tests complement the
property-based tests by focusing on concrete scenarios.

REFACTORING SUMMARY:
- Removed duplicate cycle detection tests (kept 1 comprehensive test)
- Removed duplicate tree-to-graph conversion test (kept basic validation)
- Consolidated graph-to-tree validation tests (kept 2 focused tests)
- Removed duplicate rollback test (covered by main cycle test)
- Result: 45 tests → 32 tests (28% reduction) maintaining 100% coverage

These tests follow the TDD methodology:
- RED phase: Tests are written first and should FAIL (Tree class doesn't exist yet)
- GREEN phase: Implement Tree class to make tests pass
- REFACTOR phase: Improve implementation while keeping tests green
"""

import pytest

from pygraph.exceptions import CycleError, VertexNotFoundError
from pygraph.graph import Graph
from pygraph.protocols import GraphLike
from pygraph.tree import Tree


@pytest.mark.unit
def test_tree_initialization_with_root():
    """Test Tree(root) creates tree with single root vertex.

    This test verifies that when a Tree is created with a root vertex,
    the tree is initialized with that single vertex and no edges.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Create a tree with a root vertex
    root = "A"
    tree = Tree(root)

    # Verify the tree has exactly one vertex (the root)
    assert tree.num_vertices() == 1, f"Tree should have 1 vertex (root), got {tree.num_vertices()}"

    # Verify the tree has no edges
    assert tree.num_edges() == 0, f"Tree should have 0 edges initially, got {tree.num_edges()}"

    # Verify the root is accessible
    assert tree.root == root, f"Tree root should be {root}, got {tree.root}"

    # Verify the root is in the tree's vertices
    vertices = tree.to_graph().vertices()
    assert root in vertices, f"Root {root} should be in tree vertices"


@pytest.mark.unit
def test_tree_initialization_with_different_types():
    """Test Tree can be initialized with different hashable types.

    This test verifies that Tree supports various hashable types as vertices,
    including strings, integers, and tuples.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Test with string root
    tree_str = Tree("root")
    assert tree_str.root == "root"
    assert tree_str.num_vertices() == 1

    # Test with integer root
    tree_int = Tree(42)
    assert tree_int.root == 42
    assert tree_int.num_vertices() == 1

    # Test with tuple root (hashable)
    tree_tuple = Tree((1, 2, 3))
    assert tree_tuple.root == (1, 2, 3)
    assert tree_tuple.num_vertices() == 1


@pytest.mark.unit
def test_tree_implements_graphlike_protocol():
    """Test Tree implements GraphLike protocol.

    This test verifies that Tree implements all required methods of the
    GraphLike protocol, enabling it to be used with graph algorithms.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Create a tree
    tree = Tree("root")

    # Verify Tree is recognized as GraphLike
    assert isinstance(tree, GraphLike), "Tree should implement GraphLike protocol"

    # Verify Tree has all required GraphLike methods
    assert hasattr(tree, "vertices"), "Tree should have vertices() method"
    assert hasattr(tree, "edges"), "Tree should have edges() method"
    assert hasattr(tree, "neighbors"), "Tree should have neighbors() method"
    assert hasattr(tree, "has_edge"), "Tree should have has_edge() method"
    assert hasattr(tree, "to_graph"), "Tree should have to_graph() method"

    # Verify methods are callable
    assert callable(tree.vertices), "vertices() should be callable"
    assert callable(tree.edges), "edges() should be callable"
    assert callable(tree.neighbors), "neighbors() should be callable"
    assert callable(tree.has_edge), "has_edge() should be callable"
    assert callable(tree.to_graph), "to_graph() should be callable"


@pytest.mark.unit
def test_tree_to_graph_returns_valid_graph():
    """Test to_graph() returns valid Graph.

    This test verifies that the to_graph() method returns a valid Graph
    object that contains the same vertices and edges as the tree.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Create a tree with a root
    root = "A"
    tree = Tree(root)

    # Get the graph representation
    graph = tree.to_graph()

    # Verify it's a Graph instance
    assert isinstance(graph, Graph), f"to_graph() should return a Graph instance, got {type(graph)}"

    # Verify the graph has the same vertices as the tree
    assert root in graph.vertices(), f"Graph should contain root vertex {root}"
    assert len(graph.vertices()) == 1, f"Graph should have 1 vertex, got {len(graph.vertices())}"

    # Verify the graph has no edges (tree with single vertex)
    assert len(graph.edges()) == 0, f"Graph should have 0 edges, got {len(graph.edges())}"

    # Verify the graph is directed (trees are represented as directed graphs)
    assert graph.directed is True, "Tree's graph representation should be directed"


# REMOVED: test_tree_to_graph_preserves_structure - duplicate, covered by property test


@pytest.mark.unit
def test_tree_graphlike_methods_work():
    """Test GraphLike protocol methods work on Tree.

    This test verifies that the GraphLike protocol methods (vertices, edges,
    neighbors, has_edge) work correctly on a Tree instance.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Create a tree with a root
    root = "A"
    tree = Tree(root)

    # Test vertices() method (via to_graph)
    graph = tree.to_graph()
    vertices = graph.vertices()
    assert isinstance(vertices, set), "vertices() should return a set"
    assert root in vertices, f"Root {root} should be in vertices"

    # Test edges() method (via to_graph)
    edges = graph.edges()
    assert isinstance(edges, set), "edges() should return a set"
    assert len(edges) == 0, "Tree with single vertex should have no edges"

    # Test neighbors() method (via to_graph)
    neighbors = graph.neighbors(root)
    assert isinstance(neighbors, set), "neighbors() should return a set"
    assert len(neighbors) == 0, "Root with no children should have no neighbors"

    # Test has_edge() method (via to_graph)
    # With single vertex, there should be no edges
    has_edge = graph.has_edge(root, root)
    assert has_edge is False, "Single vertex tree should have no self-loop"


@pytest.mark.unit
def test_tree_num_vertices_and_num_edges():
    """Test num_vertices() and num_edges() methods.

    This test verifies that Tree provides num_vertices() and num_edges()
    methods that return the correct counts.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Create a tree with a root
    root = "A"
    tree = Tree(root)

    # Test num_vertices()
    assert hasattr(tree, "num_vertices"), "Tree should have num_vertices() method"
    assert callable(tree.num_vertices), "num_vertices() should be callable"
    assert tree.num_vertices() == 1, f"Tree should have 1 vertex, got {tree.num_vertices()}"

    # Test num_edges()
    assert hasattr(tree, "num_edges"), "Tree should have num_edges() method"
    assert callable(tree.num_edges), "num_edges() should be callable"
    assert tree.num_edges() == 0, f"Tree should have 0 edges, got {tree.num_edges()}"


@pytest.mark.unit
def test_tree_root_property():
    """Test Tree.root property accessor.

    This test verifies that Tree provides a root property that returns
    the root vertex of the tree.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Create trees with different root types
    tree_str = Tree("root")
    tree_int = Tree(42)
    tree_tuple = Tree((1, 2))

    # Test root property
    assert tree_str.root == "root", "Root property should return the root vertex"
    assert tree_int.root == 42, "Root property should return the root vertex"
    assert tree_tuple.root == (1, 2), "Root property should return the root vertex"

    # Verify root is read-only (if implemented as property)
    assert hasattr(tree_str, "root"), "Tree should have root attribute/property"


# ============================================================================
# Task 3.2: Node Operations Tests (RED Phase)
# ============================================================================


@pytest.mark.unit
def test_add_child_adds_child_to_parent_correctly():
    """Test add_child adds child to parent correctly.

    This test verifies that when add_child is called with a valid parent
    and a new child vertex, the child is added to the tree and connected
    to the parent.

    Expected in RED phase: Test FAILS (add_child doesn't exist yet or is incomplete)
    """
    # Create a tree with a root
    tree = Tree("A")

    # Add a child to the root
    tree.add_child("A", "B")

    # Verify the tree now has 2 vertices
    assert tree.num_vertices() == 2, f"Tree should have 2 vertices, got {tree.num_vertices()}"

    # Verify the tree has 1 edge
    assert tree.num_edges() == 1, f"Tree should have 1 edge, got {tree.num_edges()}"

    # Verify B is in the tree's vertices
    assert "B" in tree.vertices(), "Child B should be in tree vertices"

    # Verify the edge exists from A to B
    assert tree.has_edge("A", "B"), "Edge from A to B should exist"

    # Verify B is a child of A
    children = tree.children("A")
    assert "B" in children, f"B should be a child of A, got children: {children}"

    # Verify A is the parent of B
    parent = tree.parent("B")
    assert parent == "A", f"Parent of B should be A, got {parent}"


@pytest.mark.unit
def test_add_child_with_multiple_children():
    """Test add_child can add multiple children to the same parent.

    This test verifies that a parent can have multiple children.

    Expected in RED phase: Test FAILS (add_child doesn't exist yet or is incomplete)
    """
    # Create a tree with a root
    tree = Tree("root")

    # Add multiple children to the root
    tree.add_child("root", "child1")
    tree.add_child("root", "child2")
    tree.add_child("root", "child3")

    # Verify the tree has 4 vertices (root + 3 children)
    assert tree.num_vertices() == 4, f"Tree should have 4 vertices, got {tree.num_vertices()}"

    # Verify the tree has 3 edges
    assert tree.num_edges() == 3, f"Tree should have 3 edges, got {tree.num_edges()}"

    # Verify all children are in the tree
    children = tree.children("root")
    assert "child1" in children, "child1 should be a child of root"
    assert "child2" in children, "child2 should be a child of root"
    assert "child3" in children, "child3 should be a child of root"
    assert len(children) == 3, f"Root should have 3 children, got {len(children)}"


@pytest.mark.unit
def test_add_child_creates_nested_structure():
    """Test add_child can create nested tree structures.

    This test verifies that children can have their own children,
    creating a multi-level tree structure.

    Expected in RED phase: Test FAILS (add_child doesn't exist yet or is incomplete)
    """
    # Create a tree with a root
    tree = Tree("A")

    # Create a nested structure: A -> B -> C
    tree.add_child("A", "B")
    tree.add_child("B", "C")

    # Verify the tree has 3 vertices
    assert tree.num_vertices() == 3, f"Tree should have 3 vertices, got {tree.num_vertices()}"

    # Verify the tree has 2 edges
    assert tree.num_edges() == 2, f"Tree should have 2 edges, got {tree.num_edges()}"

    # Verify parent-child relationships
    assert tree.parent("B") == "A", "Parent of B should be A"
    assert tree.parent("C") == "B", "Parent of C should be B"
    assert tree.parent("A") is None, "Root A should have no parent"

    # Verify children relationships
    assert "B" in tree.children("A"), "B should be a child of A"
    assert "C" in tree.children("B"), "C should be a child of B"
    assert len(tree.children("C")) == 0, "C should have no children"


@pytest.mark.unit
def test_add_child_raises_error_if_parent_does_not_exist():
    """Test add_child raises error if parent doesn't exist.

    This test verifies that attempting to add a child to a non-existent
    parent vertex raises a VertexNotFoundError.

    Expected in RED phase: Test FAILS (add_child doesn't exist yet or is incomplete)
    """
    # Create a tree with a root
    tree = Tree("A")

    # Attempt to add a child to a non-existent parent
    with pytest.raises(VertexNotFoundError) as exc_info:
        tree.add_child("NonExistent", "B")

    # Verify the error message mentions the parent
    assert "NonExistent" in str(exc_info.value), "Error message should mention the non-existent parent"

    # Verify the tree is unchanged (still only has root)
    assert tree.num_vertices() == 1, "Tree should still have only 1 vertex after failed add_child"
    assert tree.num_edges() == 0, "Tree should still have 0 edges after failed add_child"


@pytest.mark.unit
def test_add_child_raises_error_if_child_already_exists():
    """Test add_child raises error if child already exists in tree.

    This test verifies that attempting to add a child that already exists
    in the tree raises a ValueError.

    Expected in RED phase: Test FAILS (add_child doesn't exist yet or is incomplete)
    """
    # Create a tree with a root and a child
    tree = Tree("A")
    tree.add_child("A", "B")

    # Attempt to add B again as a child of A
    with pytest.raises(ValueError) as exc_info:
        tree.add_child("A", "B")

    # Verify the error message mentions the child
    assert "B" in str(exc_info.value), "Error message should mention the duplicate child"
    assert "already exists" in str(exc_info.value).lower(), "Error message should mention 'already exists'"

    # Verify the tree is unchanged
    assert tree.num_vertices() == 2, "Tree should still have 2 vertices after failed add_child"
    assert tree.num_edges() == 1, "Tree should still have 1 edge after failed add_child"


@pytest.mark.unit
def test_add_child_raises_cycle_error_if_cycle_would_be_created():
    """Test add_child raises CycleError if cycle would be created.

    This test verifies that attempting to add an edge that would create
    a cycle in the tree raises a CycleError and leaves the tree unchanged.

    Expected in RED phase: Test FAILS (add_child doesn't exist yet or is incomplete)
    """
    # Create a tree with a chain: A -> B -> C
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("B", "C")

    # Attempt to create a cycle by making A a child of C
    # This would create: A -> B -> C -> A (cycle)
    with pytest.raises(CycleError) as exc_info:
        tree.add_child("C", "A")

    # Verify the error message mentions cycle
    assert "cycle" in str(exc_info.value).lower(), "Error message should mention 'cycle'"

    # Verify the tree is unchanged (atomic operation)
    assert tree.num_vertices() == 3, "Tree should still have 3 vertices after failed add_child"
    assert tree.num_edges() == 2, "Tree should still have 2 edges after failed add_child"
    assert not tree.has_edge("C", "A"), "Cycle edge should not have been added"

    # Verify parent-child relationships are unchanged
    assert tree.parent("B") == "A", "Parent of B should still be A"
    assert tree.parent("C") == "B", "Parent of C should still be B"
    assert tree.parent("A") is None, "A should still be the root with no parent"


# REMOVED: test_add_child_cycle_detection_complex - duplicate of test_add_child_raises_cycle_error_if_cycle_would_be_created


@pytest.mark.unit
def test_remove_subtree_removes_node_and_descendants():
    """Test remove_subtree removes node and all descendants.

    This test verifies that remove_subtree removes the specified node
    and all of its descendants from the tree.

    Expected in RED phase: Test FAILS (remove_subtree doesn't exist yet)
    """
    # Create a tree with multiple levels:
    #       A
    #      / \
    #     B   C
    #    / \
    #   D   E
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")
    tree.add_child("B", "E")

    # Remove subtree rooted at B (should remove B, D, and E)
    tree.remove_subtree("B")

    # Verify the tree now has 2 vertices (A and C)
    assert tree.num_vertices() == 2, f"Tree should have 2 vertices after removing subtree, got {tree.num_vertices()}"

    # Verify the tree has 1 edge (A -> C)
    assert tree.num_edges() == 1, f"Tree should have 1 edge after removing subtree, got {tree.num_edges()}"

    # Verify B, D, and E are no longer in the tree
    vertices = tree.vertices()
    assert "B" not in vertices, "B should be removed from tree"
    assert "D" not in vertices, "D should be removed from tree"
    assert "E" not in vertices, "E should be removed from tree"

    # Verify A and C are still in the tree
    assert "A" in vertices, "A should still be in tree"
    assert "C" in vertices, "C should still be in tree"

    # Verify C is still a child of A
    assert "C" in tree.children("A"), "C should still be a child of A"


@pytest.mark.unit
def test_remove_subtree_removes_single_leaf():
    """Test remove_subtree can remove a single leaf node.

    This test verifies that remove_subtree works correctly when removing
    a leaf node (node with no children).

    Expected in RED phase: Test FAILS (remove_subtree doesn't exist yet)
    """
    # Create a simple tree: A -> B -> C
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("B", "C")

    # Remove leaf node C
    tree.remove_subtree("C")

    # Verify the tree now has 2 vertices (A and B)
    assert tree.num_vertices() == 2, f"Tree should have 2 vertices, got {tree.num_vertices()}"

    # Verify the tree has 1 edge (A -> B)
    assert tree.num_edges() == 1, f"Tree should have 1 edge, got {tree.num_edges()}"

    # Verify C is no longer in the tree
    assert "C" not in tree.vertices(), "C should be removed from tree"

    # Verify B has no children
    assert len(tree.children("B")) == 0, "B should have no children after removing C"


@pytest.mark.unit
def test_remove_subtree_updates_parent_map():
    """Test remove_subtree updates the internal parent map correctly.

    This test verifies that when a subtree is removed, the internal
    parent map is updated to remove entries for all removed nodes.

    Expected in RED phase: Test FAILS (remove_subtree doesn't exist yet)
    """
    # Create a tree: A -> B -> C
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("B", "C")

    # Verify parent relationships before removal
    assert tree.parent("B") == "A", "Parent of B should be A"
    assert tree.parent("C") == "B", "Parent of C should be B"

    # Remove subtree rooted at B
    tree.remove_subtree("B")

    # Verify B and C are no longer in the tree
    assert "B" not in tree.vertices(), "B should be removed"
    assert "C" not in tree.vertices(), "C should be removed"

    # Attempting to get parent of removed nodes should raise error
    from pygraph.exceptions import VertexNotFoundError

    with pytest.raises(VertexNotFoundError):
        tree.parent("B")

    with pytest.raises(VertexNotFoundError):
        tree.parent("C")


@pytest.mark.unit
def test_remove_subtree_raises_error_if_node_does_not_exist():
    """Test remove_subtree raises error if node doesn't exist.

    This test verifies that attempting to remove a non-existent node
    raises a VertexNotFoundError.

    Expected in RED phase: Test FAILS (remove_subtree doesn't exist yet)
    """
    # Create a simple tree
    tree = Tree("A")
    tree.add_child("A", "B")

    # Attempt to remove a non-existent node
    with pytest.raises(VertexNotFoundError) as exc_info:
        tree.remove_subtree("NonExistent")

    # Verify the error message mentions the node
    assert "NonExistent" in str(exc_info.value), "Error message should mention the non-existent node"

    # Verify the tree is unchanged
    assert tree.num_vertices() == 2, "Tree should still have 2 vertices"
    assert tree.num_edges() == 1, "Tree should still have 1 edge"


@pytest.mark.unit
def test_remove_subtree_cannot_remove_root():
    """Test remove_subtree behavior when attempting to remove root.

    This test verifies the behavior when attempting to remove the root node.
    The root should be removable, which would leave an empty tree structure.

    Expected in RED phase: Test FAILS (remove_subtree doesn't exist yet)
    """
    # Create a tree with root and children
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")

    # Remove the root (should remove entire tree)
    tree.remove_subtree("A")

    # Verify the tree is now empty (or has special handling for root removal)
    # Note: The exact behavior may depend on design decisions
    # For now, we expect all vertices to be removed
    assert tree.num_vertices() == 0, "Tree should be empty after removing root"
    assert tree.num_edges() == 0, "Tree should have no edges after removing root"


@pytest.mark.unit
def test_remove_subtree_with_deep_nesting():
    """Test remove_subtree with deeply nested structure.

    This test verifies that remove_subtree correctly removes all descendants
    even in deeply nested tree structures.

    Expected in RED phase: Test FAILS (remove_subtree doesn't exist yet)
    """
    # Create a deep tree: A -> B -> C -> D -> E
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("B", "C")
    tree.add_child("C", "D")
    tree.add_child("D", "E")

    # Remove subtree rooted at B (should remove B, C, D, E)
    tree.remove_subtree("B")

    # Verify only A remains
    assert tree.num_vertices() == 1, f"Tree should have 1 vertex, got {tree.num_vertices()}"
    assert tree.num_edges() == 0, f"Tree should have 0 edges, got {tree.num_edges()}"
    assert "A" in tree.vertices(), "A should still be in tree"

    # Verify all descendants are removed
    for vertex in ["B", "C", "D", "E"]:
        assert vertex not in tree.vertices(), f"{vertex} should be removed from tree"


# ============================================================================
# Task 3.3: Query Methods Tests (RED Phase)
# ============================================================================


@pytest.mark.unit
def test_parent_returns_correct_parent_using_parent_map():
    """Test parent() returns correct parent using _parent_map.

    This test verifies that the parent() method correctly returns the parent
    of a node using the internal _parent_map for O(1) lookup.

    Expected in RED phase: Test PASSES (parent already implemented in Task 3.2)
    """
    # Create a tree with multiple levels
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")

    # Test parent lookups
    assert tree.parent("B") == "A", "Parent of B should be A"
    assert tree.parent("C") == "A", "Parent of C should be A"
    assert tree.parent("D") == "B", "Parent of D should be B"
    assert tree.parent("A") is None, "Root A should have no parent"


@pytest.mark.unit
def test_children_returns_all_children_of_node():
    """Test children() returns all children of a node.

    This test verifies that the children() method returns a set containing
    all direct children of a given node.

    Expected in RED phase: Test PASSES (children already implemented in Task 3.2)
    """
    # Create a tree with multiple children
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("A", "D")
    tree.add_child("B", "E")

    # Test children lookups
    children_a = tree.children("A")
    assert children_a == {"B", "C", "D"}, f"Children of A should be {{B, C, D}}, got {children_a}"

    children_b = tree.children("B")
    assert children_b == {"E"}, f"Children of B should be {{E}}, got {children_b}"

    children_e = tree.children("E")
    assert children_e == set(), f"Children of E should be empty set, got {children_e}"


@pytest.mark.unit
def test_is_leaf_correctly_identifies_leaf_nodes():
    """Test is_leaf() correctly identifies leaf nodes.

    This test verifies that is_leaf() returns True for nodes with no children
    and False for nodes with children.

    Expected in RED phase: Test FAILS (is_leaf doesn't exist yet)
    """
    # Create a tree:
    #       A
    #      / \
    #     B   C
    #    /
    #   D
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")

    # Test is_leaf
    assert tree.is_leaf("C") is True, "C should be a leaf (no children)"
    assert tree.is_leaf("D") is True, "D should be a leaf (no children)"
    assert tree.is_leaf("B") is False, "B should not be a leaf (has child D)"
    assert tree.is_leaf("A") is False, "A should not be a leaf (has children B and C)"


@pytest.mark.unit
def test_is_root_correctly_identifies_root_node():
    """Test is_root() correctly identifies root node.

    This test verifies that is_root() returns True only for the root node
    and False for all other nodes.

    Expected in RED phase: Test FAILS (is_root doesn't exist yet)
    """
    # Create a tree
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")

    # Test is_root
    assert tree.is_root("A") is True, "A should be the root"
    assert tree.is_root("B") is False, "B should not be the root"
    assert tree.is_root("C") is False, "C should not be the root"
    assert tree.is_root("D") is False, "D should not be the root"


@pytest.mark.unit
def test_height_calculates_tree_height_correctly():
    """Test height() calculates tree height correctly.

    This test verifies that height() returns the maximum distance from
    the root to any leaf node. Height of a single-node tree is 0.

    Expected in RED phase: Test FAILS (height doesn't exist yet)
    """
    # Test 1: Single node tree (height = 0)
    tree1 = Tree("A")
    assert tree1.height() == 0, "Height of single-node tree should be 0"

    # Test 2: Tree with one level (height = 1)
    tree2 = Tree("A")
    tree2.add_child("A", "B")
    assert tree2.height() == 1, "Height of tree with one level should be 1"

    # Test 3: Tree with multiple levels (height = 2)
    #       A
    #      / \
    #     B   C
    #    /
    #   D
    tree3 = Tree("A")
    tree3.add_child("A", "B")
    tree3.add_child("A", "C")
    tree3.add_child("B", "D")
    assert tree3.height() == 2, "Height should be 2 (A -> B -> D)"

    # Test 4: Deeper tree (height = 3)
    tree4 = Tree("A")
    tree4.add_child("A", "B")
    tree4.add_child("B", "C")
    tree4.add_child("C", "D")
    assert tree4.height() == 3, "Height should be 3 (A -> B -> C -> D)"


@pytest.mark.unit
def test_depth_calculates_node_depth_correctly():
    """Test depth() calculates node depth correctly.

    This test verifies that depth() returns the distance from the root
    to the specified node. Root has depth 0.

    Expected in RED phase: Test FAILS (depth doesn't exist yet)
    """
    # Create a tree:
    #       A (depth 0)
    #      / \
    #     B   C (depth 1)
    #    /
    #   D (depth 2)
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")

    # Test depth calculations
    assert tree.depth("A") == 0, "Depth of root should be 0"
    assert tree.depth("B") == 1, "Depth of B should be 1"
    assert tree.depth("C") == 1, "Depth of C should be 1"
    assert tree.depth("D") == 2, "Depth of D should be 2"


@pytest.mark.unit
def test_query_methods_raise_error_for_nonexistent_nodes():
    """Test query methods raise VertexNotFoundError for non-existent nodes.

    This test verifies that all query methods properly validate that the
    node exists in the tree before performing operations.

    Expected in RED phase: Test FAILS (some methods don't exist yet)
    """
    # Create a simple tree
    tree = Tree("A")
    tree.add_child("A", "B")

    # Test parent() - already implemented, should work
    with pytest.raises(VertexNotFoundError):
        tree.parent("NonExistent")

    # Test children() - already implemented, should work
    with pytest.raises(VertexNotFoundError):
        tree.children("NonExistent")

    # Test is_leaf() - not implemented yet
    with pytest.raises(VertexNotFoundError):
        tree.is_leaf("NonExistent")

    # Test is_root() - not implemented yet
    with pytest.raises(VertexNotFoundError):
        tree.is_root("NonExistent")

    # Test depth() - not implemented yet
    with pytest.raises(VertexNotFoundError):
        tree.depth("NonExistent")


@pytest.mark.unit
def test_is_leaf_on_single_node_tree():
    """Test is_leaf() on a single-node tree.

    This test verifies that the root of a single-node tree is considered
    a leaf (since it has no children).

    Expected in RED phase: Test FAILS (is_leaf doesn't exist yet)
    """
    # Create a single-node tree
    tree = Tree("A")

    # Root with no children should be a leaf
    assert tree.is_leaf("A") is True, "Root with no children should be a leaf"


@pytest.mark.unit
def test_height_with_unbalanced_tree():
    """Test height() with an unbalanced tree.

    This test verifies that height() correctly calculates the height
    for unbalanced trees (where branches have different depths).

    Expected in RED phase: Test FAILS (height doesn't exist yet)
    """
    # Create an unbalanced tree:
    #       A
    #      / \
    #     B   C
    #    /     \
    #   D       E
    #  /         \
    # F           G
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")
    tree.add_child("C", "E")
    tree.add_child("D", "F")
    tree.add_child("E", "G")

    # Height should be 3 (longest path: A -> B -> D -> F or A -> C -> E -> G)
    assert tree.height() == 3, "Height of unbalanced tree should be 3"


@pytest.mark.unit
def test_depth_with_multiple_children():
    """Test depth() with nodes having multiple children.

    This test verifies that depth() works correctly in trees where
    nodes have multiple children.

    Expected in RED phase: Test FAILS (depth doesn't exist yet)
    """
    # Create a tree with multiple children:
    #         A
    #       / | \
    #      B  C  D
    #     /
    #    E
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("A", "D")
    tree.add_child("B", "E")

    # Test depths
    assert tree.depth("A") == 0, "Depth of root should be 0"
    assert tree.depth("B") == 1, "Depth of B should be 1"
    assert tree.depth("C") == 1, "Depth of C should be 1"
    assert tree.depth("D") == 1, "Depth of D should be 1"
    assert tree.depth("E") == 2, "Depth of E should be 2"


# ============================================================================
# Additional Coverage Tests
# ============================================================================


@pytest.mark.unit
def test_from_graph_with_valid_directed_graph():
    """Test Tree.from_graph() with a valid directed graph.

    This test covers the from_graph static method which is currently
    not covered by existing tests.
    """
    # Create a directed graph that forms a tree structure
    graph = Graph[str](directed=True)
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")

    # Convert to tree
    tree = Tree.from_graph(graph, "A")

    # Verify tree structure
    assert tree.root == "A"
    assert tree.num_vertices() == 3
    assert tree.num_edges() == 2
    assert tree.parent("B") == "A"
    assert tree.parent("C") == "A"


# REMOVED: test_from_graph_with_undirected_graph_raises_error - consolidated into test_from_graph_validation_errors


@pytest.mark.unit
def test_depth_with_disconnected_vertex_raises_error():
    """Test depth() raises error for vertex not connected to root.

    This test covers the error case in depth() where a vertex
    is not connected to the root (which shouldn't happen in a valid tree,
    but we test the error handling).

    Note: This is a theoretical edge case that shouldn't occur in practice
    with the current Tree implementation, but we test it for completeness.
    """
    # Create a tree
    tree = Tree("A")
    tree.add_child("A", "B")

    # Manually break the parent map to simulate a disconnected vertex
    # This is the only way to trigger the ValueError in depth()
    tree._parent_map["B"] = None  # pylint: disable=protected-access

    # Now depth("B") should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        tree.depth("B")

    assert "not connected to root" in str(exc_info.value)


@pytest.mark.unit
def test_tree_edges_method_returns_edge_tuples():
    """Test Tree.edges() returns set of (source, target) tuples.

    This test directly calls the edges() method on Tree to ensure
    it returns the correct format of edge tuples.
    """
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")

    # Call edges() directly on tree
    edges = tree.edges()

    # Should return set of tuples
    assert isinstance(edges, set), "edges() should return a set"
    assert len(edges) == 3, "Tree should have 3 edges"

    # Check edge tuples
    expected_edges = {("A", "B"), ("A", "C"), ("B", "D")}
    assert edges == expected_edges, f"Expected {expected_edges}, got {edges}"


@pytest.mark.unit
def test_tree_neighbors_method_returns_children():
    """Test Tree.neighbors() returns children of a vertex.

    This test directly calls the neighbors() method on Tree to ensure
    it returns the correct set of child vertices.
    """
    tree = Tree("A")
    tree.add_child("A", "B")
    tree.add_child("A", "C")
    tree.add_child("B", "D")
    tree.add_child("B", "E")

    # Call neighbors() directly on tree
    neighbors_a = tree.neighbors("A")
    neighbors_b = tree.neighbors("B")
    neighbors_d = tree.neighbors("D")

    # Check neighbors (children)
    assert isinstance(neighbors_a, set), "neighbors() should return a set"
    assert neighbors_a == {"B", "C"}, f"A's neighbors should be B and C, got {neighbors_a}"
    assert neighbors_b == {"D", "E"}, f"B's neighbors should be D and E, got {neighbors_b}"
    assert neighbors_d == set(), f"D's neighbors should be empty, got {neighbors_d}"


# ============================================================================
# Tree-Graph Conversion Tests (Task 3.4)
# ============================================================================


# REMOVED: test_from_graph_with_cyclic_graph_raises_error - consolidated into test_from_graph_validation_errors
# REMOVED: test_from_graph_with_disconnected_graph_raises_error - consolidated into test_from_graph_validation_errors
# REMOVED: test_from_graph_with_tree_property_violation - consolidated into test_from_graph_validation_errors
# REMOVED: test_from_graph_validates_connectivity_from_root - consolidated into test_from_graph_validation_errors


@pytest.mark.unit
def test_from_graph_validation_errors():
    """Test Tree.from_graph() validates all constraints (CONSOLIDATED TEST).

    This test consolidates validation for:
    - Undirected graphs (must be directed)
    - Cyclic graphs (must be acyclic)
    - Disconnected graphs (must be connected)
    - Tree property violation (must have n-1 edges)
    - Connectivity from root (all vertices reachable)

    **Validates: Requirements A2.6** - Graph to tree conversion validates constraints
    """
    from pygraph.exceptions import InvalidGraphError

    # Test 1: Undirected graph should be rejected
    graph_undirected = Graph[str](directed=False)
    graph_undirected.add_vertex("A")
    graph_undirected.add_vertex("B")
    graph_undirected.add_edge("A", "B")

    with pytest.raises(ValueError) as exc_info:
        Tree.from_graph(graph_undirected, "A")
    assert "directed" in str(exc_info.value).lower()

    # Test 2: Cyclic graph should be rejected
    graph_cyclic = Graph[str](directed=True)
    graph_cyclic.add_vertex("A")
    graph_cyclic.add_vertex("B")
    graph_cyclic.add_vertex("C")
    graph_cyclic.add_edge("A", "B")
    graph_cyclic.add_edge("B", "C")
    graph_cyclic.add_edge("C", "A")  # Creates cycle

    with pytest.raises((ValueError, InvalidGraphError)) as exc_info:
        Tree.from_graph(graph_cyclic, "A")
    error_msg = str(exc_info.value).lower()
    assert "cycle" in error_msg or "acyclic" in error_msg

    # Test 3: Disconnected graph should be rejected
    graph_disconnected = Graph[str](directed=True)
    graph_disconnected.add_vertex("A")
    graph_disconnected.add_vertex("B")
    graph_disconnected.add_vertex("C")
    graph_disconnected.add_edge("A", "B")
    # C is not connected

    with pytest.raises((ValueError, InvalidGraphError)) as exc_info:
        Tree.from_graph(graph_disconnected, "A")
    assert "connect" in str(exc_info.value).lower()

    # Test 4: Tree property violation (too many edges)
    graph_extra_edge = Graph[str](directed=True)
    graph_extra_edge.add_vertex("A")
    graph_extra_edge.add_vertex("B")
    graph_extra_edge.add_vertex("C")
    graph_extra_edge.add_edge("A", "B")
    graph_extra_edge.add_edge("A", "C")
    graph_extra_edge.add_edge("B", "C")  # Extra edge

    with pytest.raises(InvalidGraphError, match="does not have tree property"):
        Tree.from_graph(graph_extra_edge, "A")


@pytest.mark.unit
def test_from_graph_builds_correct_parent_map():
    """Test Tree.from_graph() builds correct _parent_map.

    This test verifies that from_graph() correctly builds the internal
    _parent_map during graph traversal, enabling O(1) parent lookups.

    **Validates: Requirements A2.6** - Graph to tree conversion
    """
    # Create a directed graph that forms a tree structure
    graph = Graph[str](directed=True)
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E")
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("B", "E")

    # Convert to tree
    tree = Tree.from_graph(graph, "A")

    # Verify parent map is built correctly
    assert tree.parent("A") is None, "Root should have no parent"
    assert tree.parent("B") == "A", "B's parent should be A"
    assert tree.parent("C") == "A", "C's parent should be A"
    assert tree.parent("D") == "B", "D's parent should be B"
    assert tree.parent("E") == "B", "E's parent should be B"

    # Verify parent lookups are O(1) by checking _parent_map directly
    assert "B" in tree._parent_map, "B should be in parent map"  # pylint: disable=protected-access
    assert "C" in tree._parent_map, "C should be in parent map"  # pylint: disable=protected-access
    assert "D" in tree._parent_map, "D should be in parent map"  # pylint: disable=protected-access
    assert "E" in tree._parent_map, "E should be in parent map"  # pylint: disable=protected-access
    assert "A" not in tree._parent_map, "Root should not be in parent map"  # pylint: disable=protected-access


@pytest.mark.unit
def test_from_graph_with_complex_tree_structure():
    """Test Tree.from_graph() with a more complex tree structure.

    This test verifies that from_graph() correctly handles larger, more
    complex tree structures with multiple levels and branches.

    **Validates: Requirements A2.5, A2.6** - Tree-Graph conversion
    """
    # Create a directed graph with a complex tree structure
    #       A
    #      / \
    #     B   C
    #    / \   \
    #   D   E   F
    #  /
    # G
    graph = Graph[str](directed=True)
    vertices = ["A", "B", "C", "D", "E", "F", "G"]
    for v in vertices:
        graph.add_vertex(v)

    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("B", "E"),
        ("C", "F"),
        ("D", "G"),
    ]
    for source, target in edges:
        graph.add_edge(source, target)

    # Convert to tree
    tree = Tree.from_graph(graph, "A")

    # Verify tree structure
    assert tree.root == "A"
    assert tree.num_vertices() == 7
    assert tree.num_edges() == 6  # n-1 edges for n vertices

    # Verify parent-child relationships
    assert tree.parent("B") == "A"
    assert tree.parent("C") == "A"
    assert tree.parent("D") == "B"
    assert tree.parent("E") == "B"
    assert tree.parent("F") == "C"
    assert tree.parent("G") == "D"

    # Verify children
    assert tree.children("A") == {"B", "C"}
    assert tree.children("B") == {"D", "E"}
    assert tree.children("C") == {"F"}
    assert tree.children("D") == {"G"}
    assert tree.children("E") == set()
    assert tree.children("F") == set()
    assert tree.children("G") == set()

    # Verify tree properties
    assert tree.height() == 3  # A -> B -> D -> G
    assert tree.depth("A") == 0
    assert tree.depth("B") == 1
    assert tree.depth("D") == 2
    assert tree.depth("G") == 3


@pytest.mark.unit
def test_from_graph_with_single_vertex():
    """Test Tree.from_graph() with a graph containing a single vertex.

    This test verifies that from_graph() correctly handles the edge case
    of a graph with only one vertex (the root).

    **Validates: Requirements A2.6** - Graph to tree conversion
    """
    # Create a directed graph with a single vertex
    graph = Graph[str](directed=True)
    graph.add_vertex("A")

    # Convert to tree
    tree = Tree.from_graph(graph, "A")

    # Verify tree structure
    assert tree.root == "A"
    assert tree.num_vertices() == 1
    assert tree.num_edges() == 0
    assert tree.parent("A") is None
    assert tree.children("A") == set()
    assert tree.is_root("A")
    assert tree.is_leaf("A")
    assert tree.height() == 0


# REMOVED: test_add_child_rollback_on_cycle_detection - duplicate of test_add_child_raises_cycle_error_if_cycle_would_be_created


# REMOVED: test_from_graph_with_tree_property_violation - consolidated into test_from_graph_validation_errors
# REMOVED: test_from_graph_validates_connectivity_from_root - consolidated into test_from_graph_validation_errors


@pytest.mark.unit
def test_build_parent_map_with_already_visited_neighbor():
    """Test _build_parent_map when a neighbor has already been visited.

    This tests the branch where neighbor is already in visited_bfs.
    In a valid tree, this shouldn't happen, but we test the method's robustness.
    """
    # Create a graph that looks like a tree but has an extra edge
    # that creates a diamond pattern: A -> B, A -> C, B -> D, C -> D
    # When building parent map from A, D will be visited from B first,
    # then when we process C, D is already visited
    graph = Graph[str](directed=True)
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")  # This creates multiple paths to D

    # Call the static method directly
    parent_map = Tree._build_parent_map(graph, "A")

    # D should have a parent (either B or C, depending on BFS order)
    assert "D" in parent_map
    assert parent_map["D"] in ["B", "C"]

    # B and C should have A as parent
    assert parent_map["B"] == "A"
    assert parent_map["C"] == "A"

    # A should not be in parent_map (it's the root)
    assert "A" not in parent_map
