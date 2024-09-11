'''Suitable to be run interactively or from a notebook.'''

#%%
import vtk_helpers as vh
import tifffile
import glob
import os
import vtk


#%% Try meshing a single volume
foldername = '/Users/VAND/Documents/PROJECTS/BugNist/ILLUSTRATION2/_SHINY_TOP12'
filenames = sorted(glob.glob(foldername + '/*.tif*'))
filename = filenames[0]

filename_mesh = os.path.splitext(filename)[0] + '.ply'
filename_mesh = filename_ply.replace('TOP12', 'MESHES')
vol = tifffile.imread(filename)
surface = vh.mesh_volume(vol, isovalue=40, connected=True, smooth=10, decimate=0.75, fill=5)
vh.save_mesh(surface, filename_mesh)

#%% I can't get it to work with the same settings for all volumes

# For isovalue to be low, I need to remove cotton so I crop the volume
isovalue = {}
crop = {}   
for filename in filenames:
    abbreviation = os.path.split(filename)[1][:2]
    isovalue[abbreviation] = 40
    crop[abbreviation] = 0

isovalue['BF'] = 35
isovalue['BL'] = 65
isovalue['BP'] = 55
isovalue['CF'] = 45
isovalue['PP'] = 55

crop['BF'] = 100
crop['BL'] = 100
crop['CF'] = 150  
crop['PP'] = 150  

for filename in filenames:
    abbreviation = os.path.split(filename)[1][:2]
    filename_mesh = os.path.splitext(filename)[0] + '.stl'
    filename_mesh = filename_mesh.replace('TOP12', 'MESHES')
    vol = tifffile.imread(filename)

    if crop[abbreviation] > 0:
        vol = vol[crop[abbreviation]:-crop[abbreviation]]

    surface = vh.mesh_volume(vol, 
                            isovalue=isovalue[abbreviation], 
                            connected=True, 
                            smooth=10, 
                            decimate=0.5, 
                            fill=5)
    vh.save_mesh(surface, filename_mesh)

# %%
