"""Unit tests for Graph class.

This module contains unit tests that verify specific examples, edge cases,
and error conditions for the Graph class. These tests complement the
property-based tests by focusing on concrete scenarios.

These tests follow the TDD methodology:
- RED phase: Tests are written first and should FAIL (Graph class doesn't exist yet)
- GREEN phase: Implement Graph class to make tests pass
- REFACTOR phase: Improve implementation while keeping tests green
"""

import pytest

from pygraph.exceptions import EdgeNotFoundError, VertexNotFoundError
from pygraph.graph import Graph


@pytest.mark.unit
@pytest.mark.parametrize(
    "directed,weighted,representation",
    [
        (True, True, "adjacency_list"),
        (False, True, "adjacency_list"),
        (True, False, "adjacency_list"),
        (False, False, "adjacency_list"),
        (True, True, "adjacency_matrix"),
        (False, True, "adjacency_matrix"),
        (True, False, "adjacency_matrix"),
        (False, False, "adjacency_matrix"),
    ],
    ids=[
        "directed_weighted_list",
        "undirected_weighted_list",
        "directed_unweighted_list",
        "undirected_unweighted_list",
        "directed_weighted_matrix",
        "undirected_weighted_matrix",
        "directed_unweighted_matrix",
        "undirected_unweighted_matrix",
    ],
)
def test_graph_initialization(directed, weighted, representation):
    """Test Graph initialization with various parameter combinations (consolidated test)."""
    graph = Graph(directed=directed, weighted=weighted, representation=representation)

    # Verify all parameters are set correctly through public interface
    assert graph.directed is directed, f"Graph should be {'directed' if directed else 'undirected'}"
    assert graph.weighted is weighted, f"Graph should be {'weighted' if weighted else 'unweighted'}"
    assert graph.representation == representation, f"Graph should use {representation} representation"


@pytest.mark.unit
def test_graph_initialization_defaults():
    """Test that Graph() uses default parameters correctly."""
    graph = Graph()

    # Verify default parameters based on design document through public interface
    # Default: undirected, weighted, adjacency_list
    assert graph.directed is False, "Default graph should be undirected"
    assert graph.weighted is True, "Default graph should be weighted"
    assert graph.representation == "adjacency_list", "Default graph should use adjacency list"


@pytest.mark.unit
def test_graph_initialization_invalid_representation():
    """Test that Graph raises ValueError for invalid representation."""
    with pytest.raises(ValueError, match="Invalid representation 'invalid'"):
        Graph(representation="invalid")


@pytest.mark.unit
def test_graph_properties():
    """Test Graph property accessors."""
    graph = Graph(directed=True, weighted=False, representation="adjacency_matrix")

    # Test property accessors
    assert graph.directed is True
    assert graph.weighted is False
    assert graph.representation == "adjacency_matrix"


@pytest.mark.unit
def test_graph_add_vertex_success():
    """Test successfully adding vertices."""
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex(42)

    # Check vertices were added through public interface
    vertices = graph.vertices()
    assert "A" in vertices
    assert "B" in vertices
    assert 42 in vertices
    assert len(vertices) == 3


@pytest.mark.unit
def test_graph_add_vertex_idempotent():
    """Test that adding the same vertex multiple times is idempotent."""
    graph = Graph()

    # Add same vertex multiple times
    graph.add_vertex("A")
    graph.add_vertex("A")
    graph.add_vertex("A")

    # Should only have one vertex
    vertices = graph.vertices()
    assert vertices == {"A"}
    assert len(vertices) == 1


@pytest.mark.unit
def test_graph_add_vertex_non_hashable():
    """Test that adding non-hashable vertex raises TypeError."""
    graph = Graph()

    # Test various non-hashable types with detailed error checking
    non_hashable_values = [
        [1, 2, 3],  # list
        {"key": "value"},  # dict
        {1, 2, 3},  # set
    ]

    for non_hashable_value in non_hashable_values:
        with pytest.raises(TypeError, match="Vertex must be hashable"):
            graph.add_vertex(non_hashable_value)

        # Verify graph state is unchanged after each failed attempt
        assert graph.vertices() == set()
        assert graph.num_vertices() == 0


@pytest.mark.unit
def test_graph_empty_state():
    """Test that new graph starts in empty state."""
    graph = Graph()

    # Check empty state through public interface
    assert graph.vertices() == set()
    assert graph.edges() == set()
    assert graph.num_vertices() == 0
    assert graph.num_edges() == 0


