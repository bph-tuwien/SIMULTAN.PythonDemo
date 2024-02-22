from common.import_simultan  import *
from SIMULTAN.Data.Geometry import *
from SIMULTAN.Serializer.SimGeo import *
from SIMULTAN.Data.Assets import *
import numpy as np
import matplotlib.pyplot as plt

import SIMULTAN.Data.SimMath as sm
from System.Collections.Generic import List


import matplotlib.pyplot as plt

def plot_polygon(vertices, closed=True):
    """
    Plot a polygon defined by its vertices.

    Parameters:
    - vertices: List of (x, y) coordinates representing the vertices of the polygon.
    - closed: Whether the polygon should be closed (connect the last vertex to the first). Default is True.
    """
    x, y = zip(*vertices)
    if closed:
        x = list(x) + [x[0]]
        y = list(y) + [y[0]]

    plt.plot(x, y, marker='o')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Polygon Plot')
    plt.grid(True)
    plt.axis('equal')
    plt.show()



def rotate_by_degrees(np_vector, degrees):
    # Convert degrees to radians
    radians = np.radians(degrees)

    # Define the 2D rotation matrix
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)],
                                [np.sin(radians), np.cos(radians)]])

    # Apply the rotation matrix to the vector
    ccw_rotated_vector = np.dot(rotation_matrix, np_vector)

    return ccw_rotated_vector

def gimme_normal(model, pface):
    # this will return the outward normal vector in wgs coordinates

    polyline = List[sm.SimPoint3D]()

    # for edge in volumes[0].Faces[0].Face.Boundary.Edges:
    for edge in pface.Face.Boundary.Edges:
        v1 = edge.StartVertex
        # v2 = edge.EndVertex
        # polyline.append([v1.Position.X, v1.Position.Y, v1.Position.Z])
        polyline.Add(v1.Position)
    print('polyline.Count: ', polyline.Count)

    removed = False
    if polyline[0] == polyline[polyline.Count - 1]:
        polyline.RemoveAt(polyline.Count - 1)
        removed = True
    print('polyline.Count: ', polyline.Count)

    # GeoReferenceAlgorithms.GeoReferenceMesh(polyline, )
    georef_list = List[GeoRefPoint]()
    for gr in model.Geometry.GeoReferences:
        georef_list.Add(GeoRefPoint(gr.Vertex.Position, gr.ReferencePoint))

    polyline_wgs = GeoReferenceAlgorithms.GeoReferenceMesh(polyline, georef_list)
    p0_longitude = polyline_wgs.Item2[0].X
    p0_longitude = polyline_wgs.Item2[0].Y

    normal = EdgeLoopAlgorithms.NormalCCW(polyline_wgs.Item2)

    # if edge loop is used clockwise normal actually points away from us so we turn it around
    # if face.Face.Orientation == GeometricOrientation.Backward:
    if pface.Face.Orientation == GeometricOrientation.Backward:
        normal *= -1

    # if volume is on the backside pointing away was actually correct and we shouldnt have turn it around
    # if face.Orientation == GeometricOrientation.Backward:
    if pface.Orientation == GeometricOrientation.Backward:
        normal *= -1

    # bernhard says another *-1 is necessary
    normal *= -1

    return normal


def building_properties(project_data, building, property_name=None):
    # building = siteplanner_project.Buildings[0]
    building_components = project_data.ComponentGeometryExchange.GetComponents(building)
    building_components = list(building_components)  # Converting the C# IEnumerable<T> to a python list
    first_component = building_components[0]
    comp_instance = list(first_component.Instances)[0]
    # Component.InstanceParameters
    instance_parameters = list(comp_instance.InstanceParameterValuesPersistent)
    # instance_parameters[0] has a .Key.NameTaxonomyEntry.TextOrKey and a .Value

    if property_name is None:
        for parameter in instance_parameters:
            print(f'{parameter.Key.NameTaxonomyEntry.TextOrKey}: {parameter.Value}')  # Getting the name of a parameter and the value
        return

    for parameter in instance_parameters:
        if parameter.Key.NameTaxonomyEntry.TextOrKey == property_name:
            return parameter.Value


