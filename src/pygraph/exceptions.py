"""Exception hierarchy for the PyGraph library.

This module defines all custom exceptions used throughout the graph library.
All exceptions inherit from GraphError, which provides a common base for
catching any graph-related error.

The exception hierarchy is:
    GraphError (base)
    ├── VertexNotFoundError
    ├── EdgeNotFoundError
    ├── CycleError
    ├── DisconnectedGraphError
    └── InvalidGraphError

Example:
    >>> try:
    ...     graph.get_vertex("nonexistent")
    ... except GraphError as e:
    ...     print(f"Graph operation failed: {e}")
"""


class GraphError(Exception):
    """Base exception for all graph library errors.

    This is the root exception class for all graph-related errors.
    All other custom exceptions in the library inherit from this class,
    allowing users to catch any graph library error with a single except clause.

    Args:
        message: A descriptive error message explaining what went wrong.

    Example:
        >>> raise GraphError("Something went wrong with the graph")
        Traceback (most recent call last):
        ...
        pygraph.exceptions.GraphError: Something went wrong with the graph
    """

    def __init__(self, message: str) -> None:
        """Initialize the GraphError with a message.

        Args:
            message: A descriptive error message.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Return the string representation of the error."""
        return self.message


class VertexNotFoundError(GraphError):
    """Exception raised when attempting to access a vertex that doesn't exist in the graph.

    This exception is raised when operations are attempted on vertices that are not
    present in the graph, such as trying to get neighbors of a non-existent vertex
    or removing a vertex that doesn't exist.

    Args:
        message: A descriptive error message, typically including the vertex identifier.

    Example:
        >>> raise VertexNotFoundError("Vertex 'X' not found in graph")
        Traceback (most recent call last):
        ...
        pygraph.exceptions.VertexNotFoundError: Vertex 'X' not found in graph
    """


class EdgeNotFoundError(GraphError):
    """Exception raised when attempting to access an edge that doesn't exist in the graph.

    This exception is raised when operations are attempted on edges that are not
    present in the graph, such as trying to get edge data for a non-existent edge
    or removing an edge that doesn't exist.

    Args:
        message: A descriptive error message, typically including the edge endpoints.

    Example:
        >>> raise EdgeNotFoundError("Edge ('A', 'B') not found in graph")
        Traceback (most recent call last):
        ...
        pygraph.exceptions.EdgeNotFoundError: Edge ('A', 'B') not found in graph
    """


class CycleError(GraphError):
    """Exception raised when a cycle is detected in a context where cycles are not allowed.

    This exception is raised in situations where the presence of a cycle would violate
    the constraints of an operation, such as:
    - Attempting to perform topological sorting on a cyclic graph
    - Adding an edge to a tree that would create a cycle
    - Converting a cyclic graph to a tree structure

    Args:
        message: A descriptive error message about the cycle detection.

    Example:
        >>> raise CycleError("Cannot perform topological sort: cycle detected")
        Traceback (most recent call last):
        ...
        pygraph.exceptions.CycleError: Cannot perform topological sort: cycle detected
    """


class DisconnectedGraphError(GraphError):
    """Exception raised when an operation requires a connected graph but the graph is disconnected.

    This exception is raised when algorithms that require connectivity are applied
    to disconnected graphs, such as:
    - Computing minimum spanning tree on a disconnected graph
    - Finding shortest paths between vertices in different components
    - Operations that assume all vertices are reachable from each other

    Args:
        message: A descriptive error message about the connectivity requirement.

    Example:
        >>> raise DisconnectedGraphError("Cannot compute MST: graph is disconnected")
        Traceback (most recent call last):
        ...
        pygraph.exceptions.DisconnectedGraphError: Cannot compute MST: graph is disconnected
    """


class InvalidGraphError(GraphError):
    """Exception raised when graph data is invalid or malformed.

    This exception is raised when:
    - Deserializing invalid JSON data that doesn't represent a valid graph
    - Graph data structures are in an inconsistent state
    - Input data doesn't meet the requirements for graph construction
    - Validation of graph properties fails

    Args:
        message: A descriptive error message about what makes the graph invalid.

    Example:
        >>> raise InvalidGraphError("Invalid JSON: missing required 'vertices' field")
        Traceback (most recent call last):
        ...
        pygraph.exceptions.InvalidGraphError: Invalid JSON: missing required 'vertices' field
    """


# Export all exception classes for convenient importing
__all__ = [
    "GraphError",
    "VertexNotFoundError",
    "EdgeNotFoundError",
    "CycleError",
    "DisconnectedGraphError",
    "InvalidGraphError",
]
