:install flask:

create a virtual environment

:on windows:
    -if on VScode open terminal CMD
        
        py -3 -m install venv venv

        -to activate venv-
        
        venv\Scripts\activate.bat
        (venv\Scripts\activate)

    you will se on the left of the path of the project
    (venv) it means that it is activated

    to install flask : 

    pip install flask

:to setup the project:

activate the venv if not activated
   
   venv\Scripts\activate


you should run this command only once
launch the followed command
    set FLASK_APP=farm.farm
    pip install --editable farm
then you will se a new folder farm.egg-info appearing 


:to launch the project :

activate the venv if not activated
   
   venv\Scripts\activate

follow it with

    set FLASK_APP=farm
    set FLASK_ENV=development
    run flask

