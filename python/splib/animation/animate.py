# -*- coding: utf-8 -*-
import Sofa
import math


class Animation(object):
    def __init__(self, duration, mode, cb, params):
        if 'startTime' in params :
            self.startTime = params['startTime']
        else: 
            self.startTime = None

        self.duration = duration
        self.cb = cb
        self.params = params
        self.factor = 1.0
        self.direction = 1.0
        self.mode = mode 
        
    def update(self, currentTime):
        if self.startTime == None:
            self.startTime = currentTime
      
        if self.duration == 0.0:
            self.factor = 1.0
        elif self.direction > 0.0:
            self.factor = (currentTime-self.startTime) / self.duration
        else:
            self.factor = 1.0-(currentTime-self.startTime) / self.duration
        
        if self.factor > 1.0:
            self.factor = 1.0
            
        if self.factor < 0.0:
            self.factor = 0.0
            
        self.cb(factor=self.factor , **self.params)    
        
class AnimationManagerController(Sofa.PythonScriptController):
    """Implements the AnimationManager as a PythonScriptController
    """
    def __init__(self, node):
        self.listening = True
        self.name = "AnimationManager"
        self.totalTime = 0
        self.animations = []

    def addAnimation(self, animation):
        self.animations.append(animation) 

    def bwdInitGraph(self, root):
        self.onBeginAnimationStep(0.0)

    def onBeginAnimationStep(self,dt):
        self.totalTime += dt
        
        nextanimations = []
        for animation in self.animations:
            animation.update(self.totalTime)
            if animation.factor < 1.0 and animation.direction > 0.0:
                nextanimations.append(animation)
            elif animation.factor > 0.0 and animation.direction < 0.0:
                nextanimations.append(animation)
            elif animation.mode == "pingpong":
                animation.direction = -animation.direction
                animation.startTime = None
                nextanimations.append(animation)
            elif animation.mode == "loop":
                animation.direction = animation.direction
                animation.startTime = None
                nextanimations.append(animation)
                        
        self.animations = nextanimations        
        return 0

manager = None
def animate(cb, params, duration, mode="once"):
    """Construct and starts an animation

    Build a new animation from a callback function that computes the animation value,
    a set of parameters, the animation duration and the type of animation repetition pattern.

    Animation can be added from any code location (createScene, PythonScriptController)

    Example:
        .. sourcecode:: python

            def myAnimate(target, factor):
                print("I should do something on: "+target.name)


            def createScene(rootNode)
                AnimationManager(rootNode)
                animate(myAnimate, {"target" : rootNode }, 10)
    """
    if manager == None:
        raise Exception("Missing manager in this scene")
        
    manager.addAnimation(Animation(duration=duration, mode=mode, cb=cb, params=params)) 

def AnimationManager(node):
    """
    A Controller to manage all animations in the scene

    Before using the animation framework an AnimationManager
    must be added to the scene. It has in charge, at each time step
    to update all the running animations.

    Returns:
        AnimationManagerController

    Example:
        .. sourcecode:: python

            def createScene(rootNode)
                AnimationManager(rootNode)
    """
    global manager
    if manager != None:
        Sofa.msg_info(node, "There is already one animation manager in this scene...why do you need a second one ?") 
        return manager 
    manager = AnimationManagerController(node)
    return manager
    
### This function is just an example on how to use the animate function.
def createScene(rootNode):
    def myAnimate(target, factor):
        print("I should do something on: "+target.name+" factor is: "+str(factor))

    AnimationManager(rootNode)
    animate(myAnimate, {"target" : rootNode }, 10)
    
