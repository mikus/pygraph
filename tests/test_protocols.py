"""Tests for core protocols in the PyGraph library.

This module tests the protocol definitions that enable unified algorithms
to work on both Graph and Tree structures.
"""

import pytest

from src.pygraph.protocols import GraphLike, TraversalContainer


def test_graphlike_protocol_exists():
    """Test that GraphLike protocol is defined correctly."""
    # Check that it's a protocol
    assert hasattr(GraphLike, "__protocol_attrs__")

    # Check that it has the required methods
    required_methods = {"vertices", "edges", "neighbors", "has_edge", "to_graph"}
    protocol_methods = set(GraphLike.__protocol_attrs__)
    assert required_methods.issubset(protocol_methods)


def test_traversal_container_protocol_exists():
    """Test that TraversalContainer protocol is defined correctly."""
    # Check that it's a protocol
    assert hasattr(TraversalContainer, "__protocol_attrs__")

    # Check that it has the required methods
    required_methods = {"push", "pop", "is_empty"}
    protocol_methods = set(TraversalContainer.__protocol_attrs__)
    assert required_methods.issubset(protocol_methods)


def test_graphlike_protocol_type_parameters():
    """Test that GraphLike protocol uses PEP 695 type parameter syntax."""
    # Check that the protocol is generic (has type parameters)
    assert hasattr(GraphLike, "__parameters__")
    assert len(GraphLike.__parameters__) == 1  # Should have one type parameter [V]


def test_traversal_container_protocol_type_parameters():
    """Test that TraversalContainer protocol uses PEP 695 type parameter syntax."""
    # Check that the protocol is generic (has type parameters)
    assert hasattr(TraversalContainer, "__parameters__")
    assert len(TraversalContainer.__parameters__) == 1  # Should have one type parameter [T]


class MockGraph:
    """Mock implementation of GraphLike protocol for testing."""

    def __init__(self):
        self._vertices = set()
        self._edges = set()

    def vertices(self):
        return self._vertices

    def edges(self):
        return self._edges

    def neighbors(self, vertex):  # pylint: disable=unused-argument
        return set()

    def has_edge(self, source, target):  # pylint: disable=unused-argument
        return False

    def to_graph(self):
        return self


class MockContainer:
    """Mock implementation of TraversalContainer protocol for testing."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0


def test_classes_implementing_protocols_are_recognized():
    """Test that classes implementing protocols are recognized correctly."""
    # Test GraphLike protocol recognition
    mock_graph = MockGraph()
    assert isinstance(mock_graph, GraphLike)

    # Test TraversalContainer protocol recognition
    mock_container = MockContainer()
    assert isinstance(mock_container, TraversalContainer)


def test_protocol_methods_have_correct_signatures():
    """Test that protocol methods have the expected signatures."""
    # Check that methods exist (this will be more detailed once implemented)
    expected_graphlike_methods = ["vertices", "edges", "neighbors", "has_edge", "to_graph"]
    for method in expected_graphlike_methods:
        assert method in dir(GraphLike), f"Method {method} not found in GraphLike protocol"

    # Test TraversalContainer method signatures
    expected_container_methods = ["push", "pop", "is_empty"]
    for method in expected_container_methods:
        assert method in dir(TraversalContainer), f"Method {method} not found in TraversalContainer protocol"


if __name__ == "__main__":
    pytest.main([__file__])
