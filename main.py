# Simple starter project to test installation and environment.
# Based on https://fastapi.tiangolo.com/tutorial/first-steps/
#
from fastapi import FastAPI

# Explicitly included uvicorn to enable starting within main program.
# Starting within main program is a simple way to enable running
# the code within the PyCharm debugger
#
import uvicorn

# Added support for "static" web pages and other content.
#
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# See the explanation for static files and mount on the FastAPI documentation.
# https://fastapi.tiangolo.com/tutorial/static-files/
#
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """
    Basic test for root path. I added the "hint" to the returned message to guide students to
    find the OpenAPI document pages.

    :return: Simple JSON message.
    """
    return {
        "message": "Hello World",
        "hint": "Go to /docs to see the OpenAPI documentation."
    }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Added the code below to enable running in PyCharm debugger.
# Modified the port from 8000 to 8001 because I often have multiple
# microservices running and need to spread over ports.
#
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
