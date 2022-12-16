import vtk
import PIL.Image
import io
import numpy as np


def save_screenshot(filename, renderWindow):
    ''' Save screenshot of the render window. '''
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renderWindow)
    w2if.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(filename)
    writer.SetInputData(w2if.GetOutput())
    writer.Write()


def prepare_vol_data(numpyVolume):
    ''' Prepare numpy volume to be imported in vtk. '''
    importer = vtk.vtkImageImport()
    importer.CopyImportVoidPointer(numpyVolume.tobytes(), numpyVolume.size)
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents(1)
    dims = numpyVolume.shape
    importer.SetDataExtent(0, dims[2]-1, 0, dims[1]-1, 0, dims[0]-1)
    importer.SetWholeExtent(0, dims[2]-1, 0, dims[1]-1, 0, dims[0]-1)
    return importer


def prepare_volume_actor(dataImporter, **kwargs):
    ''' Prepare for volume rendering of volumetric data. Accepts keyword 
    arguments: scalarOpacity, gradientOpacity, colorTransfer.'''
    
    # Color map settings.
    scalarOpacity = kwargs.get('scalarOpacity', 
            {0: 0.0, 100: 0.1, 255: 0.5})  # transparent dark, opaque bright
    gradientOpacity = kwargs.get('gradientOpacity', 
            {0: 0.0, 150: 1.0})  # transparent low-grad regions
    colorTransfer = kwargs.get('colorTransfer', 
            {0: (0.1, 0.1, 0.1), 255: (0.0, 0.0, 0.0)})

    volumeProperty = vtk.vtkVolumeProperty()
    
    # Opacity  transfer function.
    scalarOpacityFunc = vtk.vtkPiecewiseFunction()
    for point in scalarOpacity:
        scalarOpacityFunc.AddPoint(point, scalarOpacity[point])
    volumeProperty.SetScalarOpacity(scalarOpacityFunc)
            
    # Color transfer function.
    colorTransferFunc = vtk.vtkColorTransferFunction()
    for point in colorTransfer:
        colorTransferFunc.AddRGBPoint(point, colorTransfer[point][0], 
                colorTransfer[point][1], colorTransfer[point][2])
    volumeProperty.SetColor(colorTransferFunc)

    # Gradient opacity function (decrease opacity in constant-intensity regions).
    if gradientOpacity is not None:
        gradientOpacityFunc = vtk.vtkPiecewiseFunction()
        for point in gradientOpacity:
            gradientOpacityFunc.AddPoint(point, gradientOpacity[point])
        volumeProperty.SetGradientOpacity(gradientOpacityFunc)  

    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    return volume


def prepare_surface_actor(dataImporter, **kwargs):
    ''' Prepare for surface rendering of volumetric data. Accepts keyword 
    arguments: isovalue, diffuseColor.'''
    
    isovalue = kwargs.get('isovalue', 100)  
    diffuseColor = kwargs.get('diffuseColor', (0.5, 0.5, 0.5)) 
    
    surfaceExtractor = vtk.vtkMarchingCubes()
    surfaceExtractor.SetInputConnection(dataImporter.GetOutputPort())
    surfaceExtractor.SetValue(0, isovalue)  # contour number, contour value

    surfaceMapper = vtk.vtkPolyDataMapper()
    surfaceMapper.SetInputConnection(surfaceExtractor.GetOutputPort())
    surfaceMapper.ScalarVisibilityOff()

    surfaceActor = vtk.vtkActor()
    surfaceActor.SetMapper(surfaceMapper)
    
    if diffuseColor is not None:
        surfaceActor.GetProperty().SetDiffuseColor(diffuseColor[0], 
                        diffuseColor[1], diffuseColor[2])
    
    return surfaceActor


def prepare_renderer(actor, dims=None, **kwargs):
    ''' Prepare renderer to deal with volumetric data. '''
    # TODO Support for multiple actors; Returning renderer.
    
    # Settings. Alternative use c = actor.GetCenter().
    if dims is None:
        dims = (100, 100, 100)
    c = tuple(0.5 * (d - 1) for d in dims[-1::-1])  # center, focal point   

    windowName = kwargs.get('windowName', '')
    windowSize = kwargs.get('windowSize', (500, 500))
    backgroundColor = kwargs.get('backgroundColor', (1.0, 1.0, 1.0))
    focalPoint = kwargs.get('focalPoint', c)  
    cameraPosition = kwargs.get('cameraPosition', (c[0] + 1, c[1], c[2]))  # along x
    viewUp = kwargs.get('viewUp', (0, 0, 1))
    # resetCamera positions camera along view plane normal such that all actors are visible
    resetCamera = kwargs.get('resetCamera', True) 
    
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(*backgroundColor)
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName(windowName)
    renderWindow.SetSize(*windowSize)
        
    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(*focalPoint)
    camera.SetPosition(*cameraPosition)
    camera.SetViewUp(*viewUp)
    if resetCamera:
        renderer.ResetCamera() 
    #camera.Azimuth(30.0)
    #camera.Elevation(30.0)
    
    return renderWindow


