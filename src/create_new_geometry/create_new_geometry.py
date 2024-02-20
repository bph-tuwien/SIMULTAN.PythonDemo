from common.import_simultan  import *
from SIMULTAN.Data.Geometry import *
from SIMULTAN.Serializer.SimGeo import *


def create_new_geometry(project, projectData, name= "New Geometry"):
	resourceFile = project.AddEmptyGeometryResource(project.ProjectUnpackFolder,
		name,  f'{0} ({1})', project.AllProjectDataManagers.DispatcherTimerFactory)
		
	model_to_work_with = SimGeoIO.Load(resourceFile, projectData, None) # Load the geometry model


	layer =  Layer(model_to_work_with, "New Layer") # Adding a laer to the empty model
	model_to_work_with.Layers.Add(layer)


	position = SimPoint3D(0,0,0)
	vertex = Vertex(layer, "New Vertex", position)

	return model_to_work_with