@pytest.mark.unit
def test_graph_to_graph_protocol():
    """Test GraphLike protocol implementation."""
    graph = Graph()

    # to_graph should return self
    result = graph.to_graph()
    assert result is graph


@pytest.mark.unit
@pytest.mark.parametrize(
    "representation,vertices",
    [
        ("adjacency_list", ["X", "Y"]),
        ("adjacency_matrix", ["P", "Q"]),
    ],
    ids=["adjacency_list", "adjacency_matrix"],
)
def test_graph_with_representation(representation, vertices):
    """Test Graph functionality with different representations (consolidated test)."""
    graph = Graph(representation=representation)

    # Add vertices and check through public interface
    for vertex in vertices:
        graph.add_vertex(vertex)

    assert graph.num_vertices() == len(vertices)
    for vertex in vertices:
        assert vertex in graph.vertices()


@pytest.mark.unit
def test_graph_create_representation_method():
    """Test the _create_representation method indirectly through public interface."""
    # Test adjacency list creation
    graph1 = Graph(representation="adjacency_list", directed=True)
    assert graph1.representation == "adjacency_list"
    assert graph1.directed is True

    # Test adjacency matrix creation
    graph2 = Graph(representation="adjacency_matrix", directed=False)
    assert graph2.representation == "adjacency_matrix"
    assert graph2.directed is False


@pytest.mark.unit
def test_graph_remove_vertex_success():
    """Test successfully removing vertices."""
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    # Remove a vertex
    graph.remove_vertex("B")

    # Check vertex was removed
    vertices = graph.vertices()
    assert "A" in vertices
    assert "B" not in vertices
    assert "C" in vertices
    assert len(vertices) == 2


@pytest.mark.unit
def test_graph_remove_vertex_nonexistent():
    """Test that removing non-existent vertex raises VertexNotFoundError."""
    graph = Graph()
    graph.add_vertex("A")

    # Try to remove non-existent vertex
    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found in graph"):
        graph.remove_vertex("nonexistent")

    # Verify graph state is unchanged
    assert graph.vertices() == {"A"}
    assert graph.num_vertices() == 1


@pytest.mark.unit
def test_graph_remove_vertex_from_empty_graph():
    """Test that removing vertex from empty graph raises VertexNotFoundError."""
    graph = Graph()

    # Try to remove vertex from empty graph
    with pytest.raises(VertexNotFoundError, match="Vertex 'X' not found in graph"):
        graph.remove_vertex("X")

    # Verify graph remains empty
    assert graph.vertices() == set()
    assert graph.num_vertices() == 0


@pytest.mark.unit
def test_graph_vertex_operations_atomic():
    """Test that vertex operations are atomic (rollback on failure)."""
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")

    initial_vertices = graph.vertices().copy()
    initial_count = graph.num_vertices()

    # Try to remove non-existent vertex - should not change graph state
    with pytest.raises(VertexNotFoundError):
        graph.remove_vertex("nonexistent")

    # Verify graph state is unchanged (atomic operation)
    assert graph.vertices() == initial_vertices
    assert graph.num_vertices() == initial_count


@pytest.mark.unit
def test_graph_vertex_operations_edge_cases():
    """Test edge cases for vertex operations."""
    graph = Graph()

    # Test adding and removing the same vertex multiple times
    graph.add_vertex("X")
    assert graph.num_vertices() == 1

    # Remove it
    graph.remove_vertex("X")
    assert graph.num_vertices() == 0

    # Add it again
    graph.add_vertex("X")
    assert graph.num_vertices() == 1
    assert "X" in graph.vertices()

    # Remove it again
    graph.remove_vertex("X")
    assert graph.num_vertices() == 0
    assert graph.vertices() == set()


@pytest.mark.unit
def test_graph_vertex_operations_with_different_types():
    """Test vertex operations with different hashable types."""
    graph = Graph()

    # Test with different hashable types
    vertices = ["string", 42, (1, 2), frozenset([1, 2, 3])]

    # Add all vertices
    for vertex in vertices:
        graph.add_vertex(vertex)

    assert graph.num_vertices() == len(vertices)
    for vertex in vertices:
        assert vertex in graph.vertices()

    # Remove all vertices
    for vertex in vertices:
        graph.remove_vertex(vertex)

    assert graph.num_vertices() == 0
    assert graph.vertices() == set()


