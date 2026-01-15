"""Unit tests for exception hierarchy.

This module tests the custom exception classes used throughout the graph library.
These tests are part of the RED phase of TDD - they should FAIL initially because
the exception classes don't exist yet.
"""

import pytest

# pylint: disable=import-outside-toplevel
# Imports inside test functions are intentional for TDD - tests should fail initially


@pytest.mark.unit
def test_graph_error_is_base_exception():
    """Test that GraphError is the base exception for all graph library errors."""
    # Import the exception (this will fail initially)
    from pygraph.exceptions import GraphError

    # Test that GraphError inherits from Exception
    assert issubclass(GraphError, Exception)

    # Test that GraphError can be instantiated
    error = GraphError("Test message")
    assert isinstance(error, Exception)
    assert str(error) == "Test message"


@pytest.mark.unit
def test_all_custom_exceptions_inherit_from_graph_error():
    """Test that all custom exceptions inherit from GraphError."""
    from pygraph.exceptions import (
        CycleError,
        DisconnectedGraphError,
        EdgeNotFoundError,
        GraphError,
        InvalidGraphError,
        VertexNotFoundError,
    )

    # Test inheritance hierarchy
    assert issubclass(VertexNotFoundError, GraphError)
    assert issubclass(EdgeNotFoundError, GraphError)
    assert issubclass(CycleError, GraphError)
    assert issubclass(DisconnectedGraphError, GraphError)
    assert issubclass(InvalidGraphError, GraphError)

    # Test that they all ultimately inherit from Exception
    assert issubclass(VertexNotFoundError, Exception)
    assert issubclass(EdgeNotFoundError, Exception)
    assert issubclass(CycleError, Exception)
    assert issubclass(DisconnectedGraphError, Exception)
    assert issubclass(InvalidGraphError, Exception)


@pytest.mark.unit
def test_exceptions_can_be_raised_and_caught():
    """Test that exceptions can be raised and caught correctly."""
    from pygraph.exceptions import (
        CycleError,
        DisconnectedGraphError,
        EdgeNotFoundError,
        GraphError,
        InvalidGraphError,
        VertexNotFoundError,
    )

    # Test raising and catching GraphError
    with pytest.raises(GraphError):
        raise GraphError("Base error")

    # Test raising and catching VertexNotFoundError
    with pytest.raises(VertexNotFoundError):
        raise VertexNotFoundError("Vertex not found")

    # Test raising and catching EdgeNotFoundError
    with pytest.raises(EdgeNotFoundError):
        raise EdgeNotFoundError("Edge not found")

    # Test raising and catching CycleError
    with pytest.raises(CycleError):
        raise CycleError("Cycle detected")

    # Test raising and catching DisconnectedGraphError
    with pytest.raises(DisconnectedGraphError):
        raise DisconnectedGraphError("Graph is disconnected")

    # Test raising and catching InvalidGraphError
    with pytest.raises(InvalidGraphError):
        raise InvalidGraphError("Invalid graph data")


@pytest.mark.unit
def test_exception_messages_are_preserved():
    """Test that exception messages are preserved when raised."""
    from pygraph.exceptions import (
        CycleError,
        DisconnectedGraphError,
        EdgeNotFoundError,
        GraphError,
        InvalidGraphError,
        VertexNotFoundError,
    )

    # Test message preservation for each exception type
    test_message = "This is a test error message"

    # GraphError
    try:
        raise GraphError(test_message)
    except GraphError as e:
        assert str(e) == test_message

    # VertexNotFoundError
    try:
        raise VertexNotFoundError(test_message)
    except VertexNotFoundError as e:
        assert str(e) == test_message

    # EdgeNotFoundError
    try:
        raise EdgeNotFoundError(test_message)
    except EdgeNotFoundError as e:
        assert str(e) == test_message

    # CycleError
    try:
        raise CycleError(test_message)
    except CycleError as e:
        assert str(e) == test_message

    # DisconnectedGraphError
    try:
        raise DisconnectedGraphError(test_message)
    except DisconnectedGraphError as e:
        assert str(e) == test_message

    # InvalidGraphError
    try:
        raise InvalidGraphError(test_message)
    except InvalidGraphError as e:
        assert str(e) == test_message


@pytest.mark.unit
def test_exceptions_can_be_caught_by_base_class():
    """Test that specific exceptions can be caught by their base class."""
    from pygraph.exceptions import (
        CycleError,
        DisconnectedGraphError,
        EdgeNotFoundError,
        GraphError,
        InvalidGraphError,
        VertexNotFoundError,
    )

    # Test that specific exceptions can be caught as GraphError
    with pytest.raises(GraphError):
        raise VertexNotFoundError("Vertex not found")

    with pytest.raises(GraphError):
        raise EdgeNotFoundError("Edge not found")

    with pytest.raises(GraphError):
        raise CycleError("Cycle detected")

    with pytest.raises(GraphError):
        raise DisconnectedGraphError("Graph is disconnected")

    with pytest.raises(GraphError):
        raise InvalidGraphError("Invalid graph data")


@pytest.mark.unit
def test_exception_types_are_distinct():
    """Test that each exception type is distinct and can be caught separately."""
    from pygraph.exceptions import (
        CycleError,
        DisconnectedGraphError,
        EdgeNotFoundError,
        InvalidGraphError,
        VertexNotFoundError,
    )

    # Test that each exception type is distinct
    vertex_error = VertexNotFoundError("vertex")
    edge_error = EdgeNotFoundError("edge")
    cycle_error = CycleError("cycle")
    disconnected_error = DisconnectedGraphError("disconnected")
    invalid_error = InvalidGraphError("invalid")

    assert type(vertex_error) != type(edge_error)
    assert type(vertex_error) != type(cycle_error)
    assert type(vertex_error) != type(disconnected_error)
    assert type(vertex_error) != type(invalid_error)

    assert type(edge_error) != type(cycle_error)
    assert type(edge_error) != type(disconnected_error)
    assert type(edge_error) != type(invalid_error)

    assert type(cycle_error) != type(disconnected_error)
    assert type(cycle_error) != type(invalid_error)

    assert type(disconnected_error) != type(invalid_error)
