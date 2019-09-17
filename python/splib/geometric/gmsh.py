# -*- coding: utf-8 -*-
# This file requires gmshpy to be installed. 
# Author: stefan.escaida-navarro@inria.fr

"""
.. autosummary::

    meshFromParametricGeometry    

splib.geometric.gmsh.meshFromParametricGeometry
*********************
.. autofunction:: meshFromParametricGeometry

splib.geometric.gmsh.createScene
********************
.. autofunction:: createScene

"""

class LocaleManager:
    import locale
    def __init__(self, localename):
        self.name = localename
    def __enter__(self):
        self.orig = locale.setlocale(locale.LC_CTYPE)
        locale.setlocale(locale.LC_ALL, self.name)
    def __exit__(self, exc_type, exc_value, traceback):
        locale.setlocale(locale.LC_ALL, self.orig)
 
def meshFromParametricGeometry(filepath, outputdir='autogen', meshtype='Surface', **kwargs):
        """generate a tetrahedron and or a surface mesh from the provided file and store the 
           result in a volumetric (vtk) or surfacic file (stl, etc.). The path to the file is returned. 
           
           :param str filepath:
           :param str outputdir:
          
          Further parameters:
          
          This function accepts through the kwargs all options that can be set in Gmsh as found in the documentation:
          http://gmsh.info/doc/texinfo/gmsh.html
          The options in the referenced documentation are sorted into categories and separated by a point, e.g. "Mesh.CharacteristicLengthFactor". 
          The same option passed as kwarg is separated by an underscore, e.g. "Mesh_CharacteristicLengthFactor=0.8". See example below.
        """ 
        
        import splib.caching.cacher as cch
        import gmshpy        
        import os
        import numpy as np
        
        LM = LocaleManager('C')
        with LM:       
            # Set options from kwargs           
            OptionsStrings, Values = cch.extractOptions(kwargs)        
            
            for i in range(0, len(OptionsStrings)):            
                SplitStr = OptionsStrings[i].split('_')
                Category = SplitStr[0]
                Option = SplitStr[1]
                if isinstance(Values[i], basestring):  # need to be careful to call the correct function according to the type of value (string or numerical)
                    gmshpy.GmshSetStringOption(Category, Option, Values[i])
                else:
                    gmshpy.GmshSetNumberOption(Category, Option, Values[i])
                #Warning: these functions return no value to indicate success of setting an option!
                
            Refresh = False
            OutputFilePath = ''        
            FileNameWithExt = os.path.split(filepath)[1]
            FileNameNoExt = os.path.splitext(FileNameWithExt)[0]                
            
            #Refresh, OutputFilePath = casher(filepath, outputdir, '.stl', kwargs, FileNameNoExt)
                        
            if meshtype == 'Surface':            
                Refresh, OutputFilePath = cch.cacher(filepath, outputdir, '.stl', kwargs, FileNameNoExt)
            elif meshtype == 'Volumetric':            
                Refresh, OutputFilePath = cch.cacher(filepath, outputdir, '.vtk', kwargs, FileNameNoExt)
            

            if Refresh:
                print('Beginning meshing ...')
                GeometricModel = gmshpy.GModel()
                GeometricModel.load(filepath)
                if meshtype == 'Surface':
                    GeometricModel.mesh(2)
                elif meshtype == 'Volumetric':
                    GeometricModel.mesh(3)    
                GeometricModel.save(OutputFilePath)
                print('Finished meshing.')   
    
            return OutputFilePath

def createScene(root):
        """Example scene in SOFA, where the parametric mesh generator is used generate a volumetric mesh from a STEP-file while passing some options to Gmsh.          
        """ 
        from stlib.scene import Scene

        Scene(root)
        root.VisualStyle.displayFlags="showForceFields"

        # The list of mesh (e.g. Mesh_CharacteristicLengthFactor), geometry, view, etc. options can be found here: http://gmsh.info/doc/texinfo/gmsh.html, Appendix B
        filename = meshFromParametricGeometry(filepath='data/meshes/parametric_mesh_example.step', 
                                      outputdir='data/meshes/autogen/',
                                      meshtype='Volumetric',
                                      Mesh_CharacteristicLengthFactor=1, 
                                      Mesh_CharacteristicLengthMax=3, 
                                      Mesh_CharacteristicLengthMin=0.1, 
                                      View_GeneralizedRaiseZ='v0')
                                      
        root.createObject("MeshVTKLoader", name="loader", filename=filename)
        root.createObject("TetrahedronSetTopologyContainer", name="container", src="@loader")

        root.createObject("MechanicalObject", name="dofs", position="@loader.position")
        root.createObject("TetrahedronFEMForceField", name="forcefield")                              

