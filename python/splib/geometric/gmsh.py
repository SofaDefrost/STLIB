# -*- coding: utf-8 -*-
# This file requires gmshpy to be installed. 
# Author: stefan.escaida-navarro@inria.fr

def extractOptions(kwargsdict):
    
    OptionsStrings = []
    Values = []
        
    for key, value in kwargsdict.items():
        OptionString = key
        OptionValue = value    
        OptionsStrings.append(OptionString)
        Values.append(OptionValue)
    
    return OptionsStrings, Values

def casher(InputFilePath, OutputDir, OutputFileExtension, kwargsdict, OutputFileName=None):
# This is a first, simple version of a cashing system that takes a file and a list of arguments (through the kwargs) and:
# - generates a hash from the file content and the arguments
# - checks in the target directory if an output has been already generated from the inputs using the hash
# - returns a name under which the calling function can store or retrieve the generated data (that it will be managed by the casher in future calls)
# It has two types of behavior:
# - OneShot --> When an output filename is provided, the old file is replaced by the new one, the filename is 'human-readable'. This is a cache of size 1
# - Persistent --> Previous files are not overwritten, the files are named with the hash string. In this way the all the generated files with different parameters are 'cached'
    import os
    import hashlib
    import numpy as np
    
    if not os.path.isdir(OutputDir):
        os.mkdir(OutputDir)
        
    
    OptionsStrings, Values = extractOptions(kwargsdict)
    
    # Hashing
    SortingIdxs = np.argsort(OptionsStrings) # sort options by name to be insensitive to the order they are passed    
    ParametricGeometryFile = open(InputFilePath)
    # Warning: here we are not taking into account that the file could use a large amount of memory
    FileContents = ParametricGeometryFile.read()
    
    # hash the file contents
    FileAndOptionsHashObj = hashlib.sha256(FileContents)
    
    # add the options strings to the hash
    for i in SortingIdxs:
        ArgsForHash = OptionsStrings[i] + '=' + str(Values[i]) + ';'
        FileAndOptionsHashObj.update(ArgsForHash)
    
    # Finally, add output file extension to the hash, so that different target files from the same source will be treated differently (e.g. Surface and Volumetric meshes)
    FileAndOptionsHashObj.update(OutputFileExtension)
    
    # Get the hash string and verify if it was previously generated    
    HashStr = FileAndOptionsHashObj.hexdigest()    
    # OneShot
    if OutputFileName != None: 
        HashFilePath = OutputDir + OutputFileName + OutputFileExtension + '.hash'
        FilePath = OutputDir + OutputFileName + OutputFileExtension 
        if os.path.exists(HashFilePath):
            HashFileRead = open(HashFilePath,'r')
            OldHashStr = HashFileRead.readline()
            if OldHashStr == HashStr+'\n':
                print(FilePath + ': Found a file with an identical hash. Returning from cache.')                
                return False, FilePath
        
        # If hash is different or non-existent write hash (+options) info to file                 
        HashFile = open(HashFilePath, 'w+')
        HashFile.write(HashStr+'\n')
        HashFile.write('# Options:\n')
                       
        for i in SortingIdxs:
                HashFile.write('# ' + OptionsStrings[i]+'='+str(Values[i])+';\n')
        HashFile.close()
        return True, FilePath
    
    
    # Persistent
    else:
        HashedFileName = HashStr + OutputFileExtension
        HashedFilePath = OutputDir + HashedFileName
        if os.path.exists(HashedFilePath):    
            print(HashedFilePath + ': Found a file with an identical hash. Returning from cache.')                
            return False, HashedFilePath
        else:
            return True, HashedFilePath

    
def meshFromParametricGeometry(filepath, outputdir='autogen', meshtype='Surface', **kwargs):
        """generate a tetrahedron mesh from the provided file and store the 
           result in a vtk file. The filename is returned. 
           
           :param str filepath:
           :param str outputdir:
           :param float Mesh_CharacteristicLengthFactor:
           :param float Mesh_CharacteristicLengthMax:
           :param float Mesh_CharacteristicLengthMin: 
           :param float View_GeneralizedRaiseZ
        """ 
        import gmshpy        
        import os
        import numpy as np
        import locale
        locale.setlocale(locale.LC_ALL, 'C')

        # Set options from kwargs
       
        OptionsStrings, Values = extractOptions(kwargs)        
        
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
        
        print(OutputFilePath)
        if meshtype == 'Surface':            
            Refresh, OutputFilePath = casher(filepath, outputdir, '.stl', kwargs, FileNameNoExt)
        elif meshtype == 'Volumetric':            
            Refresh, OutputFilePath = casher(filepath, outputdir, '.vtk', kwargs, FileNameNoExt)
        
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
        from stlib.scene import Scene

        Scene(root)
        root.VisualStyle.displayFlags="showForceFields"

        # The list of mesh (e.g. Mesh_CharacteristicLengthFactor), geometry, view, etc. options can be found here: http://gmsh.info/doc/texinfo/gmsh.html, Appendix B
        filename = meshFromParametricGeometry(filepath='/home/stefan/Downloads/Cube.stl', 
                                      outputdir='data/meshes/autogen/',
                                      meshtype='Volumetric',
                                      Mesh_CharacteristicLengthFactor=0.4, 
                                      Mesh_CharacteristicLengthMax=3, 
                                      Mesh_CharacteristicLengthMin=0.1, 
                                      View_GeneralizedRaiseZ='v0')
                                      
        root.createObject("MeshVTKLoader", name="loader", filename=filename)
        root.createObject("TetrahedronSetTopologyContainer", name="container", src="@loader")

        root.createObject("MechanicalObject", name="dofs", position="@loader.position")
        root.createObject("TetrahedronFEMForceField", name="forcefield")                              

