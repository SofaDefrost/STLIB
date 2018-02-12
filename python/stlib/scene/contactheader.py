# -*- coding: utf-8 -*-

def ContactHeader(applyTo, alarmDistance, contactDistance, withFrictionCoef=0.0):
    '''
            Args:
                applyTo (Sofa.Node): the node to attach the object to

                alarmDistance (float): define the distance at which the contact are integrated into
                                       the detection computation.

                contactDistance (float): define the distance at which the contact response is
                                         integrated into the computation.


                withFrictionCoef (float, default=0.0): optional value, set to non-zero to enable
                                                       a global friction in your scene.

            Structure:
                .. sourcecode:: qml
                     {
                        CollisionPipeline,
                        BruteForceDetection,
                        CollisionResponse,
                        LocalMinDistance
                     }


    '''
    applyTo.createObject('CollisionPipeline')
    applyTo.createObject('BruteForceDetection')

    applyTo.createObject('RuleBasedContactManager', rules='0 * FrictionContact?mu='+str(withFrictionCoef),
                                                    name='Response', response='FrictionContact')
    applyTo.createObject('LocalMinDistance',
                        alarmDistance=alarmDistance, contactDistance=contactDistance,
                        angleCone=0.01)

    return applyTo

### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
        import os
        from mainheader import MainHeader
	MainHeader(rootNode, plugins=["SofaMiscCollision","SofaPython","SoftRobots"], repositoryPaths=[os.getcwd()])
	ContactHeader(rootNode, alarmDistance=1, contactDistance=0.1, withFrictionCoef=1.0)
    
