# -*- coding: utf-8 -*-
"""
Algorithms we often use.

Content:
********
.. autosummary::

    find

|

.. autofunction:: find

"""
def find(node, path):
    """
    Query a node or an object by its path from the provided node.

    Example:
        find(node, "/root/rigidcube1/visual/OglModel")
    """
    s = path.split('/')

    if s[1] != rootNode.name:
        return None

    node = rootNode

    for child in s[2:]:
        newnode = node.getChild(child, warning=False)
        if newnode == None:
            newnode = node.getObject(child)

        if newnode == None:
            return None

        node = newnode
    return node

