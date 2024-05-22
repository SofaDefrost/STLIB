import Sofa
import SofaRuntime
import xml.etree.ElementTree as ET

def _processNode(xmlNode, sofaNode, context={}):
        # set the value of the data field of the sofaNode from the attributes of the xmlNode
        for name, value in xmlNode.attrib.items():
            if name in sofaNode.__data__:
                sofaNode.findData(name).read(value)

        # for each child of the xmlNode
        for child in xmlNode:
            # if it is a special one "include"
            if child.tag == "include":
                # load the corresponding file
                filename = SofaRuntime.DataRepository.getFile(child.attrib["href"])
                n = sofaNode.addChild("Unnamed")

                # create a specific context
                local_context = context.copy()
                for name, value in child.attrib.items():
                    if name not in ["name", "href"]:
                        local_context[name] = value

                # recursively load the file
                loadXML(filename, n, local_context)
            # if it is a node then load and recursively process it
            elif child.tag == "Node":
                sofaChild = sofaNode.addChild(child.attrib["name"])
                _processNode(child, sofaChild, context)

            # otherwise, it is treated as an object
            else:
                # override the child attributes from the value from the context
                for name, value in context.items():
                    if name in child.attrib:
                        child.attrib[name] = value
                sofaNode.addObject(child.tag, **(child.attrib))

def loadXML(filename, sofaNode, context={}):
    """Load a sofa scene from an xml file and adds it to the provided sofaNode

       Example of use:
          from splib3.loaders.xmlloader import loadXML

          def createScene(root):
              loadXML("Caduceus.xml", root)
    """
    tree = ET.parse(filename)
    xmlNode = tree.getroot()
    _processNode(xmlNode, sofaNode, context)
    return sofaNode

def createScene(root):
    loadXML(SofaRuntime.DataRepository.getFile("Demos/caduceus.scn"), root)
