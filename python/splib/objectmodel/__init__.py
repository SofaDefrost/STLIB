from inspect import currentframe, getframeinfo,getdoc
import types
import Sofa

def setData(d, **kwargs):
        for k in kwargs:
            d.getData(str(k)).value = kwargs[k]

class SofaPrefab(object):
    def __init__(self, cls):
        frameinfo = getframeinfo(currentframe().f_back)
        self.cls = cls
        self.definedloc = (frameinfo.filename, frameinfo.lineno)

    def __call__(self, *args, **kwargs):
            o = self.cls(*args, **kwargs)
            frameinfo = getframeinfo(currentframe().f_back)
            o.node.addNewData("Prefab type", "Infos", "","string", str(o.__class__.__name__))
            o.node.addNewData("Defined in", "Infos", "","string", str(self.definedloc))
            o.node.addNewData("Instantiated in", "Infos", "","string", str((frameinfo.filename, frameinfo.lineno)))
            o.node.addNewData("Help", "Infos", "", "string", str(getdoc(o)))

            ## This is the kind of hack that make me love python
            def sofaprefab_getattr(self, name):
                return getattr(self.node, name)

            setattr(self.cls, "__getattr__", sofaprefab_getattr)
            return o

    def __getattr__(self, name):
        ## This one forward query to the decorated class. This is usfull to access static method of the object.
        return getattr(self.cls, name)

class SofaObject(object):
    def __init__(self, node, name):
        self.node = node.createChild(name)

    def __getattr__(self, name):
        return getattr(self.node, name)

        #tmp = self.node.getData(name)
        #if tmp == None:
        #    t = self.node.getChild(name, warning=False)
        #    if t != None:
        #        tmp = SofaObjectWrapper(t)
        #if tmp == None:
        #    tmp = self.node.getObject(name, warning=False)
        #if tmp == None:
        #    raise Exception("Missing attribute '"+name+"' in "+str(self) )

        #return tmp

    #def createChild(self, name):
    #    return self.node.createChild(name)

    #def createObject(self, *args, **kwargs):
    #    return self.node.createObject(*args, **kwargs)

class SofaObjectWrapper(object):
    def __init__(self, node):
        print("DEPRECATED.... SOFAOBJECTWRAPPER")
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
