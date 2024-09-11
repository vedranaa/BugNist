import vtk_helpers as vh
import glob
import tifffile
import os

#input_foldername = 'sample_data'
#screenshot_foldername = 'screenshots'

def process_folder(input_foldername, output_foldername):

    filenames = sorted(glob.glob(input_foldername + '/*.tif*'))
    for filename in filenames:
        root = os.path.splitext(os.path.split(filename)[1])[0]
    
        vol = tifffile.imread(filename)
        importer = vh.prepare_vol_data(vol)
        volume_actor = vh.prepare_volume_actor(importer)
        render_window = vh.prepare_renderer(volume_actor)
        vh.save_screenshots(render_window, 
                f'{output_foldername}/{root}_vol.png', vol.shape)


def proces_folders(input_foldername, output_foldername):

    fileslist = glob.glob(input_foldername)
    foldernames = sorted([f for f in fileslist if os.path.isdir(f)])



# %%
if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='Save screenshots for a folder.')
    parser.add_argument('input_foldername')  
    parser.add_argument('output_foldername')           
    args = parser.parse_args()
    process_folder(args.input_foldername, args.output_foldername)


