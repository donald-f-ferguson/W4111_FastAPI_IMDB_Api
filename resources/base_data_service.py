# Import support for abstract base classes.
#
# See https://www.educative.io/answers/what-is-the-abstract-base-class-in-python if you are unfamiliar with the
# concepts of abstract base classes.
#
from abc import ABC, abstractmethod

#
# TODO Check that the doc strings are correct for automatic documentation generation, e.g. sphinx.
# https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html
#


class BaseDataServiceConfig(ABC):
    """
    Abstract base class for dependency injection into BaseDataServiceClass.

    Just a placeholder for now.
    """
    def __init__(self, config):
        self.config = config


class BaseDataService(ABC):
    """
    A base class for defining implementations for create, retrieve, update and delete (CRUD) for databases and
    data sources supporting the application.
    """
    def __init__(self, config):
        """

        :param config: An object providing configuration information and dependencies. This is a very simple form
            of dependency injection (https://en.wikipedia.org/wiki/Dependency_injection).
        """

        # DFF TODO I intentionally am not using protected or private properties because having public properties.
        # Using public properties makes simple demos and code walk through easier.
        #
        # If you are not familiar with the concepts, see
        # https://www.tutorialsteacher.com/python/public-private-protected-modifiers
        #
        self.config = config

    @abstractmethod
    def retrieve(self, database, collection, predicate, project):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :param project: A list of subsets of the entity's properties to return. That is, if the list is
            [k1, k2, k3], this is logically like SELECT k1, k2, k3 ...
        :return: A list containing dictionaries of the projected properties for matching entities.
        """
        pass

    @abstractmethod
    def retrieve_by_key(self, database, collection, key_field_values):
        """
        Return a collection element based on values of primary key columns.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param key_field_values: A list with the values of the primary key fields in the defined order. For example,
            if the collection's primary key fields are ["postal_code", "country_code"] then an example key fields
            might be ["10027", "US"]
        :return: The element with the key or None.
        """
        pass

    @abstractmethod
    def create(self, database, collection, new_element):
        """
        Inserts a new element into the collection.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param new_element: A dictionary/JSON object to insert into the collection. For SQL, this would get mapped to a
            INSERT INTO database.collection(k1, k2, k3) VALUES(v1, v2, v3) if the new element is
            {"k1": "v1, "k2": "v2", "k3": "v3"}.
        :return: The primary key for the inserted element.
        """
        pass

    @abstractmethod
    def delete(self, database, collection, predicate):
        """
        Deletes all elements from the collection matching the predicate.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :return: The number of entities effected.
        """
        pass

    @abstractmethod
    def update(self, database, collection, predicate, new_values):
        """
        Update fields in matching a predicate..

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :param new_values: A dictionary of new field values for the matching elements.
        :return: The number of entities effected.
        """
        pass

