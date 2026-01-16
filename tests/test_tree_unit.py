"""Unit tests for Tree class.

This module contains unit tests that verify specific examples, edge cases,
and error conditions for the Tree class. These tests complement the
property-based tests by focusing on concrete scenarios.

These tests follow the TDD methodology:
- RED phase: Tests are written first and should FAIL (Tree class doesn't exist yet)
- GREEN phase: Implement Tree class to make tests pass
- REFACTOR phase: Improve implementation while keeping tests green
"""

import pytest


@pytest.mark.unit
def test_tree_initialization_with_root():
    """Test Tree(root) creates tree with single root vertex.

    This test verifies that when a Tree is created with a root vertex,
    the tree is initialized with that single vertex and no edges.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Import Tree class (will fail in RED phase)
    try:
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

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
    # Import Tree class (will fail in RED phase)
    try:
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

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
    # Import Tree class and GraphLike protocol (will fail in RED phase)
    try:
        from pygraph.protocols import GraphLike
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class or GraphLike protocol not implemented yet (expected in RED phase)")

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
    # Import Tree and Graph classes (will fail in RED phase)
    try:
        from pygraph.graph import Graph
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

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


@pytest.mark.unit
def test_tree_to_graph_preserves_structure():
    """Test to_graph() preserves tree structure with multiple vertices.

    This test verifies that when a tree has multiple vertices and edges,
    the to_graph() method returns a graph with the same structure.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    Note: This test will be more meaningful after add_child is implemented,
    but we include it now to verify the basic structure.
    """
    # Import Tree class (will fail in RED phase)
    try:
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

    # Create a tree with a root
    root = "A"
    tree = Tree(root)

    # Get the graph representation
    graph = tree.to_graph()

    # Verify basic properties
    assert graph.directed is True, "Tree's graph representation should be directed"
    assert root in graph.vertices(), f"Graph should contain root vertex {root}"

    # Verify num_vertices and num_edges are consistent
    assert tree.num_vertices() == len(graph.vertices()), "Tree and graph should have same vertex count"
    assert tree.num_edges() == len(graph.edges()), "Tree and graph should have same edge count"


@pytest.mark.unit
def test_tree_graphlike_methods_work():
    """Test GraphLike protocol methods work on Tree.

    This test verifies that the GraphLike protocol methods (vertices, edges,
    neighbors, has_edge) work correctly on a Tree instance.

    Expected in RED phase: Test FAILS (Tree class doesn't exist yet)
    """
    # Import Tree class (will fail in RED phase)
    try:
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

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
    # Import Tree class (will fail in RED phase)
    try:
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

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
    # Import Tree class (will fail in RED phase)
    try:
        from pygraph.tree import Tree
    except ImportError:
        pytest.fail("Tree class not implemented yet (expected in RED phase)")

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
