# SIMULTAN.PythonDemo

## Requirements

- Python 3+
- pip package manager

## Install packages

```
cd [PATH_TO_FOLDER]
pip install -r src/requirements.txt
```

## Run Python

Basically to run the scripts from python, the main.py in each example subfolder must be started.
Depending on the example, main.py handles the opening of a .simultan project as well as user authentication.
By default, the .simultan proejcts attached to the demo have
username: admin,
password: admin, as can be seen
in the static variables in the main.py files.

```
cd [PATH_TO_FOLDER]/src/[EXAMPLE]/
python main.py run

```

## Examples

### project_loading

This example shows how to load a project and execute a method `f_int(...)` which replaces the name of the first component. It shows how to open a simultan project file and authenticate a user.

### project_new

This example shows how to create a new, empty project and how a first admin user is added to the project

### geometry_basics

This examples shows how to open a geometry file, register the GeometryModel in the project and print some geometric measurements of a volume
