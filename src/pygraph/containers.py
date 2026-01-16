"""
Container implementations for graph traversal algorithms.

This module provides container classes that implement the TraversalContainer protocol
for use in graph traversal algorithms. Each container provides a different traversal
strategy:

- FIFOQueue: First-in-first-out queue for breadth-first search (BFS)
- LIFOStack: Last-in-first-out stack for depth-first search (DFS)
- PriorityQueue: Priority queue for algorithms like Dijkstra's shortest path

All containers implement the TraversalContainer protocol with methods:
- push(item): Add an item to the container
- pop(): Remove and return an item from the container
- __bool__(): Check if container is non-empty

Example:
    >>> from pygraph.containers import FIFOQueue, LIFOStack, PriorityQueue
    >>>
    >>> # BFS with FIFO queue
    >>> queue = FIFOQueue[str]()
    >>> queue.push("start")
    >>> while queue:
    ...     vertex = queue.pop()
    ...     # Process vertex
    >>>
    >>> # DFS with LIFO stack
    >>> stack = LIFOStack[str]()
    >>> stack.push("start")
    >>> while stack:
    ...     vertex = stack.pop()
    ...     # Process vertex
    >>>
    >>> # Dijkstra with priority queue
    >>> pq = PriorityQueue[tuple[float, str]](key=lambda x: x[0])
    >>> pq.push((0.0, "start"))
    >>> while pq:
    ...     distance, vertex = pq.pop()
    ...     # Process vertex
"""

from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Callable  # noqa: TC003
from typing import Any


class FIFOQueue[T]:
    """
    FIFO (First-In-First-Out) queue wrapper for BFS traversal.

    This container maintains items in the order they were added, returning
    the oldest item first when popped. It wraps collections.deque for
    efficient O(1) operations at both ends.

    Implements the TraversalContainer protocol for use in graph traversal
    algorithms.

    Time Complexity:
        - push(): O(1)
        - pop(): O(1)
        - __bool__(): O(1)

    Space Complexity: O(n) where n is the number of items in the queue

    Example:
        >>> queue = FIFOQueue[str]()
        >>> queue.push("first")
        >>> queue.push("second")
        >>> queue.push("third")
        >>> queue.pop()
        'first'
        >>> queue.pop()
        'second'
        >>> bool(queue)
        True
        >>> queue.pop()
        'third'
        >>> bool(queue)
        False
    """

    def __init__(self):
        """Initialize an empty FIFO queue."""
        self._queue: deque[T] = deque()

    def push(self, item: T) -> None:
        """
        Add an item to the back of the queue.

        Args:
            item: The item to push to the queue

        Time Complexity: O(1)
        """
        self._queue.append(item)

    def pop(self) -> T:
        """
        Remove and return the item from the front of the queue.

        Returns:
            The oldest item in the queue (first-in)

        Raises:
            IndexError: If the queue is empty

        Time Complexity: O(1)
        """
        return self._queue.popleft()

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if the queue is empty, False if it contains items

        Time Complexity: O(1)

        Example:
            >>> queue = FIFOQueue[int]()
            >>> queue.is_empty()
            True
            >>> queue.push(1)
            >>> queue.is_empty()
            False
        """
        return len(self._queue) == 0

    def __bool__(self) -> bool:
        """
        Check if the queue is non-empty.

        Returns:
            True if the queue contains items, False if empty

        Time Complexity: O(1)

        Example:
            >>> queue = FIFOQueue[int]()
            >>> bool(queue)
            False
            >>> queue.push(1)
            >>> bool(queue)
            True
        """
        return len(self._queue) > 0


class LIFOStack[T]:
    """
    LIFO (Last-In-First-Out) stack wrapper for DFS traversal.

    This container maintains items in reverse order of addition, returning
    the most recently added item first when popped. It wraps a Python list
    for efficient O(1) operations at the end.

    Implements the TraversalContainer protocol for use in graph traversal
    algorithms.

    Time Complexity:
        - push(): O(1) amortized
        - pop(): O(1)
        - __bool__(): O(1)

    Space Complexity: O(n) where n is the number of items in the stack

    Example:
        >>> stack = LIFOStack[str]()
        >>> stack.push("first")
        >>> stack.push("second")
        >>> stack.push("third")
        >>> stack.pop()
        'third'
        >>> stack.pop()
        'second'
        >>> bool(stack)
        True
        >>> stack.pop()
        'first'
        >>> bool(stack)
        False
    """

    def __init__(self):
        """Initialize an empty LIFO stack."""
        self._stack: list[T] = []

    def push(self, item: T) -> None:
        """
        Add an item to the top of the stack.

        Args:
            item: The item to push to the stack

        Time Complexity: O(1) amortized
        """
        self._stack.append(item)

    def pop(self) -> T:
        """
        Remove and return the item from the top of the stack.

        Returns:
            The most recently added item (last-in)

        Raises:
            IndexError: If the stack is empty

        Time Complexity: O(1)
        """
        return self._stack.pop()

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        Returns:
            True if the stack is empty, False if it contains items

        Time Complexity: O(1)

        Example:
            >>> stack = LIFOStack[int]()
            >>> stack.is_empty()
            True
            >>> stack.push(1)
            >>> stack.is_empty()
            False
        """
        return len(self._stack) == 0

    def __bool__(self) -> bool:
        """
        Check if the stack is non-empty.

        Returns:
            True if the stack contains items, False if empty

        Time Complexity: O(1)

        Example:
            >>> stack = LIFOStack[int]()
            >>> bool(stack)
            False
            >>> stack.push(1)
            >>> bool(stack)
            True
        """
        return len(self._stack) > 0


