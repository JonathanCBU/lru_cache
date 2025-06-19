"""Test comnfig."""

import pytest

from lru_cache import Node


@pytest.fixture
def template_nodes() -> list[dict[str, int]]:
    return [
        {
            "id_num": n,
            "data": n,
        }
        for n in range(5)
    ]


@pytest.fixture
def unlinked_nodes(template_nodes: list[dict[str, int]]) -> list[Node]:
    return [Node(**node) for node in template_nodes]
