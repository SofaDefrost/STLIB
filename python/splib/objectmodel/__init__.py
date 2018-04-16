from inspect import currentframe, getframeinfo,getdoc

class SofaPrefab(object):
    def __init__(self, cls):
        frameinfo = getframeinfo(currentframe().f_back)
        self.cls = cls 
        self.definedloc = (frameinfo.filename, frameinfo.lineno)
          
    def __call__(self, *args, **kwargs):
        o = self.cls(*args, **kwargs)
        frameinfo = getframeinfo(currentframe().f_back)
  
        o.node.addNewData("Prefab type", "Infos", "","s", str(o.__class__.__name__))
        o.node.addNewData("Defined in", "Infos", "","s", str(self.definedloc))
        o.node.addNewData("Instantiated in", "Infos", "","s", str((frameinfo.filename, frameinfo.lineno)))
        o.node.addNewData("Help", "Infos", "", "s", str(getdoc(o)))
        return o        

class SofaObject(object):
    def __init__(self, node, name):
        self.node = node.createChild(name)   
        self.loader = None
        self.model = None
        self.dofs = None
        self.mapping = None
        self.visual = None
        self.collision = None


