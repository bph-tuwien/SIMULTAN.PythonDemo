# Append search directory for common code
import sys, os
sys.path.append(os.path.dirname(__file__) + '\\..')

from common.import_simultan import *
from common.classes_authentication_service import *

#Importing functions to run 
from query_geometry_geometricrelations import *

#'test.simultan'
FILE_PATH = os.path.dirname(__file__) + '\\SiteplannerBuldingRelationExample.simultan'
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
print(query_geometry_geometricrelations(project, projectData))

# Here we close the project
# -------------------------

# //Disable folder watcher so they don't interfere with project closing
project.DisableProjectUnpackFolderWatcher();
# Save it
ZipProjectIO.Save(project, True);
# //Close the project, undoes the Open operation
ZipProjectIO.Close(project, True);
# //Unload the project, undoes the Load operation
ZipProjectIO.Unload(project);


# //Free all data from the project
projectData.Reset();

