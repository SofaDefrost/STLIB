# -*- coding: utf-8 -*-
import Sofa
import os
import math
path = os.path.dirname(os.path.abspath(__file__))

class Animation(object):
    def __init__(self, duration, mode, cb, params):
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
            
        if self.direction > 0.0:
            self.factor = (currentTime-self.startTime) / self.duration
        else:
            self.factor = 1.0-(currentTime-self.startTime) / self.duration
        
        if self.factor > 1.0:
            self.factor = 1.0
            
        if self.factor < 0.0:
            self.factor = 0.0
            
        self.cb(factor=self.factor , **self.params)    
        
class AnimationManagerController(Sofa.PythonScriptController):
    def __init__(self, node):
        self.listening = True
        self.name = "AnimationManager"
        self.totalTime = 0
        self.animations = []

    def addAnimation(self, animation):
        self.animations.append(animation) 

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
                        
        self.animations = nextanimations        
        return 0

def LinearRamp(beginValue, endValue, scale):
    return (endValue-beginValue) * scale + beginValue

manager = None
def animate(cb, params, duration, mode="once"):
    if manager == None:
        raise Exception("Missing manager in this scene")
        
    manager.addAnimation(Animation(duration=duration, mode=mode, cb=cb, params=params)) 

def AnimationManager(node):
    global manager
    if manager != None:
        Sofa.msg_info(node, "There is already one animation manager in this scene...why do you need a second one ?") 
        return manager 
    manager = AnimationManagerController(node)
    node.addObject(manager)    
    return manager
    
### This function is just an example on how to use the DefaultHeader function. 
def createScene(rootNode):
	AnimationManager(rootNode) 	
    
