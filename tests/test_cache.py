"""Cache unit tests."""

from lru_cache import Cache, Node


def test_create_cache(
    unlinked_nodes: list[Node],
) -> None:
    """Create basic cache and insert nodes."""
    cache = Cache(max_size=len(unlinked_nodes))

    for node in unlinked_nodes:
        cache.put(node=node)

    assert cache.head == unlinked_nodes[0]
    assert cache.tail == unlinked_nodes[-1]

    node_2 = cache.get(node=2)
    assert node_2 == unlinked_nodes[2]
    assert cache.tail == node_2


def test_evict_cache(unlinked_nodes: list[Node]) -> None:
    """Create list and overfill to evict least recently used."""
    cache = Cache(max_size=3)

    for node in unlinked_nodes[:3]:
        cache.put(node=node)

    assert cache.head == unlinked_nodes[0]
    cache.put(node=unlinked_nodes[-1])
    assert cache.head == unlinked_nodes[1]
