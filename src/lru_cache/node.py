"""Linked list node class for caching data."""

from typing import Generic, TypeVar

from lru_cache.exceptions import (
    InvalidNodeDataError,
    InvalidNodeLinkError,
    NodeSelfLinkError,
)

T = TypeVar("T")


class Node(Generic[T]):
    """Single node in a linked list.

    Attributes:
        id: unique id number for this node
        data: data being stored in the cache
        next_node: pointer to next node Node in list
    """

    def __init__(
        self,
        id_num: int,
        data: T,
        next_node: "Node[T] | None" = None,
        prev_node: "Node[T] | None" = None,
    ) -> None:
        """Initialize node object with immutable data type."""
        self._id = id_num
        self._data = data
        self._data_type = type(data)
        self._next = next_node
        self._prev = prev_node

    @property
    def id(self) -> int:
        """Get this node ID."""
        return self._id

    @property
    def next(self) -> "Node[T] | None":
        """Get the next node node in the list."""
        return self._next

    @next.setter
    def next(self, value: "Node[T] | None") -> None:
        """Set the next node in the list.

        Args:
            value: The next node, or None to end the list
        Raises:
            TypeError: If input is not None or Node type
            ValueError: if input is this Node instance
        """
        if value is not None and not isinstance(value, Node):
            raise InvalidNodeLinkError(
                message=f"Next node must be a Node instance or None, got {type(value)}",
            )
        if value == self:
            raise NodeSelfLinkError(message="Node cannot link to itself")

        self._next = value

    @property
    def prev(self) -> "Node[T] | None":
        """Get the prev node node in the list."""
        return self._prev

    @prev.setter
    def prev(self, value: "Node[T] | None") -> None:
        """Set the prev node in the list.

        Args:
            value: The prev node, or None to start the list
        Raises:
            TypeError: If input is not None or Node type
            ValueError: if input is this Node instance
        """
        if value is not None and not isinstance(value, Node):
            raise InvalidNodeLinkError(
                message=f"Prev node must be a Node instance or None, got {type(value)}",
            )
        if value == self:
            raise NodeSelfLinkError(message="Node cannot link to itself")

        self._prev = value

    @property
    def data(self) -> T:
        """Get this node data."""
        return self._data

    @data.setter
    def data(self, value: T) -> None:
        """Set the data for this node.

        Args:
            value: The new data value (must match the original type)

        Raises:
            TypeError: If the new value doesn't match the original data type
        """
        if not isinstance(value, self._data_type):
            raise InvalidNodeDataError(
                message=f"Data must be of type {self._data_type}, got {type(value)}",
            )
        self._data = value

    def delete(self) -> None:
        """Delete this node and it's data."""
        self._data = None
        self._next = None
        self._data_type = type(None)
