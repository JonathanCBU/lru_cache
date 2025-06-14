"""Test comnfig."""

import pytest


@pytest.fixture
def template_nodes() -> list[dict[str, int]]:
    """Template data for node creation."""
    return [
        {
            "id_num": n,
            "data": n,
        }
        for n in range(5)
    ]
