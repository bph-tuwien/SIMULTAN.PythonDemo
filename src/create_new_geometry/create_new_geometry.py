from common.import_simultan  import *
from SIMULTAN.Data.Geometry import *

def create_new_geometry(project, projectData):
	print(project.ProjectUnpackFolder)
	resourceFile = project.AddEmptyGeometryResource(project.ProjectUnpackFolder,
      "New Geometry",  f'{0} ({1})', project.AllProjectDataManagers.DispatcherTimerFactory)

	
	print("ASD")
	

