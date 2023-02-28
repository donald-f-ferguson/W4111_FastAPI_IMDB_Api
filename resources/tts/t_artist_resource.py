from resources.mysql_data_service import MySQLDataService, MySQLDataServiceConfig
from resources.imdb_resources.artist_resource import ArtistResource
import json
from service_factory import ServiceFactory

service_factory = ServiceFactory()
artist_resource = service_factory.get_resource("ArtistResource")


def t1():

    a_resource = artist_resource
    result = a_resource.get_by_key("nm0727778")
    print("t1: result = \n", json.dumps(result.dict(), indent=2))


def t2():

    a_resource = artist_resource
    result = a_resource.get(primaryName='Sophie Turner')
    print("t1: result = \n", json.dumps(result.dict(), indent=2))


if __name__ == "__main__":
    # t1()
    t2()
