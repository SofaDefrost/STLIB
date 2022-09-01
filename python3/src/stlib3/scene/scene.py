# -*- coding: utf-8 -*-
import Sofa
import Sofa.Core
import platform
from splib3.animation import AnimationManager
from stlib3.scene import ContactHeader

class SofaRuntime(object):
        class PluginManager(object):
                loadedPlugins = ["SofaPython3"]

def Settings(plugins=[], repositoryPaths=[]):
        self = Sofa.Core.Node("Settings")

        if not isinstance(plugins, list):
                Sofa.msg_error("MainHeader", "'plugins' expected to be a list, got "+str(type(plugins)))
                return node

        if "SofaPython3" not in plugins:
                plugins.append("SofaPython3")

        plugin = self.addChild("Plugins")
        for name in plugins:
                plugin.addObject('RequiredPlugin', name=name, printLog=False)

        i=0
        for repository in repositoryPaths:
                self.addObject('AddResourceRepository', name="AddResourceRepository"+str(i), path=repository)
                i+=1

        if platform.system() != "Darwin":
            self.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
        else:
            Sofa.msg_warning(self, "MacOs detected, removing OglSceneFrame from the Settings because of compatibility problem.")
        self.addObject('AttachBodyButtonSetting', name="mouseButton")

        return self

def Scene(root, gravity=[0.0,-9.81,0.0],
          dt=0.01, plugins=[], repositoryPaths=[], iterative=True):
        from stlib3.scene import contactheader

        def addMainHeader(plugins=plugins, repositoryPaths=repositoryPaths, doDebug=False):
            if not isinstance(plugins, list):
                Sofa.msg_error("MainHeader", "'plugins' expected to be a list, got "+str(type(plugins)))
                return

            if "SofaPython3" not in plugins:
                plugins.append("SofaPython3")

            if "Sofa.Component.ODESolver.Backward":
                plugins.append("Sofa.Component.ODESolver.Backward")

            if doDebug:
                from splib3.debug import DebugManager
                DebugManager(root)

            root.addObject(AnimationManager(root))

            addSettings(plugins=plugins, repositoryPaths=repositoryPaths)
            addModelling()
            addSimulation()

        def addDefaultSolver(node):
            node.addObject('EulerImplicitSolver', name='TimeIntegrationSchema')
            if iterative:
                node.addObject('CGLinearSolver', name='LinearSolver', iterations=25, tolerance=1e-5, threshold=1e-5)
            else:
                node.addObject('SparseLDLSolver', name='LinearSolver', template='CompressedRowSparseMatrixd')
            return node

        def addContactHeader(alarmDistance=1.0 ,  contactDistance = 0.1, frictionCoef= 1.0):
                ContactHeader(root, alarmDistance=alarmDistance , contactDistance=contactDistance , frictionCoef= frictionCoef)
                return root

        def addModelling():
                root.addChild("Modelling")
                return root

        def addSimulation():
                simulation = root.addChild("Simulation")
                addDefaultSolver(simulation)
                return root

        def addSettings(plugins=plugins, repositoryPaths=repositoryPaths):
                root.addChild(Settings(plugins=plugins, repositoryPaths=repositoryPaths))
                return root

        root.gravity.value = gravity
        root.dt.value = dt
        root.addObject('VisualStyle')
        root.addMainHeader = addMainHeader
        root.addSettings = addSettings
        root.addSolver = addDefaultSolver
        root.addContact = addContactHeader
        root.addModelling = addModelling
        root.addSimulation = addSimulation
        
        return root


def createScene(root):
        import os
        scene = Scene(root)

        scene.addSettings(repositoryPaths=[os.getcwd()])
        scene.addModelling()
        scene.addSimulation()

        scene.Simulation.addChild(scene.Modelling)
