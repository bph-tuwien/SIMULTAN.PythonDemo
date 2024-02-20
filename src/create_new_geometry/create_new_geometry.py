from common.import_simultan  import *
from SIMULTAN.Data.Geometry import Layer,Vertex, Edge, EdgeLoop, Face, FaceAlgorithms, Volume
from SIMULTAN.Serializer.SimGeo import SimGeoIO
from SIMULTAN.Data.SimMath import  SimPoint3D
from  System.Collections.Generic import List
from SIMULTAN.Data.Components import SimInstanceType, SimComponent
from create_component.create_component import *

def create_new_geometry(project, projectData, name= "New Geometry"):

	print("START")
	resourceFile = project.AddEmptyGeometryResource(project.ProjectUnpackFolder,
		name,  "{0} ({1})", project.AllProjectDataManagers.DispatcherTimerFactory) 
	# NOTE: The "{0} ({1})" is for deifnind the collision format of the name of the newly created .simgeo file
	# {0} defines that the originally provided "name" will be used and then on the ({1}) place a coutner will provide the new name
	# If it would not be provided name collision could result in an error
		
	geometry_model = SimGeoIO.Load(resourceFile, projectData, None) # Load the geometry model
	projectData.GeometryModels.AddGeometryModel(geometry_model) #register it to the managed collection of the ProjectData (this is needed to use utility funcitons handling association with SimComponents)
	geometry = geometry_model.Geometry


	layer =  Layer(geometry, "New Layer") # Adding a laer to the empty model
	geometry.Layers.Add(layer)


    # Defining the Points for the base polygon 
	# NOTE: "x,z" plane is considered as the gorund plane, and "y" is the up direction
	point1 = SimPoint3D(0,0,0)
	point2 = SimPoint3D(10,0,0)
	point3 = SimPoint3D(10,0,10)
	point4 = SimPoint3D(0,0,10)


	# Creating Vertices
	vertex1 = Vertex(layer, "vertex1", point1)  # Passing the layer as an argument registers the vertex into the "geometry.Vertices" collection
	vertex2 = Vertex(layer, "vertex2", point2) 
	vertex3 = Vertex(layer, "vertex3", point3) 
	vertex4 = Vertex(layer, "vertex4", point4) 


	list12 = List[Vertex]() # Creating a c# System.Collections.Generic.List
	list12.Add(vertex1)
	list12.Add(vertex2)

	list23 = List[Vertex]()
	list23.Add(vertex2)
	list23.Add(vertex3)

	list34 = List[Vertex]()
	list34.Add(vertex3)
	list34.Add(vertex4)

	list41 = List[Vertex]()
	list41.Add(vertex4)
	list41.Add(vertex1)
	
	edge12 = Edge(layer, "edge12",  list12)
	edge23 = Edge(layer, "edge23",  list23)
	edge34 = Edge(layer, "edge34",  list34)
	edge41 = Edge(layer, "edge41",  list41)

	edgesList = List[Edge]()
	edgesList.Add(edge12)
	edgesList.Add(edge23)
	edgesList.Add(edge34)
	edgesList.Add(edge41)

	egeLoop = EdgeLoop(layer, "edgeloop", edgesList) 	#The edgeloop giving the borders of the polyline
	face = Face(layer, "Face", egeLoop) 				#Creating a face 


	#Extruding the Face to get a Volume:
	faces = List[Face]()
	faces.Add(face)
	extrusionResult = FaceAlgorithms.Extrude(faces, face, 15)
	extrusionResult.Item1  # geometry created during extrusion: Vertices, Faces Volume
	extrusionResult.Item2  # referenceFace ("bottom" face)
	extrusionResult.Item2  # extrudedReferenceFace (Top face)

	#Looking for the created volume
	volume = next(filter(lambda item: isinstance(item, Volume)  , extrusionResult.Item1 ))
	# NOTE: Save it, otherwise the geometry we created will not be present
	SimGeoIO.Save(geometry_model, resourceFile,  SimGeoIO.WriteMode.Plaintext)

	#Assigning a Component to the Volume

	# 1. Crete the component
	component = create_component(project, projectData, "Volume Component", SimInstanceType.Entity3D)
	projectData.Components.Add(component)
	# 2. Assing them together NOTE: Associateion creates an Instance of the Component
	projectData.ComponentGeometryExchange.Associate(component, volume)

	# Get the associated components of the Volume
	components_of_volume = projectData.ComponentGeometryExchange.GetComponents(volume)
	print(len(list(components_of_volume)))


	return geometry


