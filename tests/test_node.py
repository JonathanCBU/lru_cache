"""Node unite testing."""

import pytest

from lru_cache import Node
from lru_cache.exceptions import (
    InvalidNodeDataError,
    InvalidNodeLinkError,
    NodeSelfLinkError,
)


def test_create_nodes(template_nodes: list[dict[str, int]]) -> None:
    """Create nodes from template and test linkage."""
    node_0 = Node(**template_nodes[0])
    node_1 = Node(**template_nodes[1], next_node=node_0)

    assert node_0.id == template_nodes[0]["id_num"], "Node 0 id does not match template"
    assert node_1.id == template_nodes[1]["id_num"], "Node 1 id does not match template"
    assert node_0.data == template_nodes[0]["data"], (
        "Node 0 data does not match template"
    )
    assert node_1.data == template_nodes[1]["data"], (
        "Node 1 data does not match template"
    )
    assert node_0.next is None, "Node 0 should not have a next"
    assert node_1.next == node_0, "Node 1 should link to Node 0"


def test_delete_nodes(template_nodes: list[dict[str, int]]) -> None:
    """Delete nodes."""
    node_0 = Node(**template_nodes[0])
    node_1 = Node(**template_nodes[1], next_node=node_0)
    node_1.delete()

    assert node_1.data is None, "After delete node.data should be None"
    assert node_1.next is None, "After delete node.next should be None"


def test_exceptions(template_nodes: list[dict[str, int]]) -> None:
    """Node properties should have strict setters."""
    node_0 = Node(**template_nodes[0])

    with pytest.raises(InvalidNodeDataError) as data_type_error:
        node_0.data = "Hello"
    with pytest.raises(InvalidNodeLinkError) as next_type_error:
        node_0.next = "World"
    with pytest.raises(NodeSelfLinkError) as next_value_error:
        node_0.next = node_0
    assert (
        data_type_error.value.message
        == "Data must be of type <class 'int'>, got <class 'str'>"
    )
    assert (
        next_type_error.value.message
        == "Next node must be a Node instance or None, got <class 'str'>"
    )
    assert next_value_error.value.message == "Node cannot link to itself"
    assert str(2) == 2
