import json
from resources.json_file_data_service import JSONDataServiceConfig, JSONFileDataService

db_directory = "/Users/donaldferguson/Dropbox/00NewProjects/recitations/W4111_FastAPI_IMDB_Api/data"
collection_file = "mock_people_active.json"


def get_svc() -> JSONFileDataService:
    config = JSONDataServiceConfig(None)
    svc = JSONFileDataService(config)
    return svc


def t_matches_template():
    """
    Test the matches_template methods.
    """

    o1 = {
        "last_name": "Ferguson",
        "first_name": "Donald",
        "email": "dff9@columbia.edu",
        "role": "professor",
        "friendly": False,
    }

    t1 = {
        "last_name": "Ferguson",
        "friendly": False
    }

    svc = get_svc()

    result = svc.matches_template(o1, t1)

    print("First test = ", result)

    t1 = {
        "last_name": "Ferguson",
        "friendly": True
    }

    result = svc.matches_template(o1, t1)

    print("Second test = ", result)


def t_matches_retrieve():
    """
    Test the retrieve methods.
    """

    t1 = {
        "role": "Professor",
        "friendly": True,
        "school": "SEAS"
    }

    svc = get_svc()

    result = svc.retrieve(
        db_directory, collection_file, predicate=t1, project=["email", "role", "friendly", "school"]
    )

    print("The friendly professors in CC are: \n",
          json.dumps(result, indent=2)
          )


def t_create():
    """
    Test the create method.
    """
    new_obj = {"first_name": "Donald",
               "last_name": "Ferguson",
               "email": "sauron@mordor.gov",
               "friendly": False,
               "role": "Professor",
               "school": "SEAS"
    }
    new_obj_2 = {
        "first_name": "Angus",
        "last_name": "Ferguson",
        "email": "nazgul_king@mordor.gov",
        "friendly": False,
        "role": "Professor",
        "school": "SEAS"
}

    svc = get_svc()
    res = svc.create(
        db_directory,
        collection_file,
        new_obj
    )
    res1 = svc.create(
        db_directory,
        collection_file,
        new_obj_2
    )

    print("Create test returned", res + res1)


def t_delete():
    """
    Test the create method.
    """
    predicate = {
        "last_name": "Ferguson",
        "school": "SEAS"
    }
    svc = get_svc()

    res = svc.delete(
        db_directory,
        collection_file,
        predicate
    )

    print("Delete test returned", res)


def t_update():

    predicate = {
        "last_name": "Ferguson",
        "school": "SEAS"
    }
    new_value = {
        "friendly": True,
        "school": "CC"
    }

    svc = get_svc()

    res = svc.update(
        db_directory,
        collection_file,
        predicate,
        new_value
    )

    print("Update test returned", res)


if __name__ == "__main__":
    # t_matches_template()
    # t_matches_retrieve()
    t_create()
    t_update()







