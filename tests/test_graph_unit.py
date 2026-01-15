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

from pygraph.exceptions import VertexNotFoundError
from pygraph.graph import Graph


@pytest.mark.unit
def test_graph_initialization_directed():
    """Test that Graph(directed=True) creates directed graph."""
    graph = Graph(directed=True)

    # Verify the graph is configured as directed through public interface
    assert graph.directed is True, "Graph should be configured as directed"


@pytest.mark.unit
def test_graph_initialization_undirected():
    """Test that Graph(directed=False) creates undirected graph."""
    graph = Graph(directed=False)

    # Verify the graph is configured as undirected through public interface
    assert graph.directed is False, "Graph should be configured as undirected"


@pytest.mark.unit
def test_graph_initialization_weighted():
    """Test that Graph(weighted=True) creates weighted graph."""
    graph = Graph(weighted=True)

    # Verify the graph is configured as weighted through public interface
    assert graph.weighted is True, "Graph should be configured as weighted"


@pytest.mark.unit
def test_graph_initialization_unweighted():
    """Test that Graph(weighted=False) creates unweighted graph."""
    graph = Graph(weighted=False)

    # Verify the graph is configured as unweighted through public interface
    assert graph.weighted is False, "Graph should be configured as unweighted"


@pytest.mark.unit
def test_graph_initialization_adjacency_list():
    """Test that Graph(representation='adjacency_list') uses adjacency list."""
    graph = Graph(representation="adjacency_list")

    # Verify the graph uses adjacency list representation through public interface
    assert graph.representation == "adjacency_list", "Graph should use adjacency list representation"


@pytest.mark.unit
def test_graph_initialization_adjacency_matrix():
    """Test that Graph(representation='adjacency_matrix') uses adjacency matrix."""
    graph = Graph(representation="adjacency_matrix")

    # Verify the graph uses adjacency matrix representation through public interface
    assert graph.representation == "adjacency_matrix", "Graph should use adjacency matrix representation"


@pytest.mark.unit
def test_graph_initialization_default_parameters():
    """Test that Graph() uses default parameters correctly."""
    graph = Graph()

    # Verify default parameters based on design document through public interface
    # Default: undirected, weighted, adjacency_list
    assert graph.directed is False, "Default graph should be undirected"
    assert graph.weighted is True, "Default graph should be weighted"
    assert graph.representation == "adjacency_list", "Default graph should use adjacency list"


@pytest.mark.unit
def test_graph_initialization_all_parameters():
    """Test that Graph can be initialized with all parameters specified."""
    graph = Graph(directed=True, weighted=False, representation="adjacency_matrix")

    # Verify all parameters are set correctly through public interface
    assert graph.directed is True, "Graph should be directed"
    assert graph.weighted is False, "Graph should be unweighted"
    assert graph.representation == "adjacency_matrix", "Graph should use adjacency matrix"


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
def test_graph_with_adjacency_list():
    """Test Graph functionality with adjacency list representation."""
    graph = Graph(representation="adjacency_list")

    # Add vertices and check through public interface
    graph.add_vertex("X")
    graph.add_vertex("Y")

    assert graph.num_vertices() == 2
    assert "X" in graph.vertices()
    assert "Y" in graph.vertices()


@pytest.mark.unit
def test_graph_with_adjacency_matrix():
    """Test Graph functionality with adjacency matrix representation."""
    graph = Graph(representation="adjacency_matrix")

    # Add vertices and check through public interface
    graph.add_vertex("P")
    graph.add_vertex("Q")

    assert graph.num_vertices() == 2
    assert "P" in graph.vertices()
    assert "Q" in graph.vertices()


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
