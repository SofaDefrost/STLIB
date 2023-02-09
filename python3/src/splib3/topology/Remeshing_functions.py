#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 16:57:00 2022

@author: pchaillo
"""

# importing csv module
import csv
import numpy as np
from collections import OrderedDict

def default_indices(length):
    """
    Create a default indices tab # TODO : Choisir une convention et s'y tenir pour les docstings

    INPUT:
    length : length of the default indices tab

    OUTPUT :
    indices : tab that contain default indices [0 to len-1]

    """
    return [k for k in range(length)]
     

def index_from_axis(points,axis,old_indices = None): # 
    """
    Function to order points along an axis. The points would be sorted in the crescent way aong this axis

    INPUT :
    - Points : Tab that contains the points you want to order (format [x,y,z])
    - axis (axis along which you want to order your points) [ 0 => x //  axis = 1 => y  // axis = 2 => z  ]
    - old indices : tab that contains the indices of the points before the new ordering

    OUTPUT :
    - new_points : tableau des points dans le nouvel ordre
    - ind_tab : tab that contains [old_indices] at new indices position. Liste des anciens indices des points, triés dans le nouvel ordre
        """
    if old_indices == 'null':
        raise DeprecationWarning("Attention, old_indices est à 'null', the new norm is old_indices = None")
        # old_indices == None

    if old_indices is None :
        old_indices = default_indices(len(points))


    
    # print(len(points))
    # print(len(old_indices))

    if len(points) != len(old_indices):
        # print(len(points))
        # print(len(old_indices))
        raise RuntimeError("Be carefull, the number of points and indices are not coherent in index_from_axis(), so it will create false results ! ")
    
    conv_tab=[]
    for i in range(len(points)):
          conv_tab.append([points[i],old_indices[i]])
          
    new_points = sorted (points, key=lambda item: (item [axis]))

    conv_tab_sorted = sorted(conv_tab,key=lambda item: (item [0][axis]))

    ind_tab = []
    for i in range(len(conv_tab_sorted)):
        ind_tab.append(conv_tab_sorted[i][1])

    return (new_points, ind_tab) # contain the points in the new order and the old associated index

def reindex_mesh(ind_tab,mesh):  # fusion des fonctions reindex_mesh() et new_idx_from_conv_tab() ?
    """
    To change mesh indices, by changing the number from ind_tab. If the element 212 is at 3rd position in the ind_tab, the indices 212 will be replace by indices 3 in the mesh file, to keep indices and new mesh coherent.

    INPUT :
    - ind_tab : tab that contains [old_indices] at new indices position (format [old_indices] from index_from_axis() fcn )
    - mesh : mesh that you want to change indices

    OUTPUT :
    new_mesh : the same mesh but with indices that make reference to the new point tab
    """
    sort_index = np.array(ind_tab,dtype = object)
    
    new_mesh = []
    for i in mesh :
         element = i
         new_element = []
         for j in element :
             pt = j
             value_inx = np.where( sort_index == pt ) # where function find where the sort_index tab is equal to the pt variable, and record the position in the sort_index in the bariable value_inx
             value_idx = value_inx[0]
             try:
                value_i = value_idx[0]
             except IndexError as e:
                e.add_note("Element / point of the mesh not founded in conversion tab (ind_tab) in reindex_mesh() fcn #008") # add a commentary to the exception
                raise
             new_element.append(value_i)
         new_mesh.append(new_element)

    return new_mesh

def conv_tab_from_ind_tab(ind_tab): 
    conv_tab = []
    for i in range(len(ind_tab)):
        # conv_tab.append([ind_tab[i],i])
        conv_tab.append([i,ind_tab[i]])
    return conv_tab

def new_idx_from_conv_tab(mesh,conv_tab): # fusion des fonctions reindex_mesh() et new_idx_from_conv_tab() ?
    """
    Function to convert the mesh indices from a convertion tab

    INPUT :
    mesh = mesh you want to convert
    tab = conversion tab (format [new_indices , old_indices])

    OUTPUT :
    new_mesh
    """
    lonely_tab = []
    for j in range(len(conv_tab)):
        lonely_tab.append(conv_tab[j][0])
    lonely_tab = np.array(lonely_tab)
    l = len(mesh)
    new_mesh = []
    for i in range(l):
        element = []
        nb_pt = len(mesh[i])
        for k in range(nb_pt):
            value_inx = np.where(lonely_tab  == (mesh[i][k]) )
            value_idx = value_inx[0]
            try :
                value_i = value_idx[0]
            except:
                print("\n\n Valeur non trouvée, conversion aux nouveaux indices impossible \n\n ")
                value_i = value_idx[0]
            element.append(conv_tab[value_i][1])
        new_mesh.append(element)
    return new_mesh  


def quad_2_triangles(quads) :
    """
    To convert quads mesh to triangles mesh with keeping the same normals
    """
    triangles = []
    for q in quads :
        t1 = [q[0], q[1], q[2]]
        t2 = [q[2], q[3], q[0]]
        triangles.append(t1)
        triangles.append(t2)
    return triangles

def circle_detection_regular(points, pt_per_slice,indices=None):
    """
    Code to separate each step of a cylinder (so it's circles) (the goal is then to put spring in SOFA, to constrain a cavity)

    Only work for regular cylinder, with their points already sorted along the good axis

    INPUT :
    - points = points list
    - pt_per_slice = number of points per slices

    OUTPUT :
    - points_tab = tab of points, sorted by circles
    - ind_tab = indices tab, sorted by circles
    """
    if indices is None :
        indices = default_indices(len(points))
    
    nb_slice = len(points)/pt_per_slice
    
    if nb_slice!=np.ceil(nb_slice):
        print("\n \n \n Warning : the total number of points and the number per stage are not coherent in circle_detection() function (SPLIB in STLIB) \n \n \n")
    
    ind_tab = [] 
    points_tab = []
    dec = 0
    for i in range(int(nb_slice)):
        circle = points[dec:dec+pt_per_slice]
        indi = indices[dec:dec+pt_per_slice]
        dec = dec + pt_per_slice
        points_tab.append(circle)
        ind_tab.append(indi)
        
    return [points_tab, ind_tab]

def circle_detection_axis(points, axis,tolerance=0,indices=None):
    """
    Code to separate each step of a cylinder (so it's circles) (the goal is then to put spring in SOFA, to constrain a cavity)

    Should work every cavity, even not regular. Anyway you will have to order first yours points along an axis

    INPUT :
    - points = points list
    - axis (axis along which the points are already sorted) [ 0 => x //  axis = 1 => y  // axis = 2 => z  ]
    - tolerance = minimum value between two different step of a cylinder

    OUTPUT :
    - points_tab = tab of points, sorted by circles
    - ind_tab = indices tab, sorted by circles
    """

    [new_points, conv_tab] = index_from_axis(points = points, axis = axis, old_indices = indices) # tri intégré à la fonction ?

    points_tab = []
    circle_points = []
    circles_ind = []
    ind_tab=[]
    circle_points.append(new_points[0])
    circles_ind.append(conv_tab[0])
    for i in range(len(new_points)-1) :
        # print(i)
        # print( [new_points[i+1][axis], new_points[i][axis] - tolerance])
        if new_points[i+1][axis] >= new_points[i][axis] - tolerance  and new_points[i+1][axis] <= new_points[i][axis] + tolerance :
            circle_points.append(new_points[i+1])
            circles_ind.append(conv_tab[i+1])
        else :
            points_tab.append(circle_points)
            ind_tab.append(circles_ind)
            circle_points = []
            circles_ind = []
            circle_points.append(new_points[i+1])
            circles_ind.append(conv_tab[i+1])
    points_tab.append(circle_points)
    ind_tab.append(circles_ind)

    return [points_tab, ind_tab]

def remesh_from_axis(points,mesh,axis,old_indices = None):
    """
    Function to remesh a model : 
    1 - Will order the points list alon an axis  ( function index_from_axis() )
    2 - Adapt the mesh indices to this new order ( function reindex_mesh() )
    3 - Create a new conv_tab to know the link between the old and the indices of the points

    INPUT : 
    points = liste de points à réordonner
    mesh = maillage a remesher
    axis = axe selon lequel on veut réordonner les points [ 0 -> x / 1 -> y / 2 -> z ]
    old_indices = donne les anciens indices aux cas ou ils auraient déjà été modifiés

    OUTPUT : 
    new_points = liste de points dans le nouvel ordre (celui de l'axe axis)
    conv_tab = tableau d'équivalence entre les nouveaux et les anciens points
    new_mesh = nouveau maillage avec les nouveaux indices réorodnnés
    """
    if old_indices is None :
        old_indices = default_indices(len(points))
    new_points, ind_tab = index_from_axis(points = points, axis = axis,old_indices = old_indices)
    new_mesh = reindex_mesh(ind_tab=ind_tab,mesh=mesh)
    return [new_points, ind_tab ,new_mesh]

def ordering_circle(circle,ind_tab,x_ref=1,y_ref=2): #
    """To order all the points of a circles in clockwise

    Method :
    Calculate 1st the central points, the use this center to split in 2 the circle along x axis
    Then half of the circle will be sorted along crescent x axis, and the other hald in descending along x.

    INPUT :
    circle = tab that contains all the points of the circle
    ind_tab = indices tab
    x_ref and y_ref =  position of x and y axis to get the plane of the circles 

    OUTPUT :
    new_circle_pt = points of the circles, sorted in clockwise
    new_ind_tab =  new indices tab from the new ordering
    """
    l = len(circle)
    x_tab = []
    y_tab = []
    z_tab = []
    circle_with_ind = []
    for i in range(l):
        x_tab.append(circle[i][x_ref])
        y_tab.append(circle[i][y_ref])
#        z_tab.append(circle[i][2])
        circle_with_ind.append([ circle[i],ind_tab[i] ])
    
    center = [np.mean(x_tab),np.mean(y_tab)]
        
    tab_sup = []
    tab_inf = []
    for i in range(l):
        if circle[i][x_ref] > center[0]:
            tab_sup.append(circle_with_ind[i])
        else :
            tab_inf.append(circle_with_ind[i])
            
    tab_sup_ordre = sorted (tab_sup, key=lambda item: (item [0][y_ref]))
    tab_inf_ordre = sorted (tab_inf, key=lambda item: (item [0][y_ref]), reverse=True)
    
    new_circle_pt = []
    new_ind_tab = []
    for i in range(len(tab_sup_ordre)):
        new_circle_pt.append(tab_sup_ordre[i][0])
        new_ind_tab.append(tab_sup_ordre[i][1])
    for i in range(len(tab_inf_ordre)):
        new_circle_pt.append(tab_inf_ordre[i][0])
        new_ind_tab.append(tab_inf_ordre[i][1])
    
    return [new_circle_pt,new_ind_tab] # TODO : retirer tous les corchets aux return (+ les enlever lors des appels de la fonction)

def ordering_cylinder(circle_tab,ind_tab,axis = 0):
    """ 
    To put all the points of all circles of a cylinder in the clockwise order

    INPUT :
    circle_tab = tab that contains all the points of all circles, on line of the list represent on circle.
    ind_tab = indices tab
    OUTPUT :
    new_circle_tab = tab that contains all the circles of a cylinder, in the clockwise order
    new_ind_tab_full = new _ind tab
    """
    if axis == 0 :
        x_ref = 1
        y_ref = 2
    elif axis == 1 :
        x_ref = 0
        y_ref = 2
    elif axis == 2 :
        x_ref = 0
        y_ref = 1
    new_circle_tab = []
    new_ind_tab_full = []
    for i in range(len(circle_tab)) : 
        [new_circle_pt,new_ind_tab] = ordering_circle(circle = circle_tab[i],ind_tab = ind_tab[i],x_ref = x_ref,y_ref = y_ref)
        new_circle_tab.append(new_circle_pt)
        new_ind_tab_full.append(new_ind_tab)
    return [new_circle_tab,new_ind_tab_full]     

def invers_normal(mesh):
    """
    Invers the normal of all surfaces of a mesh
    """
    l = len(mesh)
    new_mesh = []
    for i in range(l):
        element = []
        nb_pt = len(mesh[i])
        for k in range(nb_pt):
            element.append(mesh[i][nb_pt-k-1])
        new_mesh.append(element)
    return new_mesh

def shift_tab(tab): 
    """
    To shift all the points of a tab oe time. The last value will become the 1st one
    """
    return  tab[1:]+ [tab[0]]

def closeSurface(ind_tab, reccur_bool = 0):
    """
    Create triangles to close a surface, by giving all the indices of the points at the edge

    INPUT :
    - ind_tab : indices of the points at the edge of the surface we want to close

    OUTPUT : 
    - triangles : triangles mesh to close the cavity
    """
#    if reccur_bool == 0 :
    triangles = []
    new_ind = []
    for k in range(0,len(ind_tab)-1,2) :
        # print(k)
        ind_a = k
        ind_b = k + 1
        ind_c = k + 2
        if ind_c > len(ind_tab)-1 :
            ind_c = 0

        triangles.append( [ ind_tab[ind_a] ,ind_tab[ind_b] ,ind_tab[ind_c] ] )
        new_ind.append(ind_tab[ind_a] )
        new_ind.append(ind_tab[ind_c] )
    
    new_ind = list(OrderedDict.fromkeys(new_ind))
    if len(new_ind) >= 3:
        new_triangles = closeSurface(ind_tab = new_ind, reccur_bool = 1)
        for tri in new_triangles :
            triangles.append(tri)

    return triangles
