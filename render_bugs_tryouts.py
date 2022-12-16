
import vtk_helpers as vh
import processing_helpers as ph  
import tifffile 

#%% SHOW VOLUME
filename = 'out/bug_00.tiff'
filename = ('/dtu/3d-imaging-center/projects/2022_QIM_55_BugNIST/analysis/'
        'code/out_fullsize_masked/bug_00.tiff')
filename = ('/Volumes/3dimage/projects/2022_QIM_55_BugNIST/analysis/code/'
        'out_fullsize_masked/bug_00.tiff')
filename = ('/dtu/3d-imaging-center/projects/2022_QIM_55_BugNIST/analysis/'
        'annotations/out_automatic_masked/pack20221204-3_003.tif')
filename = ('/Volumes/3dimage/projects/2022_QIM_55_BugNIST/analysis/'
        'annotations/out_automatic_masked/pack20221204-3_007.tif')


filename = '/Users/VAND/Documents/PROJECTS/BugNist/sample_data/pack20221204-1_014.tif'

vol = tifffile.imread(filename)
#%%
vol_importer = vh.prepare_vol_data(vol)

#% CHOSE VOLUME ACTOR OR SURFACE ACTOR
#actor = vh.prepare_volume_actor(vol_importer)
t = ph.threshold_otsu(vol)
actor =  vh.prepare_surface_actor(vol_importer, isovalue=t)
renderWindow = vh.prepare_renderer(actor, dims=vol.shape)
renderInteractor = vh.render_interactively(renderWindow)


#%% SAVE SCREENSHOTS
#bugnames = [f'bug_{i:02d}' for i in range(42)]

#for bugname in bugnames:
    
#    print(bugname)

#    vol = tifffile.imread(f'out_fullsize_masked/{bugname}.tiff')
    
#    importer = prepare_vol_data(vol)
#    volume_actor = prepare_volume_actor(importer)
#    render_window = prepare_renderer(volume_actor)
#    save_view_screenshots(render_window, f'screenshots_fullsize/{bugname}_vol')
    
#    surface_actor =  prepare_surface_actor(importer)
#    renderWindow = prepare_renderer(surface_actor)
#    save_view_screenshots(renderWindow, f'screenshots_fullsize/{bugname}_surf')
