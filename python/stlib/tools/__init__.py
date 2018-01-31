# -*- coding: utf-8 -*-

def find(rootNode, path):
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

