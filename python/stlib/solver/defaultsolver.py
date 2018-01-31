# -*- coding: utf-8 -*-

def DefaultSolver(node):
	node.createObject('EulerImplicit', name='odesolver', firstOrder='1')
    	node.createObject('SparseLDLSolver', name='preconditioner')

### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
	DefaultSolver(rootNode) 	
    
