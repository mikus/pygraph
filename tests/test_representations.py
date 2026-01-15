"""Unit tests for graph representation classes.

This module tests the AdjacencyList and AdjacencyMatrix classes that implement
the GraphRepresentation protocol. These tests verify the public behavior
and interface compliance, not internal implementation details.
"""

import pytest

from pygraph.representations import AdjacencyList, AdjacencyMatrix


class TestAdjacencyList:
    """Test cases for AdjacencyList representation."""

    @pytest.mark.unit
    def test_initialization_directed(self):
        """Test AdjacencyList initialization for directed graphs."""
        adj_list = AdjacencyList[str](directed=True)

        # Test public behavior: empty graph should have no vertices or edges
        assert adj_list.get_vertices() == set()
        assert not adj_list.get_edges()

    @pytest.mark.unit
    def test_initialization_undirected(self):
        """Test AdjacencyList initialization for undirected graphs."""
        adj_list = AdjacencyList[str](directed=False)

        # Test public behavior: empty graph should have no vertices or edges
        assert adj_list.get_vertices() == set()
        assert not adj_list.get_edges()

    @pytest.mark.unit
    def test_add_vertex_new(self):
        """Test adding a new vertex."""
        adj_list = AdjacencyList[str]()
        result = adj_list.add_vertex("A")

        assert result is True
        assert adj_list.has_vertex("A")
        assert "A" in adj_list.get_vertices()

    @pytest.mark.unit
    def test_add_vertex_existing(self):
        """Test adding an existing vertex (idempotent)."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        result = adj_list.add_vertex("A")

        assert result is False
        assert adj_list.has_vertex("A")
        assert len(adj_list.get_vertices()) == 1

    @pytest.mark.unit
    def test_remove_vertex_existing(self):
        """Test removing an existing vertex."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")
        adj_list.add_edge("A", "B")

        result = adj_list.remove_vertex("A")
        assert result is True
        assert not adj_list.has_vertex("A")
        assert not adj_list.has_edge("A", "B")  # Edge should be removed
        assert not adj_list.has_edge("B", "A")  # Reverse edge should be removed

    @pytest.mark.unit
    def test_remove_vertex_nonexistent(self):
        """Test removing a non-existent vertex."""
        adj_list = AdjacencyList[str]()
        result = adj_list.remove_vertex("A")
        assert result is False

    @pytest.mark.unit
    def test_add_edge_directed(self):
        """Test adding edge in directed graph."""
        adj_list = AdjacencyList[str](directed=True)
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")

        result = adj_list.add_edge("A", "B", weight=2.5, metadata={"type": "road"})
        assert result is True

        # Check edge exists in forward direction
        assert adj_list.has_edge("A", "B")
        edge = adj_list.get_edge_data("A", "B")
        assert edge is not None
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 2.5
        assert edge.metadata == {"type": "road"}

        # Check reverse edge doesn't exist (directed)
        assert not adj_list.has_edge("B", "A")

    @pytest.mark.unit
    def test_add_edge_undirected(self):
        """Test adding edge in undirected graph."""
        adj_list = AdjacencyList[str](directed=False)
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")

        result = adj_list.add_edge("A", "B", weight=3.0)
        assert result is True

        # Check both directions exist (undirected)
        assert adj_list.has_edge("A", "B")
        assert adj_list.has_edge("B", "A")

        # Check edge data
        forward_edge = adj_list.get_edge_data("A", "B")
        reverse_edge = adj_list.get_edge_data("B", "A")
        assert forward_edge is not None
        assert reverse_edge is not None

        # Both edges are normalized to canonical form (A < B)
        assert forward_edge.source == "A" and forward_edge.target == "B"
        assert reverse_edge.source == "A" and reverse_edge.target == "B"
        assert forward_edge.weight == reverse_edge.weight == 3.0

        # The edges are equal due to normalization
        assert forward_edge == reverse_edge

    @pytest.mark.unit
    def test_add_edge_nonexistent_vertices(self):
        """Test adding edge with non-existent vertices."""
        adj_list = AdjacencyList[str]()
        result = adj_list.add_edge("A", "B")
        assert result is False

        # Add one vertex and try again
        adj_list.add_vertex("A")
        result = adj_list.add_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_add_edge_existing(self):
        """Test adding an existing edge (idempotent)."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")
        adj_list.add_edge("A", "B")

        result = adj_list.add_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_remove_edge_directed(self):
        """Test removing edge in directed graph."""
        adj_list = AdjacencyList[str](directed=True)
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")
        adj_list.add_edge("A", "B")

        result = adj_list.remove_edge("A", "B")
        assert result is True
        assert not adj_list.has_edge("A", "B")

    @pytest.mark.unit
    def test_remove_edge_undirected(self):
        """Test removing edge in undirected graph."""
        adj_list = AdjacencyList[str](directed=False)
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")
        adj_list.add_edge("A", "B")

        result = adj_list.remove_edge("A", "B")
        assert result is True
        assert not adj_list.has_edge("A", "B")
        assert not adj_list.has_edge("B", "A")

    @pytest.mark.unit
    def test_remove_edge_nonexistent(self):
        """Test removing non-existent edge."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")

        result = adj_list.remove_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_remove_edge_nonexistent_vertices(self):
        """Test removing edge when vertices don't exist in graph."""
        adj_list = AdjacencyList[str]()

        # Try to remove edge when no vertices exist
        result1 = adj_list.remove_edge("A", "B")
        assert result1 is False

        # Add one vertex, try to remove edge to non-existent vertex
        adj_list.add_vertex("A")
        result2 = adj_list.remove_edge("A", "B")  # B doesn't exist
        assert result2 is False

        result3 = adj_list.remove_edge("B", "A")  # B doesn't exist
        assert result3 is False

    @pytest.mark.unit
    def test_has_vertex(self):
        """Test vertex existence check."""
        adj_list = AdjacencyList[str]()
        assert adj_list.has_vertex("A") is False

        adj_list.add_vertex("A")
        assert adj_list.has_vertex("A") is True

    @pytest.mark.unit
    def test_has_edge(self):
        """Test edge existence check."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")

        assert adj_list.has_edge("A", "B") is False

        adj_list.add_edge("A", "B")
        assert adj_list.has_edge("A", "B") is True

    @pytest.mark.unit
    def test_get_vertices(self):
        """Test getting all vertices."""
        adj_list = AdjacencyList[str]()
        assert adj_list.get_vertices() == set()

        adj_list.add_vertex("A")
        adj_list.add_vertex("B")
        assert adj_list.get_vertices() == {"A", "B"}

    @pytest.mark.unit
    def test_get_edges(self):
        """Test getting all edges."""
        adj_list = AdjacencyList[str](directed=True)
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")

        assert not adj_list.get_edges()

        adj_list.add_edge("A", "B", weight=2.0)
        edges = adj_list.get_edges()
        assert len(edges) == 1
        edge = next(iter(edges))  # Get the single edge from the set
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 2.0

    @pytest.mark.unit
    def test_get_neighbors(self):
        """Test getting neighbors of a vertex."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")
        adj_list.add_vertex("C")

        # No neighbors initially
        assert adj_list.get_neighbors("A") == set()

        # Add edges
        adj_list.add_edge("A", "B")
        adj_list.add_edge("A", "C")
        assert adj_list.get_neighbors("A") == {"B", "C"}

        # Non-existent vertex
        assert adj_list.get_neighbors("D") == set()

    @pytest.mark.unit
    def test_get_edge_data(self):
        """Test getting edge data."""
        adj_list = AdjacencyList[str]()
        adj_list.add_vertex("A")
        adj_list.add_vertex("B")

        # Non-existent edge
        assert adj_list.get_edge_data("A", "B") is None

        # Add edge and retrieve
        adj_list.add_edge("A", "B", weight=1.5, metadata={"color": "red"})
        edge = adj_list.get_edge_data("A", "B")
        assert edge is not None
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 1.5
        assert edge.metadata == {"color": "red"}


