#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 16:57:00 2022

@author: pchaillo
"""

# importing csv module
import csv
import numpy as np

def default_indices(length):
    """
    Crée un tableau d'indice par défaut

    INPUT:
    length : length of the default indices tab

    OUTPUT :
    indices : tab that contain default indices [0 to len-1]

    """
    indices = [k for k in range(length)]
    return indices

def index_from_axis(points,axis,old_indices = "null"): # 
    """
    Fonction pour réindexer (réordonner) des points celon un axe. Les points seront triés dans l'ordre croissant selon cet axe.

    INPUT :
    - Points : tableau de points à réordonner
    - axis (axe selon lequel on veut trier les points celon l'ordre croissant) = 0 => x //  axis = 1 => y  // axis = 2 => z 
    - old indices : tableau des indices des points passés en argument

    OUTPUT :
    - new_points : tableau des points dans le nouvel ordre
    - conv_tab_final : tableau qui contient : [old_indices] at new indices position. Liste des anciens indices des points, triés dans le nouvel ordre
    (Remplacer par )
    """
    ###### Pour trier les points et enregistrer les indices   ##### #001    

    if old_indices == "null" :
        old_indices = default_indices(len(points))
    
    if len(points) != len(old_indices):
        print("Attention, le  nombre de points et le nombre d'indices est différent => les données ne sont pas valides")
    
    conv_tab=[]
    for i in range(len(points)):
          conv_tab.append([points[i],old_indices[i]])
          
    new_points = sorted (points, key=lambda item: (item [axis]))
    # new_points_final = np.array(new_points) # Conversion de liste à tableau => vraiment utile ?

    conv_tab_sorted = sorted(conv_tab,key=lambda item: (item [0][axis]))

    conv_tab_final = []
    for i in range(len(conv_tab_sorted)):
        conv_tab_final.append(conv_tab_sorted[i][1])

    # print(conv_tab_final)

    return [new_points, conv_tab_final] # contain the points in the new order and the old associated index

def reindex_mesh(conv_tab,mesh):
    """
    Pour changer les indices d'un mesh, en remplacant par les indices du nouveau tableau trié

    INPUT :
    - conv_tab : tableau des points avec les positions et les indices (format [old_indices] de la fonction précédente)
    - mesh : maillage dont on veut changer les indices

    OUTPUT :
    new_mesh : the same mesh but with indices that make reference to the new point tab
    """
    
    # sort_index = []
    # ind = 0
    # for x in conv_tab:
    #      sort_index.append(x[1]) # sort index good :) :) :) 
    #      # sort_index2.append((x[1],ind)) # ind pas utile finalement
    #      ind += 1
          
    # print(sort_index)
    sort_index = np.array(conv_tab)
    
    new_mesh = []
    for i in mesh :
         element = i
         new_element = []
         for j in element :
             pt = j
             # print(pt)
             value_inx = np.where( sort_index == pt )
             # print(value_inx)
             value_idx = value_inx[0]
             # print(value_idx)
             try:
                # print("what")
                value_i = value_idx[0]
             except:
                print("\n \n Element / point du maillage non trouvé dans le tableau de conversion #008 \n \n")
                value_i = value_idx[0]
             new_element.append(value_i)
         new_mesh.append(new_element)

    return new_mesh


def quad_2_triangles(quads) :
    """
    To convert quads to triangles with keeping the same normals
    """
    triangles = []
    for q in quads :
        t1 = [q[0], q[1], q[2]]
        t2 = [q[2], q[3], q[0]]
        triangles.append(t1)
        triangles.append(t2)
    return triangles

def circle_detection_regular(points, pt_per_slice,indices="null"):
    """
    Code pour relier chaque disque ensemble (pour à termes y mettre des ressorts dans SOFA)

    Ne fonctionne que pour les cylindres réguliers, déjà trié selon le bon axe, avec un nombre constant et connu de points par étages

    INPUT :
    - points = liste des points
    - pt_per_slice = numbre of points per slices

    OUTPUT :
    - points_tab = tableau des points, triés par cercles
    - ind_tab = tableau des indices, triés par cercles
    """
    if indices == "null" :
        indices = default_indices(len(points))
    
    nb_slice = len(points)/pt_per_slice
    
    if nb_slice!=np.ceil(nb_slice):
        print("\n \n \n Warning : the total number of points and the number per stage are not coherent in 'circle_detection' function (SPLIB in STLIB) \n \n \n")
    
    ind_tab = [] # tableau des indices
    points_tab = []
    dec = 0
    for i in range(int(nb_slice)):
        circle = points[dec:dec+pt_per_slice]
        indi = indices[dec:dec+pt_per_slice]
        dec = dec + pt_per_slice
        points_tab.append(circle)
        ind_tab.append(indi)
        
    return [points_tab, ind_tab]

def circle_detection_axis(points, axis,tolerance=0,indices="null"):
    """
    Code pour relier chaque disque ensemble (pour à termes y mettre des ressorts dans SOFA)

    Doit fonctionner pour toutes les cavités, même irrégulières

    INPUT :
    - points = liste des points
    - axis = 0=x / 1=y / 2=z
    - tolerance = valeur de laquelle il faut différer pour être considéré comme l'étage suivant

    OUTPUT :
    - points_tab = tableau des points, triés par cercles
    - ind_tab = tableau des indices, triés par cercles
    """
    # if indices == "null" :
    #     indices = default_indices(len(points))
    
    [new_points, conv_tab] = index_from_axis(points = points, axis = axis, old_indices = indices)

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

def remesh_from_axis(points,mesh,axis,old_indices = "null"):
    """
    Fonction pour remesher un maillage : 
    1 - Remettre la liste des points dansn un nouvel ordre ( fonction new_index() )
    2 - Changer les indices du maillage pour qu'il correspondent à cette nouvelle liste de points ( fonction reindex_mesh() )
    3 - crée un nouveau tableau pour avoir les équivalences entre les anciens et les nouveaux index des points

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
    if old_indices == "null" :
        old_indices = default_indices(len(points))
    [new_points, conv_tab] = index_from_axis(points = points, axis = axis,old_indices = old_indices)
    new_mesh = reindex_mesh(conv_tab=conv_tab,mesh=mesh)
    return [new_points, conv_tab ,new_mesh]

def close_cavity(circles,ind_tab): # dirty => you may do better my boy
    """
    Fonction qui en fonction des cercles, va créer les triangles pour fermer le maillage du cylindre aux extrémités

    INPUT : 
    circles = tableau qui contient les cercles du cylindre (tableau de tous les indices des points, un ligne du tableau représentant un cercle
    ind_tab = tableau des indices 

    OUTOUT :
    new_triangles = tableau des triangles à ajouter pour fermer les cylindres
    """
    circle_bottom = circles[0]
    ind_bottom = ind_tab [0]
    # print(ind_bottom)
    l = len(circles)
    circle_top = circles[l-1]
    ind_top = ind_tab[l-1]
    print(ind_top)
    print(len(ind_top))
    
    new_triangles = []
    nb_pt_per_slices = len(ind_top)
    print(nb_pt_per_slices)
    for i in range(6):
        i = i*2
        print(i)
        ind_a = i
        ind_b = i + 2
        ind_c = i + 1
        # print([ind_a,ind_b,ind_c])
        if ind_b == np.ceil(nb_pt_per_slices):
            # print("Y ALLONS NOUS ? je vais savoir bientpot")
            ind_b = 0
        print([ind_a,ind_b,ind_c])
        
        new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
        new_triangles.append( [ ind_bottom[ind_a] ,ind_bottom[ind_b] ,ind_bottom[ind_c] ] )
        
        ind_a = 0
        ind_b = 10
        ind_c = 2
        new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
        new_triangles.append( [ ind_bottom[ind_a] ,ind_bottom[ind_b] ,ind_bottom[ind_c] ] )
        
        ind_a = 4
        ind_b = 8
        ind_c = 6
        new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
        new_triangles.append( [ ind_bottom[ind_a] ,ind_bottom[ind_b] ,ind_bottom[ind_c] ] )
        
        ind_a = 4
        ind_b = 2
        ind_c = 10
        new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
        new_triangles.append( [ ind_bottom[ind_a] ,ind_bottom[ind_b] ,ind_bottom[ind_c] ] )
        
        ind_a = 10
        ind_b = 4
        ind_c = 8
        new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
        new_triangles.append( [ ind_bottom[ind_a] ,ind_bottom[ind_b] ,ind_bottom[ind_c] ] )
    
    return new_triangles

def close_cavity_2(ind_top,ind_bottom): # dirty => you may do better my boy
    """
    Fonction qui en fonction des cercles, va créer les triangles pour fermer le maillage du cylindre aux extrémités

    INPUT : 
    ind_top = indices du cercle à l'extrémité supérieure du cylindre
    ind_bottom = indices du cercle à l'extrémité inférieure du cylindre

    OUTOUT :
    new_triangles = tableau des triangles à ajouter pour fermer les cylindres
    """
    
    new_triangles = []
    nb_pt_per_slices = len(ind_top)
    # print(nb_pt_per_slices)
    for i in range(6):
        i = i*2
        # print(i)
        ind_a = i
        ind_b = i + 2
        ind_c = i + 1
        # print([ind_a,ind_b,ind_c])
        if ind_b == np.ceil(nb_pt_per_slices):
            # print("Y ALLONS NOUS ? je vais savoir bientpot")
            ind_b = 0
        # print([ind_a,ind_b,ind_c])
        
        new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
        new_triangles.append( [ ind_bottom[ind_c] ,ind_bottom[ind_b] ,ind_bottom[ind_a] ] )
        
    ind_a = 0
    ind_b = 10
    ind_c = 2
    new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
    new_triangles.append( [ ind_bottom[ind_c] ,ind_bottom[ind_b] ,ind_bottom[ind_a] ] )
    
    ind_a = 4
    ind_b = 8
    ind_c = 6
    new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
    new_triangles.append( [ ind_bottom[ind_c] ,ind_bottom[ind_b] ,ind_bottom[ind_a] ] )
    
    ind_a = 2
    ind_b = 10
    ind_c = 4
    new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
    new_triangles.append( [ ind_bottom[ind_c] ,ind_bottom[ind_b] ,ind_bottom[ind_a] ] )
    
    ind_a = 4
    ind_b = 10
    ind_c = 8
    new_triangles.append( [ ind_top[ind_a] ,ind_top[ind_b] ,ind_top[ind_c] ] )
    new_triangles.append( [ ind_bottom[ind_c] ,ind_bottom[ind_b] ,ind_bottom[ind_a] ] )
    
    return new_triangles

def ordering_circle(circle,ind_tab,x_ref=1,y_ref=2): #
    """
    Pour remettre les points d'un cercle dans le sens horaire ou anti-horaire.
    Récupère le point central, puis s'en sert pour coupe le cercle en deux selon x
    Ensuite une moitié trié avec les y croissant, puis l'autre avec les y décroissants

    INPUT :
    circle = tableau qui contient tous les points d'un cercle
    ind_tab = tableau des indices
    x_ref and y_ref =  positions des coordonnées x et y (du plan du cercle) dans le tableau de point circle

    OUTPUT :
    new_circle_pt = Nouveau cercle réordonné
    new_ind_tab =  nouveau tableau d'indices associés
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
    
#    print(x_tab)
#    center = [np.mean(x_tab),np.mean(y_tab),np.mean(z_tab)]
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

    print("RRRRR")
    print([tab_sup_ordre, tab_inf_ordre])
    
    new_circle_pt = []
    new_ind_tab = []
    for i in range(len(tab_sup_ordre)):
        new_circle_pt.append(tab_sup_ordre[i][0])
        new_ind_tab.append(tab_sup_ordre[i][1])
    for i in range(len(tab_inf_ordre)):
        new_circle_pt.append(tab_inf_ordre[i][0])
        new_ind_tab.append(tab_inf_ordre[i][1])
    
    return [new_circle_pt,new_ind_tab]

def ordering_cylinder(circle_tab,ind_tab):
    """ 
    Pour remettre tous les cercles successif d'un cylindre dans le sens horaire
    Va découper les cercles et les réordonner un par un avec la fonction ordering_circles() 

    INPUT :
    circle_tab = tableau qui contient les cercles du cylindre (tableau de tous les indices des points, un ligne du tableau représentant un cercle
    ind_tab = tableau des indices associés
    
    OUTPUT :
    new_circle_tab = tableau qui contient les cercles du cylindre (dans le sens horaire)
    new_ind_tab_full = nouveau tableau des indices
    """
    new_circle_tab = []
    new_ind_tab_full = []
    for i in range(len(circle_tab)) : 
        [new_circle_pt,new_ind_tab] = ordering_circles(circle = circle_tab[i],ind_tab = ind_tab[i])
        new_circle_tab.append(new_circle_pt)
        new_ind_tab_full.append(new_ind_tab)
    return [new_circle_tab,new_ind_tab_full]     

def invers_normal(mesh):
    """
    Inverse les normales d'un maillage
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

def new_idx_from_conv_tab(mesh,tab):
    lonely_tab = []
    for j in range(len(tab)):
        lonely_tab.append(tab[j][0])
    lonely_tab = np.array(lonely_tab)
    l = len(mesh)
    new_mesh = []
    # print(lonely_tab)
    for i in range(l):
        element = []
        nb_pt = len(mesh[i])
        for k in range(nb_pt):
            # print("Looking for : ") ## pour savoir quel point n'est pas trouvé
            # print(mesh[i][k])
            value_inx = np.where(lonely_tab  == (mesh[i][k]) )
            # print(value_inx)
            value_idx = value_inx[0]
            # print(value_idx)
            value_i = value_idx[0]
            element.append(tab[value_i][1])
        new_mesh.append(element)
    return new_mesh  

def shift_tab(tab): # pour décaler tous les éléments d'un tableau de 1, pour pouvoir placer les ressorts
    l = len(tab)
    new_tab = []
    for t in range(l-1) :
        new_tab.append(tab[t+1])
    new_tab.append(tab[0])
    return new_tab
