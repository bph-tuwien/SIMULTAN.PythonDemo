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

Basically to run the scripts from python, the main.py must be started.
main.py handles the opening of a .simultan project as well as user authentication.
By default, the .simulta proejcts attached to the demo have
username: admin,
password: admin, as it can be seen
in the static variables in the main.py file.

```
cd [PATH_TO_FOLDER]/src
python main.py run

```

Depending on which function is called "f_int" or "handle_geometry" in the main.py script the python is executed on the defined project.
The project is also defiend as a static variable in the main.py file.
