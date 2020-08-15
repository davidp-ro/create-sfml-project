from cx_Freeze import setup, Executable

executables = [
    Executable('create-sfml-project.py')
]

setup(name='create-sfml-project',
     version='1.0',
     description ='Create a SFML Project',
     executables=executables
)

