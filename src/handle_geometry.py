from import_simultan  import *
from SIMULTAN.Serializer.SimGeo import *

# The entry point function´s name has to be the same as the [name].py script´s name
# This function aims to access a geometry found in the project_data and access it´s proeprties and parts
def handle_geometry(project, project_data):


	# Find the geometry file in the resources of the project_data
    resource_to_open = next(filter(lambda item: item.Name  == 'geometry.simgeo', project_data.AssetManager.Resources))
    # Registering the model to the data manager to have active connection between geometry and components
    project.AllProjectDataManagers.GeometryModels.AddGeometryModel(resource_to_open) 
    
    # Load the geometry model
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
    building_components = list(building_components) #Converting the C# IEnumerable<T> to a python list
    first_component = building_components[0]
    comp_instance = list(first_component.Instances)[0]
   
    # Component.InstanceParameters 
    instance_parameters = list(comp_instance.InstanceParameterValuesPersistent)
    for parameter in instance_parameters:
        print(f'{parameter.Key.NameTaxonomyEntry.TextOrKey}: {parameter.Value}') # Getting the name of a parameter and the value
        
	    
    
    # Make some modifications to an Instance Parameter of the "DoubleParameter"
    double_instance_param = next(filter(lambda item: item.Key.NameTaxonomyEntry.TextOrKey == 'DoubleParameter', instance_parameters))
    comp_instance.InstanceParameterValuesPersistent[double_instance_param.Key]=  8.9  #Change the value of the Instance parameter (does not effect the Parameter)
    print(f'{double_instance_param.Key.NameTaxonomyEntry.TextOrKey}: {comp_instance.InstanceParameterValuesPersistent[double_instance_param.Key]}')


    # Save the changes
    SimGeoIO.Save(model, resource_to_open, SimGeoIO.WriteMode.Plaintext)


    
    #project_data.GeometryModels.AddGeometryModel(geometry_model)
    project_data.Components[0].Name = 'my cool '
    print("done")
    return project_data.Components.Count
