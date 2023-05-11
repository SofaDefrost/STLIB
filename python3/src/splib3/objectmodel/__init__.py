# -*- coding: utf-8 -*-
from inspect import currentframe, getframeinfo, getdoc, getfile, getmodule
import functools
import Sofa
import re
import sys
import os

def setData(d, **kwargs):
        for k in kwargs:
            d.getData(str(k)).value = kwargs[k]


def setTreeData(target, pathregex, **params):
        """Recursively set the data on object which have a link path that match
           the provided regex
           The regex format is using the python re module.
           Example:
                # Display all object that contains "Rigidified.*/dofs" in their
                # path
                setTreeData(simulation, "Rigidified.*/dofs",
                            showObject = True,
                            showObjectScale = 5.0)
        """
        if isinstance(target, Sofa.Node):
            for child in target.getChildren():
                setTreeData(child, pathregex, **params)
                for obj in target.getObjects():
                    if re.search(pathregex, obj.getLinkPath()):
                        for key, value in params.items():
                            if obj.getData(key) is not None:
                                obj.getData(key).value = value
        elif re.search(pathregex, target.getLinkPath()):
            for key, value in params.items():
                if target.getData(key) is not None:
                    target.getData(key).value = value


class SofaPrefab(object):
    def __init__(self, cls):
        frameinfo = getframeinfo(currentframe().f_back)
        self.cls = cls
        self.definedloc = (frameinfo.filename, frameinfo.lineno)
        functools.update_wrapper(self, cls) ## REQUIRED IN CLASS DECORATORS to transfer the docstring back to the decorated type

    def __call__(self, *args, **kwargs):
            o = self.cls(*args, **kwargs)
            frameinfo = getframeinfo(currentframe().f_back)
            o.node.addData(name="Prefab type", group="Infos", help="", type="string", value=str(o.__class__.__name__))
            if o.__module__ in sys.modules:
                o.node.addData(name="modulepath", group="Infos", help="", type="string",
                               value=str(os.path.dirname(os.path.abspath(sys.modules[o.__module__].__file__))))
            o.node.addData(name="Defined in", group="Infos", help="", type="string", value=str(self.definedloc))
            o.node.addData(name="Instantiated in", group="Infos", help="", type="string", value=str((frameinfo.filename, frameinfo.lineno)))
            o.node.addData(name="Help", group="Infos", help="", type="string", value=str(getdoc(o)))

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
        self.node = node.addChild(name)

    def __getattr__(self, name):
        return getattr(self.node, name)

class SofaObjectWrapper(object):
    def __init__(self, node):
        print("DEPRECATED.... SOFAOBJECTWRAPPER")
        self.node = node

    def addChild(self, name):
        return self.node.addChild(name)

    def addObject(self, *args, **kwargs):
        return self.node.addObject(*args, **kwargs)

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
