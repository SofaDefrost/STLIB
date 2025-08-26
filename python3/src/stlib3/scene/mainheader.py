# -*- coding: utf-8 -*-
import Sofa
from splib3.animation import AnimationManager
import platform

def MainHeader(node, gravity=[0.0, -9.8, 0.0], dt=0.01, plugins=[], repositoryPaths=[], doDebug=False):
    '''
    Args:
        gravity (vec3f): define the gravity vector.

        dt  (float): define the timestep.

        plugins (list str): list of plugins to load

        repositoryPaths (list str): list of path to the specific data repository

    Structure:
        .. sourcecode:: qml

            rootNode : {
                gravity : gravity,
                dt : dt,
                VisualStyle,
                RepositoryPath,
                RequiredPlugin,
                OglSceneFrame,
                FreeMotionAnimationLoop,
                ProjectedGaussSeidelConstraintSolver,
                DiscreteIntersection
            }

    '''
    node.addObject('VisualStyle')
    node.findData('gravity').value = gravity
    node.findData('dt').value = dt

    node.addObject('DefaultVisualManagerLoop')

    if not isinstance(plugins, list):
        Sofa.msg_error("MainHeader", "'plugins' expected to be a list, got "+str(type(plugins)))
        return node

    if "SofaPython3" not in plugins:
        plugins.append("SofaPython3")

    confignode = node.addChild("Config")
    for name in plugins:
        confignode.addObject('RequiredPlugin', name=name, printLog=False)

    i=0
    for repository in repositoryPaths:
        confignode.addObject('AddDataRepository', name="AddDataRepository"+str(i), path=repository)
        i+=1

    if platform.system() != "Darwin":
        confignode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
    else:
        Sofa.msg_warning("MainHeader", "MacOs detected, removing OglSceneFrame from the Settings because of compatibility problem.")

    if doDebug:
        from splib3.debug import DebugManager
        DebugManager(node)

    AnimationManager(node)
    return node


### This function is just an example on how to use the DefaultHeader function.
def createScene(rootNode):
    import os
    MainHeader(rootNode, plugins=["SofaPython3"], repositoryPaths=[os.getcwd()])
