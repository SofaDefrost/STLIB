# -*- coding: utf-8 -*-
"""
Templates for most of the common scene setups.

**Content:**

.. _sphinx_hyperlinks:

.. autosummary::

    Scene
    MainHeader
    ContactHeader
    Node
    Wrapper

|

stlib.scene.Scene
*****************

.. autoclass:: Scene
   :members:
   :undoc-members:

stlib.scene.Interaction
***********************

.. autoclass:: Interaction
   :members:
   :undoc-members:

stlib.scene.MainHeader
**********************

.. autofunction:: MainHeader

stlib.scene.ContactHeader
*************************

.. autofunction:: ContactHeader

stlib.scene.Node
****************

.. autofunction:: Node

stlib.scene.Wrapper
*******************

.. autoclass:: Wrapper
   :members:
   :undoc-members:
   :special-members: __getattr__

"""
import Sofa

#from splib.objectmodel import SofaPrefab, SofaObject
#from splib.scenegraph import get
#
from stlib.solver import DefaultSolver
#
from . mainheader import MainHeader
from . contactheader import ContactHeader
#from . interaction import Interaction
#
#from . wrapper import Wrapper

def Node(parentNode, name):
    """Create a new node in the graph and attach it to a parent node."""
    return parentNode.addChild(name)

class Scene(Sofa.Prefab):
    """Scene(SofaObject)
    Create a scene with default properties.

       Arg:

        node (Sofa.Node)     the node where the scene will be attached

        gravity (vec3f)      the gravity of the scene

        dt (float)           the dt time

        plugins (list(str))  set of plugins that are used in this scene

        repositoryPath (list(str)) set of path where to read the data from

        doDebug (bool)       activate debugging facility (to print text)

       There is method to add default solver and default contact management
       on demand.
    """

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)
        self.doReInit( *args, **kwargs)

    def doReInit(self, *args, **kwargs):
        
        # Instanciate Kwargs to given value
        # enter during self.doReInit
        if (kwargs.__len__() != 0):


            self.plugins=kwargs.get("plugins", [])
            self.repositoryPaths=kwargs.get("repositoryPaths", [])
            self.GRAVITY=kwargs.get("gravity", [0.0, -9.81, 0.0])
            self.DT=kwargs.get("dt", 0.01)
            self.doDebug=kwargs.get("doDebug", False)
            print('Here kwargs',self.gravity,kwargs.get("gravity"))
            print(self.__dict__)

        # Take a random python attribute and test if it exist
        # If it doesn't exist it mean that we are in the doReInit of Sofa.Prefab.__init__ 
        if ("GRAVITY" not in self.__dict__):
            print("dic empty")
            return
        
        print('Here Before')
        MainHeader(self, gravity=self.GRAVITY, dt=self.DT, plugins=self.plugins, repositoryPaths=self.repositoryPaths, doDebug=self.doDebug)

    def addSolver(self):
        self.solver = DefaultSolver(self)

    def addContact(self,  alarmDistance, contactDistance, frictionCoef=0.0):
        ContactHeader(self,  alarmDistance, contactDistance, frictionCoef)
        
#@SofaPrefab
#class Scene(SofaObject):
#    """Scene(SofaObject)
#    Create a scene with default properties.
#
#       Arg:
#
#        node (Sofa.Node)     the node where the scene will be attached
#
#        gravity (vec3f)      the gravity of the scene
#
#        dt (float)           the dt time
#
#        plugins (list(str))  set of plugins that are used in this scene
#
#        repositoryPath (list(str)) set of path where to read the data from
#
#        doDebug (bool)       activate debugging facility (to print text)
#
#       There is method to add default solver and default contact management
#       on demand.
#    """
#    def __init__(self, node,  gravity=[0.0, -9.81, 0.0], dt=0.01, plugins=[], repositoryPaths=[], doDebug=False):
#        self.node = node
#        MainHeader(node, gravity=gravity, dt=dt, plugins=plugins, repositoryPaths=repositoryPaths, doDebug=doDebug)
#        self.visualstyle = self.node["VisualStyle"] #get(node, "VisualStyle")
#
#    def addSolver(self):
#        self.solver = DefaultSolver(self.node)
#
#    def addContact(self,  alarmDistance, contactDistance, frictionCoef=0.0):
#        ContactHeader(self.node,  alarmDistance, contactDistance, frictionCoef)
