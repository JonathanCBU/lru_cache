"""Linked list node class for caching data."""

from typing import Generic, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """Single node in a linked list.

    Attributes:
        id: unique id number for this node
        data: data being stored in the cache
        next_node: pointer to next_node Node in list
    """

    def __init__(
        self,
        id_num: int,
        data: T,
        next_node: "Node[T] | None" = None,
    ) -> None:
        """Initialize node object with immutable data type."""
        self._id = id_num
        self._data = data
        self._data_type = type(data)
        self._next_node = next_node

    @property
    def id(self) -> int:
        """Get this node ID."""
        return self._id

    @property
    def next_node(self) -> "Node[T] | None":
        """Get the next_node node in the list."""
        return self._next_node

    @next_node.setter
    def next_node(self, value: "Node[T] | None") -> None:
        """Set the next node in the list.

        Args:
            value: The next_node node, or None to end the list
        """
        if value is not None and not isinstance(value, Node):
            err_msg = "next_node must be a Node instance or None"
            raise TypeError(err_msg)

        self._next_node = value

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
            err_msg = (
                f"Data must be of type {self._data_type.__name__}, "
                f"got {type(value).__name__}"
            )
            raise TypeError(err_msg)

        self._data = value
