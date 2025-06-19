"""Cache object."""

from lru_cache.exceptions import CacheLookupError, CacheNodeNotFoundError
from lru_cache.node import Node


class Cache:
    """Base cache class."""

    def __init__(self, max_size: int = 3):
        """Initialize empty cache."""
        self.max_size: int = max_size
        self.__map: dict[int, Node] = {}
        self.__size = 0
        self.head: Node | None = None
        self.tail: Node | None = None

    def _move_to_tail(self, node: Node) -> None:
        """Move node to tail (most recently used position)."""
        # If node is already the tail, nothing to do
        if node == self.tail:
            return

        # If node is the head, update head pointer
        if node == self.head:
            self.head = node.next
            if self.head:
                self.head.prev = None
        else:
            # Remove node from its current position
            if node.prev:
                node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev

        # Add node to tail
        node.prev = self.tail
        node.next = None

        if self.tail:
            self.tail.next = node
        self.tail = node

        # If this is the only node, it's also the head
        if self.head is None:
            self.head = node

    def _append(self, node: Node) -> None:
        node.prev = self.tail
        node.next = None
        self.tail.next = node
        self.tail = node

    def _remove_from_map(self, node_id: int) -> None:
        """Remove node from map and update map size."""
        del self.__map[node_id]
        self.__size -= 1

    def _add_to_map(self, node: Node) -> None:
        """Add node to map and update map size."""
        if node.id not in self.__map:
            self.__size += 1
        self.__map[node.id] = node

    def _evict(self) -> None:
        """Remove the least recently used node (head)."""
        if self.head is None:
            return

        # Get the node to remove from the map
        node_to_remove = self.head

        # Remove from map first
        if node_to_remove.id in self.__map:
            self._remove_from_map(node_to_remove.id)

        # Handle single node case
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            # Move head to next node
            self.head = self.head.next
            if self.head:
                self.head.prev = None

        # Clean up the removed node
        node_to_remove.prev = None
        node_to_remove.next = None

    def put(self, node: Node) -> None:
        """Add node to cache, evicting if necessary."""
        # Check if node already exists in cache
        if node.id in self.__map:
            # Update existing node and move to tail
            existing_node = self.__map[node.id]
            # Update the node's data if needed
            existing_node.data = node.data  # Assuming Node has a data attribute
            self._move_to_tail(existing_node)
            return

        # Add new node to map
        self._add_to_map(node)

        # Check if we need to evict before adding
        if self.__size > self.max_size:
            self._evict()

        # Handle empty cache
        if self.head is None and self.tail is None:
            self.head = node
            self.tail = node
            node.prev = None
            node.next = None
        else:
            # Add to tail
            node.prev = self.tail
            node.next = None
            if self.tail:
                self.tail.next = node
            self.tail = node

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
            else:
                ret_node = self.__map[node]
            self._move_to_tail(ret_node)
        except KeyError as err:
            raise CacheNodeNotFoundError from err
        else:
            return ret_node
