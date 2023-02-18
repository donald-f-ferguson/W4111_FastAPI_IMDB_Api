#
# A very simple, naive implementation of the service factory pattern.
# https://www.tutorialspoint.com/design_pattern/factory_pattern.htm
#

# Definitions of the services
#
from resources.imdb_resources.artist_resource import Artist, ArtistRsp, ArtistResource
from resources.mysql_data_service import MySQLDataService, MySQLDataServiceConfig


class ServiceFactory:
    """
    A simple implementation of the service factory pattern.
    (https://www.tutorialspoint.com/design_pattern/factory_pattern.htm)

    The class creates, configures and "wires" together resource implementations.
    """

    def __init__(self):

        # A class implementing a service for accessing relational data in MySQL.
        self.mysql_config = MySQLDataServiceConfig()
        self.data_service = MySQLDataService(self.mysql_config)

        # Configuration and dependencies for the ArtistResource.
        # This is sloppy and should be in a factory specific to the resource.
        #
        artist_context = dict()
        artist_context["data_service"] = self.data_service
        artist_context["key_column"] = "nconst"
        artist_context["database"] = "s22_imdb_clean"
        artist_context["collection"] = "name_basics"

        # Create the resource.
        # Use dependency injection in a simple form.
        # https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html
        #
        self.artist_resource = ArtistResource(artist_context)

    def get_resource(self, resource_name):
        """

        :param resource_name: The "name" for the resource implementation.
        :return: The resource implementation.
        """

        if resource_name == "ArtistResource":
            result = self.artist_resource
        else:
            result = None

        return result

