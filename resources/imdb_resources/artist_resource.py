#
# Implement the resource logic and methods for IMDB name_basics data.
#

# Use pydantic to define models and transfer objects.
from typing import List, Union
from pydantic import BaseModel


# All resources implement a common base interface. This simplifies using
# resources in some scenarios.
#
from resources.base_application_resource import BaseResource, Link


class Artist(BaseModel):
    """
    The model/data transfer object for a single entry from name_basics.

    Prof. Ferguson modified the format from the downloaded TSV file to produce a better
    relational/object schema.
    """

    # Primary key.
    nconst: str

    # TODO All of the name stuff might be better handled using an embedded class.
    # This would handle a name of the form "Dr. Donald Francis Ferguson IV (Darth Don)
    # See https://pypi.org/project/nameparser/ for what the fields mean.
    #
    # title: Union[str, None] = None
    # first_name: Union[str, None] = None
    # middle_name: Union[str, None] = None
    # last_name: str = None
    # suffix: Union[str, None] = None
    #   nickname: Union[str, None] = None
    # full_name: str = None

    # birth_year: str = None
    # death_year: str = None

    primaryName: Union[str, None] = None
    birthYear: Union[str, None] = None
    deathYear: Union[str, None] = None

    class Config:

        # The sample response for OpenAPI docs.
        #
        schema_extra = {
            """
            "example": {
                "nconst": "nm0000001",
                "title": "Dr.",
                "first_name": "Boris",
                "middle_name": "Alexander",
                "last_name": "Badenov",
                "suffix": "III",
                "nick_name": "Bubba",
                "full_name": "Boris Badenov",
                "birth_year": "1900",
                "death_year": "2000"
            }
            """
            "example": {
                "nconst": "nm3586035",
                "primaryName": "Maise Williams",
                "birthYear": "1997",
                "deathYear": None
            }
        }


class ArtistRsp(BaseModel):
    """
    A class implementing a HATEOAS pattern for return GET /artists?query string
    """

    # A data object with the Artist information.
    data: Artist

    # Links associated with the response.
    links: List[Link]

    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "nconst": "nm3586035",
                    "primaryName": "Maise Williams",
                    "birthYear": "1997",
                    "deathYear": None
                },
                "links": [
                    {"rel": "known_for_titles", "href": "/api/artists/nm0000001/known_for_titles"},
                    {"rel": "primary_professions", "href": "/api/artists/nm0000001/primary_professions"},
                    {"rel": "self", "href": "/api/artists/nm0000001"}
                ]
            }
        }


class ArtistResource(BaseResource):
    """
    Implement the Artist Resource
    """

    def __init__(self, context):
        super().__init__(context)
        self.key_column = context["key_column"]
        self.database = context["database"]
        self.collection = context["collection"]

    # Implements getting a single artists based on primary key.
    # Corresponds to GET /api/artists/nm0000001
    #
    def get_by_key(self, key):
        """

        :param key: The value of the primary key/ID in the collection.
        :return: An ArtistRsp with the data and links.
            TODO Need to convert to a 404 somewhere.
        """

        result = None

        ds = self.context['data_service']

        predicate = {self.key_column: key}

        result = ds.retrieve(self.database, self.collection, predicate, None)

        # Get on a path like /api/artists/id returns a single resource.
        # The collection query returns a list of matching resources.
        # Need to convert to a single element.
        #
        if result:
            result = result[0]
            tmp = dict()
            tmp["data"] = result

            # This is pretty lazy and could be handled by config information.
            #
            tmp["links"] = [
                {"rel": "primaryProfessions", "href": "/api/artists/" + key + "/primaryProfession"},
                {"rel": "knownForTitles", "href": "/api/artists/" + key + "/knownForTitles"},
                {"rel": "self", "href": "/api/artists/" + key}
            ]

            # Create the response model from the dictionary.
            result = ArtistRsp(**tmp)

        return result

    def get(self, primaryName=None, birthYear=None, deathYear=None):

        result = None

        ds = self.context['data_service']

        predicate = dict()

        if primaryName:
            predicate['primaryName'] = primaryName
        if birthYear:
            if (birthYear < '1900') or (birthYear > '2023'):
                raise ValueError("Bad birthYear")

            predicate['birthYear'] = birthYear
        if deathYear:
            predicate['deathYear'] = deathYear

        result = ds.retrieve(self.database, self.collection, predicate, None)

        # Get on a path like /api/artists/id returns a single resource.
        # The collection query returns a list of matching resources.
        # Need to convert to a single element.
        #
        if result:
            # result = result[0]
            tmp = dict()
            tmp["data"] = result

            # This is pretty lazy and could be handled by config information.
            #
            tmp["links"] = [
                #{"rel": "primaryProfessions", "href": "/api/artists/" + key + "/primaryProfession"},
                #{"rel": "knownForTitles", "href": "/api/artists/" + key + "/knownForTitles"},
                #{"rel": "self", "href": "/api/artists/" + key}
            ]

            # Create the response model from the dictionary.
            result = ArtistRsp(**tmp)

        return result

