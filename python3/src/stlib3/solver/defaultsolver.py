# -*- coding: utf-8 -*-

def DefaultSolver(node, iterative=True):
    '''
    Adds EulerImplicit, CGLinearSolver

    Components added:
        EulerImplicitIntegrationScheme
        CGLinearSolver
    '''
    node.addObject('EulerImplicitIntegrationScheme', name='TimeIntegrationSchema')
    if iterative:
        return node.addObject('CGLinearSolver', name='LinearSolver', iterations=25, tolerance=1e-5, threshold=1e-5)

    return node.addObject('SparseLDLSolver', name='LinearSolver', template='CompressedRowSparseMatrixd')

### This function is just an example on how to use the DefaultHeader function.
def createScene(rootNode):
	DefaultSolver(rootNode)
