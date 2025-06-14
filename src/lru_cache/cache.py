"""Cache object."""

from lru_cache.exceptions import CacheLookupError, CacheNodeNotFoundError
from lru_cache.node import Node


class Cache:
    """Base cache class."""

    def __init__(self, max_size: int = 3) -> None:
        """Initialize empty cache."""
        self.max_size: int = max_size
        self._map: dict[int, Node] = {}
        self.head: Node | None = None
        self.tail: Node | None = None

    def _append(self, node: Node) -> None:
        node.tail = None
        if self.tail is not None:
            self.tail.next = node
        self.tail = node

    def _move_to_tail(self, node_id: int) -> None:
        new_tail = self._map[node_id]
        new_tail.prev.next = new_tail.next
        self._append(new_tail)

    def _evict(self) -> None:
        old_head = self.head
        self.head = self.head.next
        old_head.delete()

    def put(self, node: Node) -> None:
        """Attach node to cache list."""
        self._map[node.id] = node
        if self.head is None:
            self.head = node
        self._append(node=node)

    def get(self, node: Node | int) -> Node:
        """Get node from cache by id."""
        if not isinstance(node, Node | int):
            raise CacheLookupError(
                message=(
                    f"Cache requires a node or a node id for lookup, got {type(node)}"
                ),
            )
        try:
            if isinstance(node, Node):
                ret_node = self._map[node.id]
            ret_node = self._map[node]
            self._append(node=ret_node)
        except KeyError as err:
            raise CacheNodeNotFoundError from err
        else:
            return ret_node
