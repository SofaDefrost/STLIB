# -*- coding: utf-8 -*-
import Sofa
from defrost.solver import DefaultSolver

def ElasticObject(rootNode, 
		  name="elasticelasticobject", surface=None, volume=None, 
          rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
          surfacecolor=[1.0, 1.0, 1.0],
          poisson=0.3, young=18000,
          totalmass=1.0):
                  
    if volume == None:
        Sofa.msg_error(rootNode, "Unable to create an elastic object because there is no volume mesh provided.") 
        return None
    	
    elasticobject = rootNode.createChild(name)
    DefaultSolver(elasticobject)

    if volume.endswith(".msh"):
        elasticobject.createObject('MeshGmshLoader', name='loader', filename=volume, rotation=rotation, translation=translation)
    else:
        elasticobject.createObject('MeshVTKLoader', name='loader', filename=volume, rotation=rotation, translation=translation)
    
    elasticobject.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
    elasticobject.createObject('MechanicalObject', name='tetras', template='Vec3d')

    ## To be properly simulated and to interact with gravity or inertia forces, an elasticobject
    ## also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
    ## by adding a UniformMass component to the elasticobject node
    elasticobject.createObject('UniformMass', totalmass=totalmass)

    ## The next component to add is a FEM forcefield which defines how the elasticobject reacts
    ## to a loading (i.e. which deformations are created from forces applied onto it).
    ## Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
    ## This behavior is available via the TetrahedronFEMForceField component.
    elasticobject.createObject('TetrahedronFEMForceField', template='Vec3d',
                         	name='fem', method='large', poissonRatio=poisson,  youngModulus=young)

    #################################################################################
    ## Visualization
    if surface:
	    elasticobjectVisu = elasticobject.createChild('visual')

	    ## Add to this empty node a rendering model made of triangles and loaded from an stl file.
	    elasticobjectVisu.createObject('OglModel', filename=surface,
	                            template='ExtVec3f', color=surfacecolor, rotation=rotation, translation=translation)

	    ## Add a BarycentricMapping to deform the rendering model to follow the ones of the
	    ## mechanical model.
	    elasticobjectVisu.createObject('BarycentricMapping')
       
    return elasticobject
    
def createScene(rootNode):
    from defrost.scene import DefaultHeader
    DefaultHeader(rootNode)
    ElasticObject(rootNode, "ShouldFail")
    ElasticObject(rootNode, "NoVisual", volume="mesh/liver.msh", translation=[3.0, 0.0, 0.0])
    ElasticObject(rootNode, "WithVisual", surface="mesh/liver.obj", surfacecolor=[1.0, 0.0, 0.0], volume="mesh/liver.msh", translation=[-3, 0, 0])
	
