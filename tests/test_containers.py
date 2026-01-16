"""
Unit tests for traversal container implementations.

This module tests the container classes used in graph traversal algorithms:
- FIFOQueue: FIFO queue for BFS traversal
- LIFOStack: LIFO stack for DFS traversal
- PriorityQueue: Priority queue for algorithms like Dijkstra

These tests follow the TDD RED phase - they are expected to FAIL until
the container implementations are created.
"""

import pytest


@pytest.mark.unit
def test_fifo_queue_maintains_fifo_order():
    """Test that FIFOQueue maintains FIFO (first-in-first-out) order."""
    from src.pygraph.containers import FIFOQueue

    queue = FIFOQueue[str]()

    # Add items in order
    queue.push("first")
    queue.push("second")
    queue.push("third")

    # Pop should return items in FIFO order
    assert queue.pop() == "first"
    assert queue.pop() == "second"
    assert queue.pop() == "third"


@pytest.mark.unit
def test_fifo_queue_with_integers():
    """Test FIFOQueue with integer items."""
    from src.pygraph.containers import FIFOQueue

    queue = FIFOQueue[int]()

    # Add integers
    for i in range(5):
        queue.push(i)

    # Pop should return in FIFO order
    for i in range(5):
        assert queue.pop() == i


@pytest.mark.unit
def test_lifo_stack_maintains_lifo_order():
    """Test that LIFOStack maintains LIFO (last-in-first-out) order."""
    from src.pygraph.containers import LIFOStack

    stack = LIFOStack[str]()

    # Add items in order
    stack.push("first")
    stack.push("second")
    stack.push("third")

    # Pop should return items in LIFO order (reverse)
    assert stack.pop() == "third"
    assert stack.pop() == "second"
    assert stack.pop() == "first"


@pytest.mark.unit
def test_lifo_stack_with_integers():
    """Test LIFOStack with integer items."""
    from src.pygraph.containers import LIFOStack

    stack = LIFOStack[int]()

    # Add integers
    for i in range(5):
        stack.push(i)

    # Pop should return in LIFO order (reverse)
    for i in range(4, -1, -1):
        assert stack.pop() == i


@pytest.mark.unit
def test_priority_queue_returns_items_by_priority():
    """Test that PriorityQueue returns items by priority (lowest first)."""
    from src.pygraph.containers import PriorityQueue

    # Create priority queue with tuples (priority, value)
    pq = PriorityQueue[tuple[int, str]](key=lambda x: x[0])

    # Add items with different priorities (not in order)
    pq.push((3, "low"))
    pq.push((1, "high"))
    pq.push((2, "medium"))

    # Pop should return items in priority order (lowest priority first)
    assert pq.pop() == (1, "high")
    assert pq.pop() == (2, "medium")
    assert pq.pop() == (3, "low")


@pytest.mark.unit
def test_priority_queue_with_default_key():
    """Test PriorityQueue with default key function (first element of tuple)."""
    from src.pygraph.containers import PriorityQueue

    # Create priority queue without explicit key (uses default)
    pq = PriorityQueue[tuple[float, str]]()

    # Add items with float priorities
    pq.push((5.5, "item1"))
    pq.push((1.2, "item2"))
    pq.push((3.7, "item3"))

    # Pop should return items in priority order
    assert pq.pop() == (1.2, "item2")
    assert pq.pop() == (3.7, "item3")
    assert pq.pop() == (5.5, "item1")


@pytest.mark.unit
def test_priority_queue_stable_sorting():
    """Test that PriorityQueue maintains stable sorting for equal priorities."""
    from src.pygraph.containers import PriorityQueue

    pq = PriorityQueue[tuple[int, str]](key=lambda x: x[0])

    # Add items with same priority
    pq.push((1, "first"))
    pq.push((1, "second"))
    pq.push((1, "third"))

    # Should maintain insertion order for equal priorities
    assert pq.pop() == (1, "first")
    assert pq.pop() == (1, "second")
    assert pq.pop() == (1, "third")


@pytest.mark.unit
def test_fifo_queue_is_empty():
    """Test that FIFOQueue.is_empty() works correctly."""
    from src.pygraph.containers import FIFOQueue

    queue = FIFOQueue[int]()

    # Empty queue should return True for is_empty()
    assert queue.is_empty()
    assert not queue  # __bool__() should also work
    assert not bool(queue)

    # Non-empty queue should return False for is_empty()
    queue.push(1)
    assert not queue.is_empty()
    assert queue  # __bool__() should also work
    assert bool(queue)

    # After popping, should return True for is_empty() again
    queue.pop()
    assert queue.is_empty()
    assert not queue


