# -*- coding: utf-8 -*-

def ContactHeader(rootNode, alarmDistance, contactDistance, frictionCoef=0.0):
    '''
    Args:
        rootNode (Sofa.Node): the node to attach the object to

        alarmDistance (float): define the distance at which the contact are integrated into
                               the detection computation.

        contactDistance (float): define the distance at which the contact response is
                                 integrated into the computation.


        frictionCoef (float, default=0.0): optional value, set to non-zero to enable
                                               a global friction in your scene.

    Structure:
        .. sourcecode:: qml

            rootNode : {
                DefaultPipeline,
                BruteForceDetection,
                RuleBasedContactManager,
                LocalMinDistance
            }
    '''
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('DefaultPipeline', verbose="0")
    rootNode.addObject('BruteForceBroadPhase')
    rootNode.addObject('BVHNarrowPhase')

    rootNode.addObject('RuleBasedContactManager', responseParams="mu="+str(frictionCoef),
                                                    name='Response', response='FrictionContact')
    rootNode.addObject('LocalMinDistance',
                        alarmDistance=alarmDistance, contactDistance=contactDistance,
                        angleCone=0.1)
    rootNode.addObject('GenericConstraintSolver', tolerance=1e-5, maxIterations=5e2)

    if rootNode.hasObject('SparseLDLSolver') is None:
            rootNode.addObject('SparseLDLSolver')

    return rootNode

### This function is just an example on how to use the DefaultHeader function.
def createScene(rootNode):
    import os
    from mainheader import MainHeader
    MainHeader(rootNode, plugins=["SofaMiscCollision","SofaPython","SoftRobots"], repositoryPaths=[os.getcwd()])
    ContactHeader(rootNode, alarmDistance=1, contactDistance=0.1, frictionCoef=1.0)
