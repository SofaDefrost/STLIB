# -*- coding: utf-8 -*-
import Sofa


def Topology(node, src=None, type="tetrahedron"):
    """
    Add topology container to the given node.

    Args:
        node (Sofa.Node): Node where the topology is added

        src (link): Link to the mesh loader.

        type (str): Type of topology between (point/edge/triangle/quad/tetrahedron/hexahedron), default is tetrahedron.
    """

    if type == "point":
        node.createObject('PointSetTopologyContainer', src='@loader', name='container')
        node.createObject('PointSetTopologyModifier', name="topologymodifier")
        node.createObject('PointSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('PointSetGeometryAlgorithms', name="geometryalgorithms")

    elif type == "edge":
        node.createObject('EdgeSetTopologyContainer', src='@loader', name='container')
        node.createObject('EdgeSetTopologyModifier', name="topologymodifier")
        node.createObject('EdgeSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('EdgeSetGeometryAlgorithms', name="geometryalgorithms")

    elif type == "triangle":
        node.createObject('TriangleSetTopologyContainer', src='@loader', name='container')
        node.createObject('TriangleSetTopologyModifier', name="topologymodifier")
        node.createObject('TriangleSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('TriangleSetGeometryAlgorithms', name="geometryalgorithms")

    elif type == "quad":
        node.createObject('QuadSetTopologyContainer', src='@loader', name='container')
        node.createObject('QuadSetTopologyModifier', name="topologymodifier")
        node.createObject('QuadSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('QuadSetGeometryAlgorithms', name="geometryalgorithms")

    elif type == "hexahedron":
        node.createObject('HexahedronSetTopologyContainer', src='@loader', name='container')
        node.createObject('HexahedronSetTopologyModifier', name="topologymodifier")
        node.createObject('HexahedronSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('HexahedronSetGeometryAlgorithms', name="geometryalgorithms")

    elif type == "tetrahedron":
        node.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
        node.createObject('TetrahedronSetTopologyModifier', name="topologymodifier")
        node.createObject('TetrahedronSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('TetrahedronSetGeometryAlgorithms', name="geometryalgorithms")

    else:
        Sofa.msg_warning("Did not understand topology type. Set default tetrahedron.")
        node.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
        node.createObject('TetrahedronSetTopologyModifier', name="topologymodifier")
        node.createObject('TetrahedronSetTopologyAlgorithms', name="topologyalgorithms")
        node.createObject('TetrahedronSetGeometryAlgorithms', name="geometryalgorithms")
