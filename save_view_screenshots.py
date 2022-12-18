#%%
import vtk_helpers as vh
import glob
import tifffile
import os

input_foldername = 'sample_data'
screenshot_foldername = 'screenshots'
filenames = sorted(glob.glob(input_foldername + '/*.tif*'))

#%%

for filename in filenames:
    root = os.path.splitext(os.path.split(filename)[1])[0]
 
    vol = tifffile.imread(filename)
    importer = vh.prepare_vol_data(vol)
    volume_actor = vh.prepare_volume_actor(importer)
    render_window = vh.prepare_renderer(volume_actor)
    vh.save_view_screenshots(render_window, 
            f'{screenshot_foldername}/{root}_vol.png', vol.shape)
    
    surface_actor =  vh.prepare_surface_actor(importer)
    render_Window = vh.prepare_renderer(surface_actor)
    vh.save_view_screenshots(render_window, 
            f'{screenshot_foldername}/{root}_surf.png', vol.shape)


# %%
