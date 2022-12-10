# Starter Project

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