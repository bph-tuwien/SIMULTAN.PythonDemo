# Append search directory for common code
import sys, os
sys.path.append(os.path.dirname(__file__) + '\\..')

from common.import_simultan import *

# Project file and user
FILE_PATH = os.path.dirname(__file__) + '\\NewProject.simultan'
USERNAME = 'admin'
PASSWORD = 'admin'

# Generate data for the initial admin user
passwordArray = Encoding.UTF8.GetBytes(PASSWORD)
encryptionKey = RandomNumberGenerator.GetBytes(32)
encryptedEncryptionKey = SimUsersManager.EncryptEncryptionKey(encryptionKey, passwordArray)
passwordHash = SimUsersManager.HashPassword(passwordArray)
initialUser = SimUser(Guid.NewGuid(), USERNAME, passwordHash, encryptedEncryptionKey, SimUserRole.ADMINISTRATOR)

# Choose a folder in which files are temporarily placed during project creation
tempPath = Path.GetTempPath()

# Create ProjectData and project file
projectFile = FileInfo(FILE_PATH)
projectData = ExtendedProjectData()

# Set the encryption key for this project
projectData.UsersManager.EncryptionKey = encryptionKey

#Make sure that the project doesn't already exist
if projectFile.Exists:
    projectFile.Delete()

#Create Project
project = ZipProjectIO.NewProject(projectFile, tempPath, projectData, initialUser)

# Check if project has been created
projectFile.Refresh();
if projectFile.Exists:
    print("Project created successfully");
else:
    print("Failed to create project");