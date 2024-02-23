from common.import_simultan  import *
from SIMULTAN.Data.Geometry import *
from SIMULTAN.Serializer.SimGeo import *
from SIMULTAN.Data.Assets import *

#Lists the "geb_id"s of BuildingComponents which have a geometric relation to the Buildings geometry
def query_geometry_geometricrelations(project, project_data):
    
    siteplanner_file = next(filter(lambda item: item.Name.endswith(".spdxf"), project_data.AssetManager.Resources))
    siteplanner_project = project_data.SitePlannerManager.GetSitePlannerProjectByFile(siteplanner_file.File)

    buildings = siteplanner_project.Buildings
    relations = project_data.GeometryRelations

   
    # For each building we get the geb_id of the afajcent
    for building in buildings: 
        building_gebid = get_building_component_parameter_value_by_name(building, project_data, parameter_name="geb_id")
        # Load the geometry model
        building_geometry = SimGeoIO.Load(building.GeometryModelRes.ResourceFile, project_data, None)
        #project.AllProjectDataManagers.GeometryModels.AddGeometryModel(building_geometry) 
        building_volume = building_geometry.Geometry.Volumes[0]
        adjacencies = []
        for pface in building_volume.Faces:
            adjacent_gebids = get_adjacent_building_gebid(pface, project_data, siteplanner_project)
            if(len(adjacent_gebids) > 0):
                adjacencies = adjacencies + adjacent_gebids
        if len(adjacencies) > 0:
           print(f'building id: {building_gebid}, adajcent_buildings: {adjacencies}')


    # Exmample for getting buildings efficiently based on the relations
    for relation in relations: 
        source_building = next(filter(lambda item: item.GeometryModelRes.ResourceFile.Key == relation.Source.FileId, buildings))
        target_building = next(filter(lambda item: item.GeometryModelRes.ResourceFile.Key == relation.Target.FileId, buildings))
        
        



# Function to get the value of a parameter attached to the component of the building
def get_building_component_parameter_value_by_name(building, project_data, parameter_name):
     component = list(project_data.ComponentGeometryExchange.GetComponents(building))[0] 
     if component != None:   
        parameter =  next(filter(lambda item: item.NameTaxonomyEntry.TextOrKey == parameter_name,component.Parameters ))
        if parameter != None:
           return parameter.Value
     return None
  


# Returns the list of "geb_id" of the adjacent buildings. 
# NOTE: geb_id is a parameter in the component attached to the building
def get_adjacent_building_gebid(pface, project_data, siteplanner_project):
    adjacent_buildings = get_adjacent_buildings(pface, project_data, siteplanner_project)
    geb_ids = []
    for adjacent_building in adjacent_buildings:
        geb_id = get_building_component_parameter_value_by_name(adjacent_building, project_data, parameter_name="geb_id")
        if geb_id != None:    
           geb_ids.append(geb_id)
    return geb_ids
        


# Returns SitePlanner buildings which have a GeometricRelation to the pface
def get_adjacent_buildings(pface, project_data, siteplanner_project):
    adjacent_buildings = []
    face_relations = filter(
        lambda item: item.Source.FileId == pface.Face.ModelGeometry.Model.File.Key and 
        item.Source.BaseGeometryId == pface.Face.Id,  project_data.GeometryRelations)

    for relation in face_relations:
        target_building = next(filter(lambda item: item.GeometryModelRes.ResourceFile.Key == relation.Target.FileId, siteplanner_project.Buildings))
        adjacent_buildings.append(target_building)
    return adjacent_buildings
    