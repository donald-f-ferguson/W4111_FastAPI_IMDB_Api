#
# An abstract base class for all resources.
# The simplifies development in some cases because we can code to the base class.
#

# Enable Abstract Base Class
# https://www.educative.io/answers/what-is-the-abstract-base-class-in-python
#
from abc import ABC

import copy

# Use pydantic, especially for OpenAPI/models, type hints, ... ...
from typing import List, Union
from pydantic import BaseModel

# The Links section for a HATEOAS REST response.
#
class Link(BaseModel):
    rel: str
    href: str


#
# Do we need a base class for this?
#
class ResourceResponse(BaseModel):
    pass


class BaseResource(ABC):
    """
    The blueprint for REST resources.
    """

    def __init__(self, context):
        """

        :param data_service: An instance of BaseDataService to provide access to the data.
        """
        super().__init__()

        self.context = copy.deepcopy(context)

