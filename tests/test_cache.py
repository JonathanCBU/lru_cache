"""Cache unit tests."""

from lru_cache import Cache, Node


def test_create_cache(
    unlinked_nodes: list[Node],
) -> None:
    """Create basic cache and insert nodes."""
    cache = Cache()
