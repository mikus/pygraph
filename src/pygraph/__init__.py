"""PyGraph: A Python graph library with efficient data structures and common graph algorithms.

This library provides:
- Graph data structures (directed/undirected, weighted/unweighted)
- Tree data structures with specialized algorithms
- Common graph algorithms (BFS, DFS, Dijkstra, MST, etc.)
- Property-based testing for correctness using Hypothesis
- Modern Python 3.14+ with comprehensive type hints

Example:
    >>> from pygraph import Graph
    >>> g = Graph()
    >>> g.add_vertex("A")
    >>> g.add_vertex("B")
    >>> g.add_edge("A", "B", weight=1.0)
    >>> print(g.vertices())
    {'A', 'B'}
"""

__version__ = "0.1.0"
__author__ = "Graph Library Contributors"
__license__ = "Apache-2.0"

# from .tree import Tree
# from .algorithms import bfs, dfs, dijkstra, topological_sort
from .exceptions import (
    CycleError,
    DisconnectedGraphError,
    EdgeNotFoundError,
    GraphError,
    InvalidGraphError,
    VertexNotFoundError,
)

# Import main classes for convenient access
# Note: These imports will be added as we implement the classes
from .graph import Graph

__all__ = [
    # Core data structures (to be uncommented as implemented)
    "Graph",
    # "Tree",
    # Algorithms (to be uncommented as implemented)
    # "bfs",
    # "dfs",
    # "dijkstra",
    # "topological_sort",
    "GraphError",
    "VertexNotFoundError",
    "EdgeNotFoundError",
    "CycleError",
    "DisconnectedGraphError",
    "InvalidGraphError",
]
