'''Usage from CL
    showbug filename
    showbug filename -surf
'''

import vtk_helpers as vh
import processing_helpers as ph  
import tifffile
import argparse

parser = argparse.ArgumentParser(description='Show bug saved in tif.')
parser.add_argument('filename')  
parser.add_argument('-s', '--surf', action='store_true')           
args = parser.parse_args()

vol = tifffile.imread(args.filename)
vol_importer = vh.prepare_vol_data(vol)

if args.surf:
    t = ph.threshold_otsu(vol)
    actor =  vh.prepare_surface_actor(vol_importer, isovalue=t)
else: 
    actor = vh.prepare_volume_actor(vol_importer)

renderWindow = vh.prepare_renderer(actor, dims=vol.shape)
renderInteractor = vh.render_interactively(renderWindow)
