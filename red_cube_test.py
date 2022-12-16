"""
Created on Fri May 22 22:46:16 2020
@author: vand
Very simple vtk example, inspired by:
https://lorensen.github.io/VTKExamples/site/Python/GeometricObjects/
"""
import vtk

#%% SOURCE
# Generate polygon data for a cube.
cube = vtk.vtkCubeSource()

#%% MAPPER
# Create a mapper for the polygon data.
cube_mapper = vtk.vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort()) 

#%% ACTOR
# Connect the mapper to an actor.
cube_actor = vtk.vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

#%% RENDERER
# Create a renderer and add the actor to it.
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(cube_actor)

#%% RENDER WINDOW
# Create a render window.
render_window = vtk.vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetWindowName("Simple VTK scene")
render_window.AddRenderer(renderer)

#%% INTERACTOR
# Create an interactor.
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

#%% SHOWTIME
# Initialize the interactor and start the rendering loop.
interactor.Initialize()
render_window.Render()
interactor.Start()