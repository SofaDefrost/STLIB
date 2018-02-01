# -*- coding: utf-8 -*-

def STLIBHeader(node, gravity=[0.0, -9.8, 0.0], dt=0.01, plugins=[]):
        '''
        Adds: VisualStyle, RequiredPlugin, OglSceneFrame, ...

        Components added:
            VisualStyle, RequiredPlugin, OglSceneFrame,
            OglSceneFrame, FreeMotionAnimationLoop,
            GenericConstraintSolver, Collision Pipeline, BruteForceDetection

        Parameters:
            gravity
            dt
            plugins
        '''
	node.createObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels showCollisionModels showForceFields showInteractionForceFields')
    	node.findData('gravity').value=gravity;
    	node.findData('dt').value=0.01

        if "SofaMiscCollision" not in plugins:
            plugins.append("SofaMiscCollision")

        if "SofaPython" not in plugins:
            plugins.append("SofaPython")

 	for name in plugins:
	 	node.createObject('RequiredPlugin', name=name)
	 	
    	node.createObject('OglSceneFrame', style="Arrows", alignment="TopRight")

        node.createObject('FreeMotionAnimationLoop')
        node.createObject('GenericConstraintSolver', tolerance="1e-6", maxIterations="1000")
        node.createObject('CollisionPipeline')
        node.createObject('BruteForceDetection')

    
### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
	STLIBHeader(rootNode, plugins=["SofaMiscCollision","SofaPython","SoftRobots"])
	
    
