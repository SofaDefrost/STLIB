# -*- coding: utf-8 -*-

def addTimeIntegration(node, iterative=True):
    '''
    Adds EulerImplicit, CGLinearSolver

    Components added:
        EulerImplicitSolver
        CGLinearSolver
    '''
    node.addObject('EulerImplicitSolver', name='TimeIntegrationSchema')
    if iterative:
        return node.addObject('CGLinearSolver', name='LinearSolver')

    return node.addObject('SparseLDLSolver', name='LinearSolver')

### This function is just an example on how to use the DefaultHeader function.
def createScene(root):
	addTimeIntegration(root)
