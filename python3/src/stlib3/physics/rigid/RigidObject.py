import Sofa
from stlib3.visuals import VisualModel


class RigidObject(Sofa.Prefab):
    """Creates and adds rigid body from a surface mesh.
    Args:
        surfaceMeshFileName (str):  The path or filename pointing to surface mesh file.
        totalMass (float):   The mass is distributed according to the geometry of the object.
        color (vec3f):  The default color used for the rendering of the object.
        translation (vec3f):   Apply a 3D translation to the object.
        rotation (vec3f):   Apply a 3D rotation to the object in Euler angles.
        uniformScale (vec3f):   Apply a uniform scaling to the object.
        isAStaticObject (bool): The object does not move in the scene (e.g. floor, wall) but react to collision.
    Structure:
            .. sourcecode:: qml
                Node : {
                    name : "rigidobject"
                    MechanicalObject,
                    UniformMass,
                    UncoupledConstraintCorrection,
                    *EulerImplicit,
                    *SparseLDLSolver,
                    Node : {
                        name : "collision",
                        Mesh,
                        MechanicalObject,
                        Triangle,
                        Line,
                        Point,
                        RigidMapping
                    }
                    Node : {
                       name : "visual"
                       OglModel,
                       RigidMapping
                    }
                }
    """
#        def RigidObject(name="RigidObject",
#                surfaceMeshFileName=None,
#                translation=[0., 0., 0.],
#                rotation=[0., 0., 0.],
#                uniformScale=1.,
#                totalMass=1.,
#                volume=1.,
#                inertiaMatrix=[1., 0., 0., 0., 1., 0., 0., 0., 1.],
#                color=[1., 1., 0.],
#                isAStaticObject=False, parent=None):


    properties = [
        {'name':'surfaceMeshFileName', 'type':'string', 'help':'Path to visual mesh file',  'default':''},
        {'name':'translation',    'type':'Vec3d',  'help':'translate visual model',    'default':[0.,0.,0.]},
        {'name':'rotation',       'type':'Vec3d',  'help':'rotate visual model',       'default':[0.,0.,0.]},
        {'name':'uniformScale',          'type':'double',  'help':'scale visual model',        'default': 1.},
        {'name':'color',          'type':'Vec4d',  'help':'color put to visual model', 'default':[1., 1., 1., 1.]},
        {'name':'isStaticObject', 'type':'bool',  'help':'Indicate that the object will not move in the scene', 'default':False}]

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)
        self.hasVisualModel = False
        self.hasCollisionModel = False
        
    def doReInit(object):
        #### mechanics
        plugins = object.addChild("Dependencies")
                         
        object.addObject('MechanicalObject',
                          name="mstate", template="Rigid3",
                          translation2=list(object.translation.value), rotation2=list(object.rotation.value), scale3d=[object.uniformScale.value]*3)
    
        #object.addObject('UniformMass', name="mass", vertexMass=[list(object.totalMass.value), 
        #                                                         list(object.volume.value), 
        #                                                         list(object.inertiaMatrix[:])])
        #object.addObject('UniformMass', name="mass")
    
        if object.isStaticObject:
            plugins.addObject("RequiredPlugin", name="SofaConstraint")        
            object.addObject('UncoupledConstraintCorrection')
    
        def addCollisionModel(inputMesh=object.surfaceMeshFileName.value):
            objectCollis = object.addChild('collision')
            plugins.addObject("RequiredPlugin", name="SofaRigid")                    
            plugins.addObject("RequiredPlugin", name="SofaMeshCollision")                    
            objectCollis.addObject('MeshObjLoader', name="loader",
                                filename=inputMesh, triangulate=True,
                                scale3d=[object.uniformScale.value]*3)
    
            objectCollis.addObject('MeshTopology', src="@loader")
            objectCollis.addObject('MechanicalObject')
    
            if object.isStaticObject:
                objectCollis.addObject('TriangleCollisionModel', moving=False, simulated=False)
                objectCollis.addObject('LineCollisionModel', moving=False, simulated=False)
                objectCollis.addObject('PointCollisionModel', moving=False, simulated=False)
            else:
                objectCollis.addObject('TriangleCollisionModel')
                objectCollis.addObject('LineCollisionModel')
                objectCollis.addObject('PointCollisionModel')
    
            objectCollis.addObject('RigidMapping')

        object.addCollisionModel = addCollisionModel

        #### visualization
        def addVisualModel(inputMesh=object.surfaceMeshFileName):
            visual = VisualModel(name="visual", visualMeshPath=inputMesh, color=object.color, scale=[object.uniformScale.value]*3)
            object.addChild(visual)
            visual.addObject('RigidMapping')

        object.addVisualModel = addVisualModel

        if object.surfaceMeshFileName.value != "":
            object.addCollisionModel()
            object.addVisualModel()

def createScene(root):
    from stlib3.scene.scene import Scene

    ## Create a basic scene graph layout with settings, modelling and simulation
    scene = Scene(root)
    scene.addSettings()
    scene.addModelling()
    scene.addSimulation()

    scene.Settings.addObject("OglGrid", nbSubdiv=10, size=1000)


    ## Create a RigidObject with a cube mesh.
    rigid = RigidObject(surfaceMeshFileName="mesh/smCube27.obj")
    scene.Modelling.addChild(rigid)    
    scene.Simulation.addChild(rigid)