class TestAdjacencyMatrix:
    """Test cases for AdjacencyMatrix representation."""

    @pytest.mark.unit
    def test_initialization_directed(self):
        """Test AdjacencyMatrix initialization for directed graphs."""
        adj_matrix = AdjacencyMatrix[str](directed=True)

        # Test public behavior: empty graph should have no vertices or edges
        assert adj_matrix.get_vertices() == set()
        assert not adj_matrix.get_edges()

    @pytest.mark.unit
    def test_initialization_undirected(self):
        """Test AdjacencyMatrix initialization for undirected graphs."""
        adj_matrix = AdjacencyMatrix[str](directed=False)

        # Test public behavior: empty graph should have no vertices or edges
        assert adj_matrix.get_vertices() == set()
        assert not adj_matrix.get_edges()

    @pytest.mark.unit
    def test_add_vertex_new(self):
        """Test adding a new vertex."""
        adj_matrix = AdjacencyMatrix[str]()
        result = adj_matrix.add_vertex("A")

        assert result is True
        assert adj_matrix.has_vertex("A")
        assert "A" in adj_matrix.get_vertices()

    @pytest.mark.unit
    def test_add_vertex_existing(self):
        """Test adding an existing vertex (idempotent)."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        result = adj_matrix.add_vertex("A")

        assert result is False
        assert adj_matrix.has_vertex("A")
        assert len(adj_matrix.get_vertices()) == 1

    @pytest.mark.unit
    def test_add_multiple_vertices(self):
        """Test adding multiple vertices."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_vertex("C")

        vertices = adj_matrix.get_vertices()
        assert vertices == {"A", "B", "C"}
        assert len(vertices) == 3

    @pytest.mark.unit
    def test_remove_vertex_existing(self):
        """Test removing an existing vertex."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_vertex("C")
        adj_matrix.add_edge("A", "B")
        adj_matrix.add_edge("B", "C")

        result = adj_matrix.remove_vertex("B")
        assert result is True
        assert not adj_matrix.has_vertex("B")
        assert adj_matrix.get_vertices() == {"A", "C"}

        # Edges involving B should be removed
        assert not adj_matrix.has_edge("A", "B")
        assert not adj_matrix.has_edge("B", "C")

    @pytest.mark.unit
    def test_remove_vertex_nonexistent(self):
        """Test removing a non-existent vertex."""
        adj_matrix = AdjacencyMatrix[str]()
        result = adj_matrix.remove_vertex("A")
        assert result is False

    @pytest.mark.unit
    def test_add_edge_directed(self):
        """Test adding edge in directed graph."""
        adj_matrix = AdjacencyMatrix[str](directed=True)
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        result = adj_matrix.add_edge("A", "B", weight=2.5, metadata={"type": "road"})
        assert result is True

        # Check edge exists in forward direction
        assert adj_matrix.has_edge("A", "B")
        edge = adj_matrix.get_edge_data("A", "B")
        assert edge is not None
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 2.5
        assert edge.metadata == {"type": "road"}

        # Check reverse edge doesn't exist (directed)
        assert not adj_matrix.has_edge("B", "A")

    @pytest.mark.unit
    def test_add_edge_undirected(self):
        """Test adding edge in undirected graph."""
        adj_matrix = AdjacencyMatrix[str](directed=False)
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        result = adj_matrix.add_edge("A", "B", weight=3.0)
        assert result is True

        # Check both directions exist (undirected)
        assert adj_matrix.has_edge("A", "B")
        assert adj_matrix.has_edge("B", "A")

        forward_edge = adj_matrix.get_edge_data("A", "B")
        reverse_edge = adj_matrix.get_edge_data("B", "A")
        assert forward_edge is not None
        assert reverse_edge is not None

        # Both edges are normalized to canonical form (A < B)
        assert forward_edge.source == "A" and forward_edge.target == "B"
        assert reverse_edge.source == "A" and reverse_edge.target == "B"

        # The edges are equal due to normalization
        assert forward_edge == reverse_edge

    @pytest.mark.unit
    def test_add_edge_nonexistent_vertices(self):
        """Test adding edge with non-existent vertices."""
        adj_matrix = AdjacencyMatrix[str]()
        result = adj_matrix.add_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_add_edge_existing(self):
        """Test adding an existing edge (idempotent)."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_edge("A", "B")

        result = adj_matrix.add_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_remove_edge_directed(self):
        """Test removing edge in directed graph."""
        adj_matrix = AdjacencyMatrix[str](directed=True)
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_edge("A", "B")

        result = adj_matrix.remove_edge("A", "B")
        assert result is True
        assert not adj_matrix.has_edge("A", "B")

    @pytest.mark.unit
    def test_remove_edge_undirected(self):
        """Test removing edge in undirected graph."""
        adj_matrix = AdjacencyMatrix[str](directed=False)
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_edge("A", "B")

        result = adj_matrix.remove_edge("A", "B")
        assert result is True
        assert not adj_matrix.has_edge("A", "B")
        assert not adj_matrix.has_edge("B", "A")

    @pytest.mark.unit
    def test_remove_edge_nonexistent(self):
        """Test removing non-existent edge."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        result = adj_matrix.remove_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_remove_edge_twice(self):
        """Test removing the same edge twice."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_edge("A", "B")

        # Remove edge first time
        result1 = adj_matrix.remove_edge("A", "B")
        assert result1 is True

        # Try to remove same edge again
        result2 = adj_matrix.remove_edge("A", "B")
        assert result2 is False

        # Also test the reverse direction for undirected graph
        result3 = adj_matrix.remove_edge("B", "A")
        assert result3 is False

    @pytest.mark.unit
    def test_remove_edge_never_added(self):
        """Test removing edge that was never added."""
        adj_matrix = AdjacencyMatrix[str](directed=True)
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        # Verify vertices exist but no edge between them
        assert adj_matrix.has_vertex("A")
        assert adj_matrix.has_vertex("B")
        assert not adj_matrix.has_edge("A", "B")

        # Try to remove edge that was never added
        result = adj_matrix.remove_edge("A", "B")
        assert result is False

    @pytest.mark.unit
    def test_remove_edge_nonexistent_vertices(self):
        """Test removing edge when vertices don't exist in graph."""
        adj_matrix = AdjacencyMatrix[str]()

        # Try to remove edge when no vertices exist
        result1 = adj_matrix.remove_edge("A", "B")
        assert result1 is False

        # Add one vertex, try to remove edge to non-existent vertex
        adj_matrix.add_vertex("A")
        result2 = adj_matrix.remove_edge("A", "B")  # B doesn't exist
        assert result2 is False

        result3 = adj_matrix.remove_edge("B", "A")  # B doesn't exist
        assert result3 is False

    @pytest.mark.unit
    def test_has_vertex(self):
        """Test vertex existence check."""
        adj_matrix = AdjacencyMatrix[str]()
        assert adj_matrix.has_vertex("A") is False

        adj_matrix.add_vertex("A")
        assert adj_matrix.has_vertex("A") is True

    @pytest.mark.unit
    def test_has_edge(self):
        """Test edge existence check."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        assert adj_matrix.has_edge("A", "B") is False

        adj_matrix.add_edge("A", "B")
        assert adj_matrix.has_edge("A", "B") is True

        # Test with non-existent vertices
        assert adj_matrix.has_edge("C", "D") is False

    @pytest.mark.unit
    def test_get_vertices(self):
        """Test getting all vertices."""
        adj_matrix = AdjacencyMatrix[str]()
        assert adj_matrix.get_vertices() == set()

        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        assert adj_matrix.get_vertices() == {"A", "B"}

    @pytest.mark.unit
    def test_get_edges(self):
        """Test getting all edges."""
        adj_matrix = AdjacencyMatrix[str](directed=True)
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        assert not adj_matrix.get_edges()

        adj_matrix.add_edge("A", "B", weight=2.0)
        edges = adj_matrix.get_edges()
        assert len(edges) == 1
        edge = next(iter(edges))  # Get the single edge from the set
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 2.0

    @pytest.mark.unit
    def test_get_neighbors(self):
        """Test getting neighbors of a vertex."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")
        adj_matrix.add_vertex("C")

        # No neighbors initially
        assert adj_matrix.get_neighbors("A") == set()

        # Add edges
        adj_matrix.add_edge("A", "B")
        adj_matrix.add_edge("A", "C")
        assert adj_matrix.get_neighbors("A") == {"B", "C"}

        # Non-existent vertex
        assert adj_matrix.get_neighbors("D") == set()

    @pytest.mark.unit
    def test_get_edge_data(self):
        """Test getting edge data."""
        adj_matrix = AdjacencyMatrix[str]()
        adj_matrix.add_vertex("A")
        adj_matrix.add_vertex("B")

        # Non-existent edge
        assert adj_matrix.get_edge_data("A", "B") is None

        # Add edge and retrieve
        adj_matrix.add_edge("A", "B", weight=1.5, metadata={"color": "red"})
        edge = adj_matrix.get_edge_data("A", "B")
        assert edge is not None
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 1.5
        assert edge.metadata == {"color": "red"}

        # Non-existent vertices
        assert adj_matrix.get_edge_data("C", "D") is None
