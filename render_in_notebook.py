'''Suitable to be run interactively or from a notebook.'''

#%%
import vtk_helpers as vh
import tifffile
import matplotlib.pyplot as plt
import glob
import os


    
#%%
filename = '/Users/VAND/Documents/PROJECTS/BugNist/sample_data/pack20221204-1_014.tif'
vol = tifffile.imread(filename)
vol_importer = vh.prepare_vol_data(vol)
actor = vh.prepare_volume_actor(vol_importer)
renderWindow = vh.prepare_renderer(actor, dims=vol.shape, windowSize=(100, 100))
image = vh.render_to_PIL(renderWindow)
image  # PIL image gets displayed


# %%
images = vh.render_to_PIL_views(renderWindow, vol.shape)
fig, ax = plt.subplots(1, len(images))
for a, i in zip(ax, images):
    a.imshow(i)

# %%
foldername = 'sample_data'
filenames = sorted(glob.glob(foldername + '/*.tif*'))

#%%

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
