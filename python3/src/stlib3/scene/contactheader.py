# -*- coding: utf-8 -*-

def ContactHeader(applyTo, alarmDistance, contactDistance, frictionCoef=0.0):
    '''
    Args:
        applyTo (Sofa.Node): the node to attach the object to

        alarmDistance (float): define the distance at which the contact are integrated into
                               the detection computation.

        contactDistance (float): define the distance at which the contact response is
                                 integrated into the computation.


        frictionCoef (float, default=0.0): optional value, set to non-zero to enable
                                               a global friction in your scene.

    Structure:
        .. sourcecode:: qml

            applyTo : {
                DefaultPipeline,
                BruteForceDetection,
                RuleBasedContactManager,
                LocalMinDistance
            }
    '''

    if applyTo.hasObject("DefaultPipeline") is False:
            applyTo.addObject('DefaultPipeline')

    applyTo.addObject('BruteForceBroadPhase')
    applyTo.addObject('BVHNarrowPhase')

    applyTo.addObject('RuleBasedContactManager', responseParams="mu="+str(frictionCoef),
                                                    name='Response', response='FrictionContact')
    applyTo.addObject('LocalMinDistance',
                        alarmDistance=alarmDistance, contactDistance=contactDistance,
                        angleCone=0.01)

    if applyTo.hasObject("FreeMotionAnimationLoop") is False:
            applyTo.addObject('FreeMotionAnimationLoop')

    if applyTo.hasObject("GenericConstraintSolver") is False:
            applyTo.addObject('GenericConstraintSolver', tolerance=1e-6, maxIterations=1000)

    return applyTo

### This function is just an example on how to use the DefaultHeader function.
def createScene(rootnode):
    import os
    from mainheader import MainHeader
    MainHeader(rootnode, plugins=["SofaMiscCollision","SofaPython3","SoftRobots","SofaConstraint"], repositoryPaths=[os.getcwd()])
    ContactHeader(rootnode, alarmDistance=1, contactDistance=0.1, frictionCoef=1.0)