# Edge Operation Tests (RED phase - should fail)


@pytest.mark.unit
def test_graph_add_edge_success():
    """Test successfully adding edges between existing vertices."""
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    # Add edges
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("B", "C", weight=2.5)

    # Check edges were added
    assert graph.num_edges() == 2
    assert graph.has_edge("A", "B")
    assert graph.has_edge("B", "C")


@pytest.mark.unit
def test_graph_add_edge_with_nonexistent_vertex():
    """Test that adding edge with non-existent vertex raises VertexNotFoundError."""
    graph = Graph()
    graph.add_vertex("A")

    # Try to add edge with non-existent source
    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found"):
        graph.add_edge("nonexistent", "A", weight=1.0)

    # Try to add edge with non-existent target
    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found"):
        graph.add_edge("A", "nonexistent", weight=1.0)

    # Verify graph state is unchanged
    assert graph.num_edges() == 0


@pytest.mark.unit
def test_graph_add_edge_idempotent():
    """Test that adding the same edge multiple times is idempotent."""
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Add same edge multiple times
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "B", weight=1.0)

    # Should only have one edge
    assert graph.num_edges() == 1
    assert graph.has_edge("A", "B")


@pytest.mark.unit
def test_graph_add_edge_with_metadata():
    """Test adding edge with metadata."""
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Add edge with metadata
    metadata = {"type": "highway", "speed_limit": 65}
    graph.add_edge("A", "B", weight=2.5, metadata=metadata)

    # Check edge exists and has correct metadata
    assert graph.has_edge("A", "B")
    edge = graph.get_edge("A", "B")
    assert edge.weight == 2.5
    assert edge.metadata == metadata


@pytest.mark.unit
def test_graph_remove_edge_success():
    """Test successfully removing edges."""
    graph = Graph()

    # Add vertices and edges
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("B", "C", weight=2.0)

    # Remove an edge
    graph.remove_edge("A", "B")

    # Check edge was removed
    assert graph.num_edges() == 1
    assert not graph.has_edge("A", "B")
    assert graph.has_edge("B", "C")

    # Verify vertices still exist
    assert graph.num_vertices() == 3
    assert "A" in graph.vertices()
    assert "B" in graph.vertices()


@pytest.mark.unit
def test_graph_remove_edge_nonexistent():
    """Test that removing non-existent edge raises EdgeNotFoundError."""
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Try to remove non-existent edge
    with pytest.raises(EdgeNotFoundError, match="Edge .* not found"):
        graph.remove_edge("A", "B")

    # Verify graph state is unchanged
    assert graph.num_edges() == 0


@pytest.mark.unit
def test_graph_has_edge():
    """Test has_edge method."""
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    # Initially no edges
    assert not graph.has_edge("A", "B")
    assert not graph.has_edge("B", "C")

    # Add edge
    graph.add_edge("A", "B", weight=1.0)

    # Check edge exists
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("B", "C")


@pytest.mark.unit
def test_graph_get_edge():
    """Test get_edge returns correct Edge with weight and metadata."""
    graph = Graph(directed=True)  # Use directed graph to test edge direction

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Add edge with weight and metadata
    metadata = {"type": "road", "lanes": 2}
    graph.add_edge("A", "B", weight=3.5, metadata=metadata)

    # Get edge and verify
    edge = graph.get_edge("A", "B")
    assert edge.source == "A"
    assert edge.target == "B"
    assert edge.weight == 3.5
    assert edge.metadata == metadata

    # Try to get non-existent edge (reverse direction in directed graph)
    with pytest.raises(EdgeNotFoundError, match="Edge .* not found"):
        graph.get_edge("B", "A")


@pytest.mark.unit
def test_graph_get_edge_undirected():
    """Test get_edge works in both directions for undirected graphs."""
    graph = Graph(directed=False)  # Undirected graph

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Add edge with weight and metadata
    metadata = {"type": "road", "lanes": 2}
    graph.add_edge("A", "B", weight=3.5, metadata=metadata)

    # Get edge in forward direction
    edge_forward = graph.get_edge("A", "B")
    assert edge_forward.weight == 3.5
    assert edge_forward.metadata == metadata

    # Get edge in reverse direction (should work for undirected graph)
    edge_reverse = graph.get_edge("B", "A")
    assert edge_reverse.weight == 3.5
    assert edge_reverse.metadata == metadata

    # Both directions should return edges that are equal (normalized to same form)
    assert edge_forward == edge_reverse
    assert hash(edge_forward) == hash(edge_reverse)

    # Both edges are normalized to canonical form (A < B, so source='A', target='B')
    assert edge_forward.source == "A"
    assert edge_forward.target == "B"
    assert edge_reverse.source == "A"  # Also normalized
    assert edge_reverse.target == "B"  # Also normalized


