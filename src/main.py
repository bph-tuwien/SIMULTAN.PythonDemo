from import_simultan import *
from classes_authentication_service import *

#Importing functions to run 
from f_int import *
from handle_geometry import *

#'src\\projects\\test.simultan'
FILE_PATH = 'geometry.simultan'
USERNAME = 'admin'
PASSWORD = 'admin'


servicesProvider = ServicesProvider()
servicesProvider.AddService[IAuthenticationService](Python_AuthenticationService(USERNAME, PASSWORD))
projectData = ExtendedProjectData()
projectFile = FileInfo(FILE_PATH)
project = ZipProjectIO.Load(projectFile, projectData)
isAuthenticated = ZipProjectIO.AuthenticateUserAfterLoading(project, projectData, servicesProvider )

if isAuthenticated != True:
    print('Authentication failed')
    exit(-1)

ZipProjectIO.OpenAfterAuthentication(project, projectData)

#Call your function here
#print(f_int.f_int(projectData))
print(handle_geometry(projectData))

# Here we close the project
# -------------------------

# //Disable folder watcher so they don't interfere with project closing
project.DisableProjectUnpackFolderWatcher();
# //Close the project, undoes the Open operation
ZipProjectIO.Close(project, False, True);
# //Unload the project, undoes the Load operation
ZipProjectIO.Unload(project);
# //Free all data from the project
projectData.Reset();

