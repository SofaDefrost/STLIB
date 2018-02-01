# -*- coding: utf-8 -*-

def DefaultSolver(node):
    '''
    Add the basic element to simulate a scene in Sofa.
    There is an EulerImplicit time integrator and a CGLinearSolver for the
    numerical processing.
    '''
    node.createObject('EulerImplicit', name='timeintegration', firstOrder='1')
    node.createObject('CGLinearSolver', name='numericsolver')


### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
	DefaultSolver(rootNode) 	
    