@pytest.mark.unit
def test_graph_directed_edges():
    """Test that directed graphs distinguish between (u,v) and (v,u)."""
    graph = Graph(directed=True)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Add edge A -> B
    graph.add_edge("A", "B", weight=1.0)

    # Check only forward edge exists
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("B", "A")
    assert graph.num_edges() == 1

    # Add reverse edge B -> A
    graph.add_edge("B", "A", weight=2.0)

    # Check both edges exist
    assert graph.has_edge("A", "B")
    assert graph.has_edge("B", "A")
    assert graph.num_edges() == 2


@pytest.mark.unit
def test_graph_undirected_edges():
    """Test that undirected graphs treat (u,v) and (v,u) as the same edge."""
    graph = Graph(directed=False)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Add edge A - B
    graph.add_edge("A", "B", weight=1.0)

    # Check both directions exist (same edge)
    assert graph.has_edge("A", "B")
    assert graph.has_edge("B", "A")
    assert graph.num_edges() == 1


@pytest.mark.unit
def test_graph_edge_operations_atomic():
    """Test that edge operations are atomic (rollback on failure)."""
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")

    # Try to remove non-existent edge - should not change graph state
    with pytest.raises(EdgeNotFoundError):
        graph.remove_edge("A", "B")

    graph.add_edge("A", "B", weight=1.0)

    initial_edges = graph.edges().copy()
    initial_count = graph.num_edges()

    # Try to remove non-existent edge - should not change graph state
    with pytest.raises(VertexNotFoundError):
        graph.remove_edge("B", "C")

    # Verify graph state is unchanged (atomic operation)
    assert graph.edges() == initial_edges
    assert graph.num_edges() == initial_count


# Analysis Method Tests (RED phase - should fail)


@pytest.mark.unit
def test_graph_neighbors_returns_correct_set():
    """Test that neighbors() returns correct set of adjacent vertices."""
    graph = Graph(directed=False)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")

    # Add edges: A-B, A-C, B-C
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "C", weight=1.0)
    graph.add_edge("B", "C", weight=1.0)

    # Check neighbors
    neighbors_a = graph.neighbors("A")
    assert neighbors_a == {"B", "C"}, f"A should have neighbors B and C, got {neighbors_a}"

    neighbors_b = graph.neighbors("B")
    assert neighbors_b == {"A", "C"}, f"B should have neighbors A and C, got {neighbors_b}"

    neighbors_c = graph.neighbors("C")
    assert neighbors_c == {"A", "B"}, f"C should have neighbors A and B, got {neighbors_c}"

    neighbors_d = graph.neighbors("D")
    assert neighbors_d == set(), f"D should have no neighbors, got {neighbors_d}"


@pytest.mark.unit
def test_graph_neighbors_directed():
    """Test that neighbors() returns outgoing neighbors for directed graphs."""
    graph = Graph(directed=True)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    # Add directed edges: A->B, B->C, C->A
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("B", "C", weight=1.0)
    graph.add_edge("C", "A", weight=1.0)

    # Check neighbors (outgoing edges only)
    neighbors_a = graph.neighbors("A")
    assert neighbors_a == {"B"}, f"A should have neighbor B (outgoing), got {neighbors_a}"

    neighbors_b = graph.neighbors("B")
    assert neighbors_b == {"C"}, f"B should have neighbor C (outgoing), got {neighbors_b}"

    neighbors_c = graph.neighbors("C")
    assert neighbors_c == {"A"}, f"C should have neighbor A (outgoing), got {neighbors_c}"


@pytest.mark.unit
def test_graph_neighbors_nonexistent_vertex():
    """Test that neighbors() raises VertexNotFoundError for non-existent vertex."""
    graph = Graph()
    graph.add_vertex("A")

    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found"):
        graph.neighbors("nonexistent")


