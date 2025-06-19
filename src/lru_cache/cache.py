"""Cache object."""

from lru_cache.exceptions import CacheLookupError, CacheNodeNotFoundError
from lru_cache.node import Node


class Cache:
    """Base cache class."""

    def __init__(self, max_size: int = 3) -> None:
        """Initialize empty cache."""
        self.max_size: int = max_size
        self.__map: dict[int, Node] = {}
        self.head: Node | None = None
        self.tail: Node | None = None

    def _move_to_tail(self, node: Node) -> None:
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        node.prev = self.tail
        node.next = None
        self.tail.next = node
        self.tail = node

    def _append(self, node: Node) -> None:
        node.prev = self.tail
        node.next = None
        self.tail.next = node
        self.tail = node

    def _evict(self) -> None:
        old_head = self.head
        self.head.next.prev = None
        self.head = self.head.next
        old_head.delete()
        del old_head

    def put(self, node: Node) -> None:
        """Attach node to cache list."""
        self.__map[node.id] = node
        if len(self.__map) > self.max_size:
            self._evict()
        if self.head is None:
            self.head = node
        if self.tail is None:
            self.tail = node
        if len(self.__map) > 1:
            self._append(node)

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
                ret_node = self.__map[node.id]
            ret_node = self.__map[node]
            self._move_to_tail(ret_node)
        except KeyError as err:
            raise CacheNodeNotFoundError from err
        else:
            return ret_node
