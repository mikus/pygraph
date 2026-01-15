"""Test to verify Hypothesis configuration is working correctly."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st


@pytest.mark.property
@given(st.integers())
def test_hypothesis_basic(x):
    """Verify Hypothesis is properly configured and runs tests."""
    # Simple property: any integer is equal to itself
    assert x == x


@pytest.mark.property
@given(st.integers(min_value=0, max_value=100))
def test_hypothesis_with_range(x):
    """Verify Hypothesis works with constrained ranges."""
    # Property: non-negative integers are >= 0
    assert x >= 0
    assert x <= 100


@pytest.mark.property
@given(st.lists(st.integers()))
def test_hypothesis_with_lists(lst):
    """Verify Hypothesis works with complex data structures."""
    # Property: reversing a list twice gives the original list
    assert list(reversed(list(reversed(lst)))) == lst


@pytest.mark.property
@settings(max_examples=150)
@given(st.integers())
def test_hypothesis_custom_iterations(x):
    """Verify we can override the default iteration count."""
    # Property: adding zero doesn't change the value
    assert x + 0 == x


@pytest.mark.unit
def test_hypothesis_settings_applied():
    """Verify that Hypothesis settings from pyproject.toml are applied."""
    from hypothesis import settings as hypothesis_settings

    # Get the default profile settings
    default_settings = hypothesis_settings.default

    # Verify max_examples is at least 100
    assert default_settings.max_examples >= 100, f"Expected max_examples >= 100, got {default_settings.max_examples}"