@pytest.mark.unit
def test_graph_degree_undirected():
    """Test that degree() works correctly for undirected graphs."""
    graph = Graph(directed=False)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")

    # Add edges: A-B, A-C, B-C
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "C", weight=1.0)
    graph.add_edge("B", "C", weight=1.0)

    # Check degrees
    assert graph.degree("A") == 2, "A should have degree 2"
    assert graph.degree("B") == 2, "B should have degree 2"
    assert graph.degree("C") == 2, "C should have degree 2"
    assert graph.degree("D") == 0, "D should have degree 0 (isolated vertex)"


@pytest.mark.unit
def test_graph_degree_directed():
    """Test that degree() works correctly for directed graphs (returns out-degree)."""
    graph = Graph(directed=True)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    # Add directed edges: A->B, A->C, B->C
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "C", weight=1.0)
    graph.add_edge("B", "C", weight=1.0)

    # Check degrees (should return out-degree for directed graphs)
    assert graph.degree("A") == 2, "A should have degree 2 (2 outgoing edges)"
    assert graph.degree("B") == 1, "B should have degree 1 (1 outgoing edge)"
    assert graph.degree("C") == 0, "C should have degree 0 (0 outgoing edges)"


@pytest.mark.unit
def test_graph_degree_nonexistent_vertex():
    """Test that degree() raises VertexNotFoundError for non-existent vertex."""
    graph = Graph()
    graph.add_vertex("A")

    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found"):
        graph.degree("nonexistent")


@pytest.mark.unit
def test_graph_in_degree_directed():
    """Test that in_degree() works correctly for directed graphs."""
    graph = Graph(directed=True)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")

    # Add directed edges: A->B, A->C, B->C, D->C
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "C", weight=1.0)
    graph.add_edge("B", "C", weight=1.0)
    graph.add_edge("D", "C", weight=1.0)

    # Check in-degrees
    assert graph.in_degree("A") == 0, "A should have in-degree 0 (no incoming edges)"
    assert graph.in_degree("B") == 1, "B should have in-degree 1 (1 incoming edge from A)"
    assert graph.in_degree("C") == 3, "C should have in-degree 3 (3 incoming edges)"
    assert graph.in_degree("D") == 0, "D should have in-degree 0 (no incoming edges)"


@pytest.mark.unit
def test_graph_out_degree_directed():
    """Test that out_degree() works correctly for directed graphs."""
    graph = Graph(directed=True)

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")

    # Add directed edges: A->B, A->C, B->C, D->C
    graph.add_edge("A", "B", weight=1.0)
    graph.add_edge("A", "C", weight=1.0)
    graph.add_edge("B", "C", weight=1.0)
    graph.add_edge("D", "C", weight=1.0)

    # Check out-degrees
    assert graph.out_degree("A") == 2, "A should have out-degree 2 (2 outgoing edges)"
    assert graph.out_degree("B") == 1, "B should have out-degree 1 (1 outgoing edge)"
    assert graph.out_degree("C") == 0, "C should have out-degree 0 (no outgoing edges)"
    assert graph.out_degree("D") == 1, "D should have out-degree 1 (1 outgoing edge)"


@pytest.mark.unit
def test_graph_in_degree_undirected_raises_error():
    """Test that in_degree() raises error for undirected graphs."""
    graph = Graph(directed=False)
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", weight=1.0)

    # in_degree should only work on directed graphs
    with pytest.raises(ValueError, match="in_degree.*directed"):
        graph.in_degree("A")


@pytest.mark.unit
def test_graph_out_degree_undirected_raises_error():
    """Test that out_degree() raises error for undirected graphs."""
    graph = Graph(directed=False)
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", weight=1.0)

    # out_degree should only work on directed graphs
    with pytest.raises(ValueError, match="out_degree.*directed"):
        graph.out_degree("A")


@pytest.mark.unit
def test_graph_in_degree_nonexistent_vertex():
    """Test that in_degree() raises VertexNotFoundError for non-existent vertex."""
    graph = Graph(directed=True)
    graph.add_vertex("A")

    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found"):
        graph.in_degree("nonexistent")


@pytest.mark.unit
def test_graph_out_degree_nonexistent_vertex():
    """Test that out_degree() raises VertexNotFoundError for non-existent vertex."""
    graph = Graph(directed=True)
    graph.add_vertex("A")

    with pytest.raises(VertexNotFoundError, match="Vertex 'nonexistent' not found"):
        graph.out_degree("nonexistent")
