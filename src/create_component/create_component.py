from common.import_simultan  import *
from SIMULTAN.Data.Geometry import Layer,Vertex, Edge, EdgeLoop, Face, FaceAlgorithms, Volume
from SIMULTAN.Serializer.SimGeo import SimGeoIO
from SIMULTAN.Data.SimMath import  SimPoint3D
from System.Collections.Generic import List
from SIMULTAN.Data.Components import SimInstanceType, SimComponent



def create_component(project, project_data, name= "New Component", instance_type = SimInstanceType.Entity3D):
	""" Creates a SimComponent but does not add it to the ProjectData
	Args:
		project (HierarchicalProject): the Project
		project_data (ProjectData): _description_
		name (str, optional): The name of the new SimComponent. Defaults to "New Component".
		instance_type (SimInstanceType, optional): The instance type of the SimComponent. It is important to assign the SimComponent to geometry
		Defaults to SimInstanceType.Entity3D. 
		Possible types: 
		SimInstanceType.Entity3D: 
		SimInstanceType.Entity3D - Volume
		SimInstanceType.AttributesFace  - Face
		SimInstanceType.AttributesPoint - Vertex

	Returns:
		SimComponent: SimComponent
	"""

	# Create a new Coponent 
	component = SimComponent(project.AllProjectDataManagers.UsersManager.CurrentUser.Role)
	component.InstanceType = instance_type
	component.Name = name

	
	return component


