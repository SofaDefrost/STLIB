from inspect import currentframe, getframeinfo,getdoc
import types 

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

    def __getattr__(self, name):
        ## This one forward query to the decorated class. This is usfull to access static method of the object.       
        return getattr(self.cls, name)

class SofaObject(object):
    def __init__(self, node, name):
        self.node = node.createChild(name)   
        self.loader = None
        self.model = None
        self.dofs = None
        self.mapping = None
        self.visual = None
        self.collision = None

    def __getattr__(self, name):
        tmp = self.node.getData(name)
        if tmp == None:
            t = self.node.getChild(name, warning=False)
            if t != None:
                tmp = SofaObjectWrapper(t)
        if tmp == None:
            tmp = self.node.getObject(name, warning=False)
        if tmp == None:
            raise Exception("Missing attribute '"+name+"' in "+str(self) )

        return tmp

    def createChild(self, name):
        return self.node.createChild(name)
    
    def createObject(self, *args, **kwargs):
        return self.node.createObject(*args, **kwargs)

class SofaObjectWrapper(object):
    def __init__(self, node):
        self.node = node

    def createChild(self, name):
        return self.node.createChild(name)

    def createObject(self, *args, **kwargs):
        return self.node.createObject(*args, **kwargs)

    def __getattr__(self, name):
        
        tmp = self.node.getData(name)
        if tmp == None:
            t = self.node.getChild(name, warning=False)
            if t != None:
                tmp = SofaObjectWrapper(t)
        if tmp == None:
            tmp = self.node.getObject(name, warning=False)
        if tmp == None:
            raise Exception("Missing attribute '"+name+"' in "+str(self) )

        return tmp

