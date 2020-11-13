import Sofa
from stlib3.visuals import VisualModel

def RigidObject(name="RigidObject",
                surfaceMeshFileName=None,
                translation=[0., 0., 0.],
                rotation=[0., 0., 0.],
                uniformScale=1.,
                totalMass=1.,
                volume=1.,
                inertiaMatrix=[1., 0., 0., 0., 1., 0., 0., 0., 1.],
                color=[1., 1., 0.],
                isAStaticObject=False, parent=None):
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
    #### mechanics
    object = Sofa.Core.Node(name)
    if(parent != None):
        parent.addChild(object)

    object.addObject('MechanicalObject',
                      name="mstate", template="Rigid3",
                      translation2=translation, rotation2=rotation, showObjectScale=uniformScale)

    object.addObject('UniformMass', name="mass", vertexMass=[totalMass, volume, inertiaMatrix[:]])

    if not isAStaticObject:
        object.addObject('UncoupledConstraintCorrection')

    def addCollisionModel(inputMesh=surfaceMeshFileName):
        objectCollis = object.addChild('collision')
        objectCollis.addObject('MeshObjLoader', name="loader",
                            filename=inputMesh, triangulate=True,
                            scale=uniformScale)

        objectCollis.addObject('MeshTopology', src="@loader")
        objectCollis.addObject('MechanicalObject')

        if isAStaticObject:
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
    def addVisualModel(inputMesh=surfaceMeshFileName):
        visual = VisualModel(name="visual", inputMesh=inputMesh, color=color, scale=[uniformScale]*3)
        object.addChild(visual)
        visual.addObject('RigidMapping')

    object.addVisualModel = addVisualModel

    if surfaceMeshFileName != None:
        object.addCollisionModel()
        object.addVisualModel()

    return object

def createScene(root):
    from stlib33.scene.Scene import Scene

    ## Create a basic scene graph layout with settings, modelling and simulation
    scene = Scene(root)
    scene.addSettings()
    scene.addModelling()
    scene.addSimulation()

    ## Create a RigidObject with a cube mesh.
    rigid = RigidObject(surfaceMeshFileName="mesh/smCube27.obj", parent=scene.Modelling)
    rigid.addCollisionModel()
    rigid.addVisualModel()
