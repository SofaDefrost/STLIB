# -*- coding: utf-8 -*-

def DefaultHeader(node, gravity=[-981.0, 0.0, 0.0], dt=0.01, plugins=[]):
	node.createObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels showCollisionModels showForceFields showInteractionForceFields')
    	node.findData('gravity').value=gravity;
    	node.findData('dt').value=0.01
 
 	for name in plugins:
	 	node.createObject('RequiredPlugin', name=name)
	 	
    	node.createObject('OglSceneFrame', style="Arrows", alignment="TopRight")

    
### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
	DefaultHeader(rootNode, plugins=["SofaMiscCollision","SofaPython","SoftRobots"])
	
    
