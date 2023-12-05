from utils.import_simultan  import *
from SIMULTAN.Serializer.SimGeo import *

# The entry point function´s name has to be the same as the [name].py script´s name
# This function aims to access a geometry found in the project_data and access it´s proeprties and parts
def handle_geometry(project_data):


	# Find the geometry file in the resources of the project_data
    resource_to_open = next(filter(lambda item: item.Name  == 'geometry.simgeo', project_data.AssetManager.Resources))
    
    # Load the geometry model
	# Check if the geometry is open already // only necceserry f
    model = SimGeoIO.Load(resource_to_open, project_data, None)


    # Explore the geometry
    all_geometries = model.Geometry.Geometries # listing all geometries in the model regardless of it´s type
    
    layers = model.Geometry.Layers  #Geometries are assigned to layers for grouping
    
    vertices = model.Geometry.Vertices # can have components attached
    edges = model.Geometry.Edges   # Consists of exactly 2 vertices, can have components attached
    edge_loops = model.Geometry.EdgeLoops #Consists of edges , can have components attached
    faces = model.Geometry.Faces    # Consists of an edge_loop , can have components attached
    volumes = model.Geometry.Volumes # Consists of faces, can have components attached
    
    
    # Getting a volume fomr the mdel and inspecting it´s properties
		# Basic calculations
    first_volume = volumes[0]
    volume = VolumeAlgorithms.Volume(first_volume)
    volume_net = VolumeAlgorithms.VolumeBruttoNetto(first_volume).Item2
    volume_brutto = VolumeAlgorithms.VolumeBruttoNetto(first_volume).Item3
    clear_height =  VolumeAlgorithms.Height(first_volume).Item2
    max_height =  VolumeAlgorithms.Height(first_volume).Item3
    reference_height =  VolumeAlgorithms.Height(first_volume).Item1
    area_net =  VolumeAlgorithms.AreaBruttoNetto(first_volume).Item3
    area_brutto =  VolumeAlgorithms.AreaBruttoNetto(first_volume).Item2
    floor_plerimiter =  VolumeAlgorithms.FloorPerimeter(first_volume)





	# Building
    resource_to_open = next(filter(lambda item: item.Name  == 'siteplanner.spdxf', project_data.AssetManager.Resources))
    siteplanner_project = project_data.SitePlannerManager.GetSitePlannerProjectByFile(resource_to_open.File)
    building = siteplanner_project.Buildings[0]
    building_components = project_data.ComponentGeometryExchange.GetComponents(building)

    # Component.InstanceParameters 


    # Save the changes
    SimgeoIO.Save(model, resource_to_open, WriteMode.Plaintext)


    
    #project_data.GeometryModels.AddGeometryModel(geometry_model)
    project_data.Components[0].Name = 'my cool '
    print("done")
    return project_data.Components.Count
