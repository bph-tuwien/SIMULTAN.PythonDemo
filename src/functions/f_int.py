from utils.import_simultan import *

def f_int(project_data):

    project_data.Components[0].Name = 'my cool '
    return project_data.Components.Count
