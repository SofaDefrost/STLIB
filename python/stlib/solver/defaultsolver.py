# -*- coding: utf-8 -*-

def DefaultSolver(node):
        node.createObject('EulerImplicit', name='timeintegration', firstOrder='1')
        node.createObject('CGLinearSolver', name='numericsolver')


### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
	DefaultSolver(rootNode) 	
    