class PriorityQueue[T]:
    """
    Priority queue wrapper for algorithms like Dijkstra's shortest path.

    This container maintains items ordered by priority, returning the item
    with the lowest priority value first when popped. It wraps Python's
    heapq module for efficient O(log n) operations.

    The priority is determined by a key function that extracts a comparable
    value from each item. By default, it assumes items are tuples and uses
    the first element as the priority.

    For items with equal priority, the queue maintains stable sorting based
    on insertion order using an internal counter.

    Implements the TraversalContainer protocol for use in graph traversal
    algorithms.

    Time Complexity:
        - push(): O(log n)
        - pop(): O(log n)
        - __bool__(): O(1)

    Space Complexity: O(n) where n is the number of items in the queue

    Example:
        >>> # With explicit key function
        >>> pq = PriorityQueue[tuple[int, str]](key=lambda x: x[0])
        >>> pq.push((3, "low"))
        >>> pq.push((1, "high"))
        >>> pq.push((2, "medium"))
        >>> pq.pop()
        (1, 'high')
        >>> pq.pop()
        (2, 'medium')
        >>>
        >>> # With default key (first element of tuple)
        >>> pq = PriorityQueue[tuple[float, str]]()
        >>> pq.push((5.5, "item1"))
        >>> pq.push((1.2, "item2"))
        >>> pq.pop()
        (1.2, 'item2')
    """

    def __init__(self, key: Callable[[T], Any] | None = None):
        """
        Initialize an empty priority queue.

        Args:
            key: Optional function to extract priority from items.
                 If None, assumes items are tuples and uses first element.
                 Lower priority values are returned first.

        Example:
            >>> # Default key for tuples
            >>> pq = PriorityQueue[tuple[int, str]]()
            >>>
            >>> # Custom key function
            >>> pq = PriorityQueue[dict](key=lambda x: x['priority'])
        """
        self._heap: list[tuple[Any, int, T]] = []
        self._key = key if key else lambda x: x[0] if isinstance(x, tuple) else x
        self._counter = 0  # For stable sorting when priorities are equal

    def push(self, item: T) -> None:
        """
        Add an item to the priority queue.

        The item is inserted in the correct position based on its priority
        as determined by the key function. Items with equal priority maintain
        insertion order (stable sorting).

        Args:
            item: The item to push to the queue

        Time Complexity: O(log n)
        """
        # Use counter for stable sorting when priorities are equal
        priority = self._key(item)
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> T:
        """
        Remove and return the item with the lowest priority.

        Returns:
            The item with the lowest priority value

        Raises:
            IndexError: If the queue is empty

        Time Complexity: O(log n)
        """
        return heapq.heappop(self._heap)[2]

    def is_empty(self) -> bool:
        """
        Check if the priority queue is empty.

        Returns:
            True if the queue is empty, False if it contains items

        Time Complexity: O(1)

        Example:
            >>> pq = PriorityQueue[tuple[int, str]]()
            >>> pq.is_empty()
            True
            >>> pq.push((1, "item"))
            >>> pq.is_empty()
            False
        """
        return len(self._heap) == 0

    def __bool__(self) -> bool:
        """
        Check if the priority queue is non-empty.

        Returns:
            True if the queue contains items, False if empty

        Time Complexity: O(1)

        Example:
            >>> pq = PriorityQueue[tuple[int, str]]()
            >>> bool(pq)
            False
            >>> pq.push((1, "item"))
            >>> bool(pq)
            True
        """
        return len(self._heap) > 0


__all__ = [
    "FIFOQueue",
    "LIFOStack",
    "PriorityQueue",
]
