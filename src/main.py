from import_simultan import *
from classes_authentication_service import *
import f_int

servicesProvider = ServicesProvider()
servicesProvider.AddService[IAuthenticationService](Python_AuthenticationService())
projectData = ExtendedProjectData()
projectFile = FileInfo('C:\\Soft_Dev_Prj\\HAM4D_VIE_Py_Simultan_Input\\test.simultan')
project = ZipProjectIO.Load(projectFile, projectData)
isAuthenticated = ZipProjectIO.AuthenticateUserAfterLoading(project, projectData, servicesProvider)

if isAuthenticated != True:
    print('Authentication failed')
    exit(-1)

ZipProjectIO.OpenAfterAuthentication(project, projectData)

print(f_int.f_int(projectData))


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

