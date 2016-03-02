#!/usr/bin/env python3

from depgraph import Node

def test_node_constructor():
    n1 = Node("Name1")
    assert n1.name == "Name1"
    assert n1.parents == []
    assert n1.children == []

def test_node_add_child():
    n1 = Node("Node1")
    n2 = Node("Node2")
    n3 = Node("Node3")

    n1.add_child(n2)
    n1.add_child(n3)
    n2.add_child(n3)

    ## check n1 prperties.
    assert (n2 in n1.children) and (n3 in n1.children)
    assert n1.parents == []
    ## check n2 properties
    assert (n1 in n2.parents) and (n3 in n2.children)
    ## checck n3 properties
    assert (n2 in n3.parents) and (n1 in n3.parents)
    assert n3.children == []

def test_noe_add_parent():
    n1 = Node("Node1")
    n2 = Node("Node2")
    n3 = Node("Node3")

    n1.add_parent(n2)
    n1.add_parent(n3)
    n2.add_parent(n3)

    ## check n1 prperties.
    assert (n2 in n1.parents) and (n3 in n1.parents)
    assert n1.children == []
    ## check n2 properties
    assert (n3 in n2.parents)
    assert (n1 in n2.children)
    ## checck n3 properties
    assert (n2 in n3.children) and (n1 in n3.children)
    assert n3.parents == []

def test_node_search():
    n1 = Node("Node1")
    n2 = Node("Node2")
    n3 = Node("Node3")
    n4 = Node("Node4")

    n1.add_child(n2)
    n1.add_child(n3)
    n2.add_child(n4)

    assert (None != n1.search("Node2"))
    assert (None != n1.search("Node3"))
    assert (None != n1.search("Node4"))
    assert (None == n1.search("Node42"))

    assert (None != n2.search("Node4"))
    assert (None == n2.search("Node3"))

    assert (None == n3.search("Node1"))
    assert (None == n3.search("Node2"))
    assert (None == n3.search("Node4"))

    assert (None == n4.search("Node1"))
    assert (None == n4.search("Node2"))
    assert (None == n4.search("Node3"))
    assert (None != n4.search("Node4"))    

def test_node_return_tree():
    pass