def render_interactively(renderWindow):
 
    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    renderInteractor.SetRenderWindow(renderWindow)
    renderInteractor.Initialize()
    
    renderWindow.Render()
    renderInteractor.Start()
    return renderInteractor


def render_to_PIL(renderWindow):
    """
    Takes vtkRenderWindow instance and returns a PIL.Image with the rendering.
    """
    renderWindow.OffScreenRenderingOn() 
    renderWindow.Render()
    
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()
     
    writer = vtk.vtkPNGWriter()
    writer.WriteToMemoryOn()
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = memoryview(writer.GetResult())
    image = PIL.Image.open(io.BytesIO(data))
    return image

def render_to_PIL_views(renderWindow, dims):
    
    c = tuple(0.5 * (d - 1) for d in dims[-1::-1])   
    focalPoint = c  
    renderer = renderWindow.GetRenderers().GetFirstRenderer()
    viewUp = (0, 0, 1)
    positions = [(c[0] + d[0], c[1] + d[1], c[2]) 
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]]  # camera along x and y
    renderWindow.OffScreenRenderingOn() # NO SCREEN APPEARING, I'm not sure how this is to be used
    renderWindow.Render()
    camera = renderer.GetActiveCamera()

    images = []
    for n, p in enumerate(positions): 
    
        camera.SetFocalPoint(*focalPoint)
        camera.SetPosition(*p)
        camera.SetViewUp(*viewUp)
        renderer.ResetCamera()
        renderWindow.Render()
    
        windowToImageFilter = vtk.vtkWindowToImageFilter()
        windowToImageFilter.SetInput(renderWindow)
        windowToImageFilter.Update()
     
        writer = vtk.vtkPNGWriter()
        writer.WriteToMemoryOn()
        writer.SetInputConnection(windowToImageFilter.GetOutputPort())
        writer.Write()
        data = memoryview(writer.GetResult())
        images.append(PIL.Image.open(io.BytesIO(data)))
    
    return images


def save_view_screenshots(renderWindow, name, dims):
   
    # Alternative get hold of renderer and actor, e.g. c = actor.GetCenter()
    c = tuple(0.5 * (d - 1) for d in dims[-1::-1])   
    focalPoint = c  
    renderer = renderWindow.GetRenderers().GetFirstRenderer()
    viewUp = (0, 0, 1)
    positions = [(c[0] + d[0], c[1] + d[1], c[2]) 
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]]  # camera along x and y
    renderWindow.OffScreenRenderingOn() # NO SCREEN APPEARING, I'm not sure how this is to be used
    renderWindow.Render() 
    camera = renderer.GetActiveCamera()
    
    for n, p in enumerate(positions): 
    
        camera.SetFocalPoint(*focalPoint)
        camera.SetPosition(*p)
        camera.SetViewUp(*viewUp)
        renderer.ResetCamera() # positions camera along view plane normal such that all actors are visible
        save_screenshot(f'{name}_w{n}.png', renderWindow)

def threshold_otsu(image=None, nbins=256):
    """Return threshold value based on Otsu's method. Adapted from
    https://github.com/scikit-image/scikit-image/blob/70fa904eee9ef370c824427798302551df57afa1/skimage/filters/thresholding.py#L312
    """

    counts, bin_edges = np.histogram(image, nbins)
    bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

    # class probabilities for all possible thresholds
    weight1 = np.cumsum(counts)
    weight2 = np.cumsum(counts[::-1])[::-1]
    
    # class means for all possible thresholds
    mean1 = np.cumsum(counts * bin_centers) / weight1
    mean2 = (np.cumsum((counts * bin_centers)[::-1]) / weight2[::-1])[::-1]

    # Clip ends to align class 1 and class 2 variables:
    # The last value of ``weight1``/``mean1`` should pair with zero values in
    # ``weight2``/``mean2``, which do not exist.
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    idx = np.argmax(variance12)
    threshold = bin_centers[idx]

    return threshold