def get_building_by_id(project_data, siteplanner_project, geb_id):
    for building in siteplanner_project.Buildings:
        if building_properties(project_data, building, property_name='geb_id') == geb_id:
            return building
    return 'building not found'


def my_script(project_data, siteplanner_project):
    # we get the building 4373, because it has 2 adjacients. we care about the south east adjacency towards 4371
    building4373 = get_building_by_id(project_data, siteplanner_project, 4373)
    building = building4373

    # building_gebid = get_building_component_parameter_value_by_name(building, project_data, parameter_name="geb_id")
    # Load the geometry model
    building_geometry = SimGeoIO.Load(building.GeometryModelRes.ResourceFile, project_data, None)
    # project.AllProjectDataManagers.GeometryModels.AddGeometryModel(building_geometry)
    building_volume = building_geometry.Geometry.Volumes[0]
    adjacencies = []
    myfaces = building_volume.Faces

    # get the pface that has the building 4371 on the other side
    pface_to_4371 = None
    for pface in building_volume.Faces:
        adjacent_gebids = get_adjacent_building_gebid(pface, project_data, siteplanner_project)
        if 4371 in adjacent_gebids:
            pface_to_4371 = pface

    # get normal vector of that face
    mynormal = gimme_normal(building_geometry, pface_to_4371)
    mynormal_np = np.array([mynormal.X, mynormal.Y])
    print(f'the outward normal has the coordinates \nX: {mynormal.X} \nY: {mynormal.Y}')

    x=0

    # check plausibility: copied the polyline of the building 4373 from the geojason file...
    polyline_4373 = [[16.770242159243402, 48.03267471753271],
                     [16.77032460939326, 48.03265356788971],
                     [16.770282760198892, 48.03258017384838],
                     [16.77020031014858, 48.03260132346129],
                     [16.770242159243402, 48.03267471753271]]

    polyline_4373_warped = [[vtx[0] * np.sin(np.pi/2 - vtx[1]*np.pi/180.), vtx[1]] for vtx in polyline_4373]
    plot_polygon(polyline_4373_warped)

    # get the directions of the edges and normalize them
    diff_vecs_4373 = []
    for i in range(len(polyline_4373) - 1):
        diff_vecs_4373.append(np.array([polyline_4373[i+1][0] - polyline_4373[i][0], polyline_4373[i+1][1] - polyline_4373[i][1]]))
    diff_vecs_4373_normalized = [dv / np.linalg.norm(dv) for dv in diff_vecs_4373]
    print('normalized directions of the edges')
    for dv in diff_vecs_4373_normalized:
        print(dv)

    x=0

    pass


def query_geometry_geometricrelations(project, project_data, name= "New Geometry"):

    folder = next(filter(lambda item: isinstance(item, ResourceDirectoryEntry), project_data.AssetManager.Resources))
    siteplanner_file = next(filter(lambda item: item.Name.endswith(".spdxf"), folder.Children))
    siteplanner_project = project_data.SitePlannerManager.GetSitePlannerProjectByFile(siteplanner_file.File)

    my_script(project_data, siteplanner_project)

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
            
        

        #project.AllProjectDataManager.GeometryModels.RemoveGeometryModel(building_geometry)
 





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
  



def get_adjacent_building_gebid(pface, project_data, siteplanner_project):
    adjacent_buildings = get_adjacent_buildings(pface, project_data, siteplanner_project)
    geb_ids = []
    for adjacent_building in adjacent_buildings:
        geb_id = get_building_component_parameter_value_by_name(adjacent_building, project_data, parameter_name="geb_id")
        if geb_id != None:    
           geb_ids.append(geb_id)
    return geb_ids
        



def get_adjacent_buildings(pface, project_data, siteplanner_project):
    adjacent_buildings = []
    face_relations = filter(
        lambda item: item.Source.FileId == pface.Face.ModelGeometry.Model.File.Key and 
        item.Source.BaseGeometryId == pface.Face.Id,  project_data.GeometryRelations)

    for relation in face_relations:
        target_building = next(filter(lambda item: item.GeometryModelRes.ResourceFile.Key == relation.Target.FileId, siteplanner_project.Buildings))
        adjacent_buildings.append(target_building)
    return adjacent_buildings
    