from pythonnet import load
load("coreclr") # load net core

import clr
import os

# Get the value of a user environment variable
simultan_sdk_var = os.environ.get('SIMULTAN_SDK_DIR')
clr.AddReference(simultan_sdk_var+'\\SIMULTAN.dll')    # the dll

#Load additional .NET assemblies
clr.AddReference("System.Security.Cryptography")

# Import SIMULTAN Namespaces
from SIMULTAN.Data import *
from SIMULTAN.Data.Geometry import *
from SIMULTAN.Data.Components import *
from SIMULTAN.Data.Users import *
from SIMULTAN.Projects import *
from SIMULTAN.Utils import *
from SIMULTAN.Serializer.Projects import *

# Import useful .NET namespaces
from System import *
from System.IO import *
from System.Security import *
from System.Security.Cryptography import *
from System.Text import *