"""Test to verify pytest configuration is working."""

import pytest


@pytest.mark.unit
def test_pytest_configured():
    """Verify pytest is properly configured."""
    assert True


@pytest.mark.unit
def test_markers_work():
    """Verify pytest markers are configured."""
    # This test should be collected with the 'unit' marker
    assert True
