from common.import_simultan  import *
from SIMULTAN.Serializer.SimGeo import *

# The entry point function´s name has to be the same as the [name].py script´s name
# This function aims to access a geometry found in the project_data and access it´s proeprties and parts
def access_geometry_components(project, project_data):


	# Find the geometry file in the resources of the project_data
    resource_to_open = next(filter(lambda item:  item.Name.endswith(".simgeo"), project_data.AssetManager.Resources))

    
    # Load the geometry model
    model = SimGeoIO.Load(resource_to_open, project_data, None)
    # Registering the model to the data manager to have active connection between geometry and components
    project.AllProjectDataManagers.GeometryModels.AddGeometryModel(model) 


    volumes = model.Geometry.Volumes # Consists of faces, can have components attached

    # Getting a volume fomr the mdel and inspecting it´s properties
		# Basic calculations
    first_volume = volumes[0]
    volume_components = list(project_data.ComponentGeometryExchange.GetComponents(first_volume)) # this works with every geometry

    

   