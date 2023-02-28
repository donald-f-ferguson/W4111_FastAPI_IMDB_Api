import json
import os.path
import copy

from resources.base_data_service import BaseDataService, BaseDataServiceConfig


class JSONDataServiceConfig(BaseDataServiceConfig):

    def __init__(self, config):
        super().__init__(config)


class JSONFileDataService(BaseDataService):

    def __init__(self, config: JSONDataServiceConfig):
        super().__init__(config)

    @staticmethod
    def load(database, collection):
        """

        :param database: Directory containing the JSON file.
        :param collection: File name.
        :return: The contents of the file as an array of JSON objects.
        """

        full_fn = os.path.join(database, collection)

        #
        # Standard code pattern for loading a JSON file.
        #
        with open(full_fn, "r") as in_file:
            result = json.load(in_file)

        return result

    @staticmethod
    def save(database, collection, the_data):
        """

        :param database: Directory containing the JSON file.
        :param collection: File name.
        :param the_data: A list of dict/JSON objects to save. This overwrites the existing file.
        :return: The contents of the file as an array of JSON objects.
        """

        full_fn = os.path.join(database, collection)

        #
        # Standard code pattern for loading a JSON file.
        #
        with open(full_fn, "w") as out_file:
            json.dump(the_data, out_file, indent=2)


    @staticmethod
    def matches_template(json_object, predicate):
        """

        Determines if the JSON object/dictionary matches a template.

        :param json_object: A dictionary/JSON element.
        :param predicate: A dictionary/JSON element. The json_object matches if it has the same value
            for every key as the template.
        :return: True if there is a match. False otherwise. If the template is None or {}, then the result is True.
        """

        # I guess that I am an optimist.
        result = True

        # On test if there is a predicate.
        if predicate:

            # For each key, value pair in the dictionary.
            for k, v in predicate.items():

                # Using get() allows return None instead of trigger an exception if I used json_object[k]
                # and there was no entry for k.
                tmp_v = json_object.get(k, None)

                # There is no element to match or the values are not the same.
                if tmp_v is None or tmp_v != v:

                    # The element does not match the template. We can stop checking other values.
                    result = False
                    break
        else:
            # Everything matches an empty template. So TRue is OK
            pass

        return result

    @staticmethod
    def project(json_object, fields):
        """
        Get the k,v elements of a dictionary from a list of keys.

        :param json_object: A dictionary/JSON object.
        :param fields: A list of fields
        :return: A dictionary containing the fields. This explodes is a field is not in the dictionary. Returns all
            of the elements is the field list is None.
        """

        # Yes. I know I could use a dictionary comprehension but I do not want to confuse
        # new Python programmers.
        result = {}

        if fields is not None:
            for k in fields:
                result[k] = json_object[k]
        else:
            result = copy.deepcopy(result)

        return result

    def retrieve(self, database, collection, predicate, project):
        """
        Read a JSON file and return the matching elements.

        :param database: Directory containing the file.
        :param collection: Name of the file containing the data.
        :param predicate: See BaseDataService
        :param project: See BaseDataService
        :return: A list containing dictionaries of the projected properties for matching entities.
        """
        collection = self.load(database, collection)

        result = []

        for d in collection:
            if self.matches_template(d, predicate):
                tmp = self.project(d, project)
                result.append(tmp)

        return result

    def retrieve_by_key(self, database, collection, key_field_values):
        pass

    def create(self, database, collection, new_element):
        """
        Add a new element to the JSON file.

        :param database: Directory containing the file.
        :param collection: Name of the file containing the data.
        :param new_element: The JSON object to add.
        :return: 1 if success (the number of rows effected).
        """

        coll = self.load(database, collection)
        coll.append(new_element)
        self.save(database, collection, coll)

        return 1

    def delete(self, database, collection, predicate):
        """
        Delete matching elements from a JSON file.

        :param database: Directory containing the file.
        :param collection: Name of the file containing the data.
        :param predicate: See BaseDataService
        :return: The number of elements deleted.
        """
        coll = self.load(database, collection)

        new_coll = []
        count = 0

        for c in coll:
            if not self.matches_template(c, predicate):
                new_coll.append(c)
            else:
                count = count + 1

        self.save(database, collection, new_coll)

        return count

    def update(self, database, collection, predicate, new_values):
        """
        Delete matching elements from a JSON file.

        :param database: Directory containing the file.
        :param collection: Name of the file containing the data.
        :param predicate: See BaseDataService
        :param new_values: A dictionary with new values for fields matching the predicate.
        :return: The number of elements deleted.
        """

        coll = self.load(database, collection)

        count = 0

        for c in coll:
            if self.matches_template(c, predicate):
                count = count + 1
                for k, v in new_values.items():
                    c[k] = v

        self.save(database, collection, coll)

        return count


