# W4111 - Intro. to Databases Starter Project

This is a simple FastAPI application project that has minor changes to the [tutorial
starter project.](https://fastapi.tiangolo.com/tutorial/first-steps/).

The comments in ```main.py``` explain the minor changes.

The project was created using the project wizard in [PyCharm](https://www.jetbrains.com/pycharm/)
The wizard installs Python packages. I added a ```requirements.txt``` to allow
```pip install -r requirements.txt```

The application listens on port 8001. The path ```localhost:8001/docs``` will open the
OpenAPI documenting the paths.

I added support for serving static files, e.g. web pages. ```localhost:8001/static/index.html```
is the only file. See the [explanation in the FastAPI](https://fastapi.tiangolo.com/tutorial/static-files/)
docs for serving static files.

The structure of the project is:
- ```main.py``` the FastAPI main program the defines the routes.
- ```requirements.txt``` defines the required python packages for pip install.
- ```/static``` shows how to return "static files," i.e. HTML files.
  - ```/static/index.html``` a simple HTML file.
- ```tts``` some unit tests. I do not use something like "tests" because PyCharm thinks I want
to use some testing automation package. I would use automation in a larger project.
  - ```t_mysql_data_service``` unit tests MySQL interaction.
  - ```t_artist_resource``` unit tests the IMDB Artist resource for name_basics.
- ```/resources``` contains the implementation of the resources.
  - ```base_data_service``` is an abstract base class for access to databases.
  - ```mysql_data_service``` is an implementation of ```base_data_service``` foe MySQL.
  - ```base_application_resource``` is an abstract base class for REST resources.
  - ```/imdb_resources``` is implementation of IMDB specific resources.
    - ```/artist_resource``` implements the resource for name_basics.