@pytest.mark.unit
def test_lifo_stack_is_empty():
    """Test that LIFOStack.is_empty() works correctly."""
    from src.pygraph.containers import LIFOStack

    stack = LIFOStack[int]()

    # Empty stack should return True for is_empty()
    assert stack.is_empty()
    assert not stack  # __bool__() should also work
    assert not bool(stack)

    # Non-empty stack should return False for is_empty()
    stack.push(1)
    assert not stack.is_empty()
    assert stack  # __bool__() should also work
    assert bool(stack)

    # After popping, should return True for is_empty() again
    stack.pop()
    assert stack.is_empty()
    assert not stack


@pytest.mark.unit
def test_priority_queue_is_empty():
    """Test that PriorityQueue.is_empty() works correctly."""
    from src.pygraph.containers import PriorityQueue

    pq = PriorityQueue[tuple[int, str]]()

    # Empty priority queue should return True for is_empty()
    assert pq.is_empty()
    assert not pq  # __bool__() should also work
    assert not bool(pq)

    # Non-empty priority queue should return False for is_empty()
    pq.push((1, "item"))
    assert not pq.is_empty()
    assert pq  # __bool__() should also work
    assert bool(pq)

    # After popping, should return True for is_empty() again
    pq.pop()
    assert pq.is_empty()
    assert not pq


@pytest.mark.unit
def test_fifo_queue_multiple_add_pop_cycles():
    """Test FIFOQueue with multiple add/pop cycles."""
    from src.pygraph.containers import FIFOQueue

    queue = FIFOQueue[str]()

    # First cycle
    queue.push("a")
    queue.push("b")
    assert queue.pop() == "a"

    # Second cycle (queue not empty)
    queue.push("c")
    assert queue.pop() == "b"
    assert queue.pop() == "c"

    # Third cycle (queue empty)
    queue.push("d")
    assert queue.pop() == "d"


@pytest.mark.unit
def test_lifo_stack_multiple_add_pop_cycles():
    """Test LIFOStack with multiple add/pop cycles."""
    from src.pygraph.containers import LIFOStack

    stack = LIFOStack[str]()

    # First cycle
    stack.push("a")
    stack.push("b")
    assert stack.pop() == "b"

    # Second cycle (stack not empty)
    stack.push("c")
    assert stack.pop() == "c"
    assert stack.pop() == "a"

    # Third cycle (stack empty)
    stack.push("d")
    assert stack.pop() == "d"


@pytest.mark.unit
def test_containers_implement_traversal_container_protocol():
    """Test that all containers implement TraversalContainer protocol."""
    from src.pygraph.containers import FIFOQueue, LIFOStack, PriorityQueue
    from src.pygraph.protocols import TraversalContainer

    # Create instances
    queue = FIFOQueue[int]()
    stack = LIFOStack[int]()
    pq = PriorityQueue[tuple[int, str]]()

    # All should be recognized as TraversalContainer instances
    assert isinstance(queue, TraversalContainer)
    assert isinstance(stack, TraversalContainer)
    assert isinstance(pq, TraversalContainer)


@pytest.mark.unit
def test_fifo_queue_with_tuples():
    """Test FIFOQueue with tuple items (for graph traversal)."""
    from src.pygraph.containers import FIFOQueue

    queue = FIFOQueue[tuple[str, str | None]]()

    # Add vertex-parent pairs
    queue.push(("A", None))
    queue.push(("B", "A"))
    queue.push(("C", "A"))

    # Pop should return in FIFO order
    assert queue.pop() == ("A", None)
    assert queue.pop() == ("B", "A")
    assert queue.pop() == ("C", "A")


@pytest.mark.unit
def test_lifo_stack_with_tuples():
    """Test LIFOStack with tuple items (for graph traversal)."""
    from src.pygraph.containers import LIFOStack

    stack = LIFOStack[tuple[str, str | None]]()

    # Add vertex-parent pairs
    stack.push(("A", None))
    stack.push(("B", "A"))
    stack.push(("C", "A"))

    # Pop should return in LIFO order
    assert stack.pop() == ("C", "A")
    assert stack.pop() == ("B", "A")
    assert stack.pop() == ("A", None)
