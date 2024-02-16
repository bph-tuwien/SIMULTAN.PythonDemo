from common.import_simultan  import *
from SIMULTAN.Data.Geometry import *
from SIMULTAN.Serializer.SimGeo import *


def create_new_geometry(project, projectData, name= "New Geometry"):
	resourceFile = project.AddEmptyGeometryResource(project.ProjectUnpackFolder,
		name,  f'{0} ({1})', project.AllProjectDataManagers.DispatcherTimerFactory)
		# Load the geometry model
	model_to_work_with = SimGeoIO.Load(resourceFile, projectData, None)
	return model_to_work_with


