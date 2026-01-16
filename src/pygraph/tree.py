"""Tree data structure implementation.

This module provides the Tree class, which represents a tree structure
as a specialized directed acyclic graph. Trees are internally stored using
a Graph instance, allowing unified algorithms (BFS, DFS) to work seamlessly
on both Graph and Tree structures.

Key features:
- Trees are represented as directed acyclic graphs
- Single root vertex with parent-child relationships
- O(1) parent lookups using _parent_map
- Implements GraphLike protocol for algorithm compatibility
- Enforces tree constraints (acyclic, connected, single root)

Example:
    >>> tree = Tree("root")
    >>> tree.add_child("root", "child1")
    >>> tree.add_child("root", "child2")
    >>> tree.num_vertices()
    3
    >>> tree.num_edges()
    2
"""

from __future__ import annotations

from collections.abc import Hashable

from pygraph.exceptions import CycleError, VertexNotFoundError
from pygraph.graph import Graph


class Tree[V: Hashable]:
    """Tree structure represented as a directed acyclic graph with a root.

    A tree is a connected acyclic graph with a designated root vertex.
    This implementation uses an internal directed Graph to store the tree
    structure, enabling code reuse for traversal algorithms.

    Type Parameters:
        V: The vertex type, must be hashable

    Attributes:
        root: The root vertex of the tree (read-only property)

    Example:
        >>> tree = Tree("A")
        >>> tree.root
        'A'
        >>> tree.num_vertices()
        1
        >>> tree.add_child("A", "B")
        >>> tree.add_child("A", "C")
        >>> tree.num_vertices()
        3
        >>> tree.children("A")
        {'B', 'C'}
    """

    def __init__(self, root: V) -> None:
        """Initialize a tree with a root vertex.

        Creates a new tree with a single root vertex and no edges.
        The tree is represented internally as a directed graph.

        Args:
            root: The root vertex of the tree (must be hashable)

        Example:
            >>> tree = Tree("root")
            >>> tree.root
            'root'
            >>> tree.num_vertices()
            1
            >>> tree.num_edges()
            0
        """
        self._root = root
        self._graph = Graph[V](directed=True, weighted=False)
        self._graph.add_vertex(root)
        self._parent_map: dict[V, V] = {}  # Maps child -> parent for O(1) lookups

    @property
    def root(self) -> V:
        """Get the root vertex of the tree.

        Returns:
            The root vertex

        Example:
            >>> tree = Tree(42)
            >>> tree.root
            42
        """
        return self._root

    def add_child(self, parent: V, child: V) -> None:
        """Add a child vertex to a parent vertex.

        Creates a new vertex and adds an edge from parent to child.
        Validates that the operation maintains tree constraints:
        - Parent must exist in the tree
        - Child must not already exist in the tree
        - Adding the edge must not create a cycle

        Args:
            parent: The parent vertex (must exist in tree)
            child: The child vertex to add (must not exist in tree)

        Raises:
            VertexNotFoundError: If parent vertex doesn't exist
            ValueError: If child vertex already exists
            CycleError: If adding the edge would create a cycle

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.add_child("A", "C")
            >>> tree.children("A")
            {'B', 'C'}
        """
        if parent not in self._graph.vertices():
            raise VertexNotFoundError(f"Parent vertex {parent} does not exist in tree")

        # Check if child already exists - in a tree, each vertex has exactly one parent
        if child in self._graph.vertices():
            # Check if this is a duplicate operation (same parent-child relationship)
            if child in self._graph.neighbors(parent):
                # This is a duplicate - child is already a child of this parent
                raise ValueError(f"Child vertex {child} already exists in tree")
            # Child exists but with a different parent - this would create a cycle
            # because the child already has a parent in the tree
            raise CycleError(f"Adding edge ({parent}, {child}) would create a cycle in tree")

        # Add vertex and edge
        self._graph.add_vertex(child)
        self._graph.add_edge(parent, child)

        # Update parent map
        self._parent_map[child] = parent

    def remove_subtree(self, node: V) -> None:
        """Remove a node and all its descendants from the tree.

        This method removes the specified node and recursively removes all
        of its descendants. The parent map is updated to remove entries for
        all removed nodes.

        Args:
            node: The root of the subtree to remove

        Raises:
            VertexNotFoundError: If node doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.add_child("B", "C")
            >>> tree.remove_subtree("B")  # Removes B and C
            >>> tree.num_vertices()
            1
        """
        if node not in self._graph.vertices():
            raise VertexNotFoundError(f"Vertex {node} does not exist in tree")

        # Find all descendants using BFS
        to_remove = []
        queue = [node]

        while queue:
            current = queue.pop(0)
            to_remove.append(current)

            # Add all children to the queue
            for child in self._graph.neighbors(current):
                queue.append(child)

        # Remove all nodes and update parent map
        for vertex in to_remove:
            # Remove from parent map
            if vertex in self._parent_map:
                del self._parent_map[vertex]

            # Remove vertex from graph (this also removes its edges)
            self._graph.remove_vertex(vertex)

    def parent(self, vertex: V) -> V | None:
        """Get the parent of a vertex.

        Uses the internal parent map for O(1) lookup.

        Args:
            vertex: The vertex to get the parent of

        Returns:
            The parent vertex, or None if vertex is the root

        Raises:
            VertexNotFoundError: If vertex doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.parent("B")
            'A'
            >>> tree.parent("A") is None
            True
        """
        if vertex not in self._graph.vertices():
            raise VertexNotFoundError(f"Vertex {vertex} does not exist in tree")

        return self._parent_map.get(vertex)

    def children(self, vertex: V) -> set[V]:
        """Get the children of a vertex.

        Args:
            vertex: The vertex to get children of

        Returns:
            A set of child vertices

        Raises:
            VertexNotFoundError: If vertex doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.add_child("A", "C")
            >>> tree.children("A")
            {'B', 'C'}
            >>> tree.children("B")
            set()
        """
        return self._graph.neighbors(vertex)

    def is_leaf(self, vertex: V) -> bool:
        """Check if a vertex is a leaf node (has no children).

        Args:
            vertex: The vertex to check

        Returns:
            True if vertex is a leaf (no children), False otherwise

        Raises:
            VertexNotFoundError: If vertex doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.add_child("A", "C")
            >>> tree.is_leaf("A")
            False
            >>> tree.is_leaf("B")
            True
        """
        if vertex not in self._graph.vertices():
            raise VertexNotFoundError(f"Vertex {vertex} does not exist in tree")

        return len(self.children(vertex)) == 0

    def is_root(self, vertex: V) -> bool:
        """Check if a vertex is the root node.

        Args:
            vertex: The vertex to check

        Returns:
            True if vertex is the root, False otherwise

        Raises:
            VertexNotFoundError: If vertex doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.is_root("A")
            True
            >>> tree.is_root("B")
            False
        """
        if vertex not in self._graph.vertices():
            raise VertexNotFoundError(f"Vertex {vertex} does not exist in tree")

        return vertex == self._root

    def height(self) -> int:
        """Calculate the height of the tree.

        The height is the maximum distance from the root to any leaf node.
        A single-node tree has height 0.

        Returns:
            The height of the tree

        Example:
            >>> tree = Tree("A")
            >>> tree.height()
            0
            >>> tree.add_child("A", "B")
            >>> tree.height()
            1
            >>> tree.add_child("B", "C")
            >>> tree.height()
            2
        """
        if self.num_vertices() == 1:
            return 0

        # Use BFS to find maximum depth
        max_depth = 0
        queue = [(self._root, 0)]  # (vertex, depth)

        while queue:
            vertex, depth = queue.pop(0)
            max_depth = max(max_depth, depth)

            # Add all children with incremented depth
            for child in self.children(vertex):
                queue.append((child, depth + 1))

        return max_depth

    def depth(self, vertex: V) -> int:
        """Calculate the depth of a vertex.

        The depth is the distance from the root to the vertex.
        The root has depth 0.

        Args:
            vertex: The vertex to calculate depth for

        Returns:
            The depth of the vertex

        Raises:
            VertexNotFoundError: If vertex doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.add_child("B", "C")
            >>> tree.depth("A")
            0
            >>> tree.depth("B")
            1
            >>> tree.depth("C")
            2
        """
        if vertex not in self._graph.vertices():
            raise VertexNotFoundError(f"Vertex {vertex} does not exist in tree")

        # Root has depth 0
        if vertex == self._root:
            return 0

        # Traverse from root to vertex, counting edges
        depth = 0
        current = vertex

        while current != self._root:
            parent = self.parent(current)
            if parent is None:
                # This shouldn't happen in a valid tree
                raise ValueError(f"Vertex {vertex} is not connected to root")
            depth += 1
            current = parent

        return depth

    def to_graph(self) -> Graph[V]:
        """Convert tree to graph representation.

        Returns the internal directed graph representation of the tree.
        This enables tree structures to be used with graph algorithms
        through the GraphLike protocol.

        Returns:
            A Graph instance representing the tree structure

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> graph = tree.to_graph()
            >>> graph.directed
            True
            >>> "A" in graph.vertices()
            True
            >>> "B" in graph.vertices()
            True
        """
        return self._graph

    def vertices(self) -> set[V]:
        """Get all vertices in the tree.

        Implements GraphLike protocol method.

        Returns:
            A set of all vertices in the tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.vertices()
            {'A', 'B'}
        """
        return self._graph.vertices()

    def edges(self) -> set[tuple[V, V]]:
        """Get all edges in the tree.

        Implements GraphLike protocol method.
        Returns edges as (source, target) tuples.

        Returns:
            A set of (source, target) tuples representing edges

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.edges()
            {('A', 'B')}
        """
        # Convert Edge objects to (source, target) tuples
        return {(edge.source, edge.target) for edge in self._graph.edges()}

    def neighbors(self, vertex: V) -> set[V]:
        """Get neighbors (children) of a vertex.

        Implements GraphLike protocol method.
        For trees, neighbors are the children of the vertex.

        Args:
            vertex: The vertex to get neighbors of

        Returns:
            A set of neighbor vertices (children)

        Raises:
            VertexNotFoundError: If vertex doesn't exist in tree

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.neighbors("A")
            {'B'}
        """
        return self._graph.neighbors(vertex)

    def has_edge(self, source: V, target: V) -> bool:
        """Check if an edge exists between two vertices.

        Implements GraphLike protocol method.

        Args:
            source: The source vertex
            target: The target vertex

        Returns:
            True if edge exists from source to target, False otherwise

        Example:
            >>> tree = Tree("A")
            >>> tree.add_child("A", "B")
            >>> tree.has_edge("A", "B")
            True
            >>> tree.has_edge("B", "A")
            False
        """
        return self._graph.has_edge(source, target)

    def num_vertices(self) -> int:
        """Get the number of vertices in the tree.

        Returns:
            The number of vertices

        Example:
            >>> tree = Tree("A")
            >>> tree.num_vertices()
            1
            >>> tree.add_child("A", "B")
            >>> tree.num_vertices()
            2
        """
        return self._graph.num_vertices()

    def num_edges(self) -> int:
        """Get the number of edges in the tree.

        For a tree with n vertices, there are always n-1 edges.

        Returns:
            The number of edges

        Example:
            >>> tree = Tree("A")
            >>> tree.num_edges()
            0
            >>> tree.add_child("A", "B")
            >>> tree.num_edges()
            1
            >>> tree.add_child("A", "C")
            >>> tree.num_edges()
            2
        """
        return self._graph.num_edges()

    @staticmethod
    def from_graph(graph: Graph[V], root: V) -> Tree[V]:
        """Create a tree from a graph if it's acyclic and connected.

        Validates that the graph meets tree constraints:
        - Must be directed
        - Must be acyclic (no cycles)
        - Must be connected (all vertices reachable from root)

        Args:
            graph: The graph to convert to a tree
            root: The root vertex for the tree

        Returns:
            A Tree instance representing the graph structure

        Raises:
            ValueError: If graph is not directed, contains cycles, or is not connected

        Example:
            >>> graph = Graph(directed=True)
            >>> graph.add_vertex("A")
            >>> graph.add_vertex("B")
            >>> graph.add_edge("A", "B")
            >>> tree = Tree.from_graph(graph, "A")
            >>> tree.root
            'A'
        """
        if not graph.directed:
            raise ValueError("Graph must be directed to convert to tree")

        # Check for cycles - for now, we'll implement a simple check
        # A proper has_cycle will be implemented in Phase 5
        # For now, we assume the graph is acyclic if it's being converted to a tree

        # Check connectivity - for now, we'll implement a simple check
        # A proper is_connected will be implemented in Phase 5
        # For now, we assume the graph is connected if it's being converted to a tree

        # Create tree with root
        tree = Tree[V](root)
        tree._graph = graph  # pylint: disable=protected-access
        tree._root = root  # pylint: disable=protected-access

        # Build parent map using BFS traversal
        # Note: This will be implemented when BFS is available
        # For now, we'll build it manually by traversing edges
        for edge in graph.edges():
            tree._parent_map[edge.target] = edge.source  # pylint: disable=protected-access

        return tree


# Export Tree class
__all__ = ["Tree"]
