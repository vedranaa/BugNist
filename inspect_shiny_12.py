'''Suitable to be run interactively or from a notebook.'''

#%%
import vtk_helpers as vh
import tifffile
import matplotlib.pyplot as plt
import glob
import os


    
#%%
foldername = '/Users/VAND/Documents/PROJECTS/BugNist/ILLUSTRATION2/_SHINY_TOP12'
filenames = sorted(glob.glob(foldername + '/*.tif*'))


#%% try volume rendering one volume
filename = filenames[0]
vol = tifffile.imread(filename)
vol_importer = vh.prepare_vol_data(vol)
actor = vh.prepare_volume_actor(vol_importer)
renderWindow = vh.prepare_renderer(actor, dims=vol.shape, windowSize=(100, 100))
image = vh.render_to_PIL(renderWindow)
image  # PIL image gets displayed


#%% surface rendering of the same volume
images = vh.render_to_PIL_views(renderWindow, vol.shape)
fig, ax = plt.subplots(1, len(images))
for a, i in zip(ax, images):
    a.imshow(i)


#%% surface rendering of all volumes

for filename in filenames:
    vol = tifffile.imread(filename)
    root = os.path.splitext(os.path.split(filename)[1])[0]

    vol_importer = vh.prepare_vol_data(vol)
    actor = vh.prepare_surface_actor(vol_importer)
    renderWindow = vh.prepare_renderer(actor, dims=vol.shape, windowSize=(150, 300))

    images = vh.render_to_PIL_views(renderWindow, vol.shape)
    fig, ax = plt.subplots(1, len(images))
    for a, i in zip(ax, images):
        a.imshow(i)
        a.axis("off")
    fig.suptitle(root)
    plt.show()

# %%
