from pythonnet import load
load("coreclr") # load net core

import clr
import os

# Get the value of a user environment variable
simultan_sdk_var = os.environ.get('SIMULTAN_SDK_DIR')
clr.AddReference(simultan_sdk_var+'\\SIMULTAN.dll')    # the dll

from SIMULTAN.Data import *
from SIMULTAN.Data.Geometry import *
from SIMULTAN.Data.Users import *
from SIMULTAN.Projects import *
from SIMULTAN.Utils import *
from SIMULTAN.Serializer.Projects import *
from System.IO import *
from System.Security import *
