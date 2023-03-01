#
# Implements a very simple, naive data access service for MySQL.
# https://tuscany.apache.org/das-overview.html
#

# Uses pymysql for interacting with MySQL
#
import pymysql

# We will use multiple databases over the semester.
# To simplify REST resource implementation and loosely couple application logic to data access.
# In many cases, the design allows modifying the database without affecting application logic.
#
from resources.base_data_service import BaseDataService


class MySQLDataServiceConfig:
    """
    Class with configuration information
    """

    def __init__(self, user="root", pw="dbuserdbuser", db=None, host="localhost", port=3306,
                 autocommit=True, cursorclass=pymysql.cursors.DictCursor):
        """
        TODO This signature and method is lazy and sloppy. The defaults should not be hardcoded
        in the method definition.

        See the pymysql documentation for the explanation of the connection parameters.


        :param user:
        :param pw:
        :param db:
        :param host:
        :param port:
        :param autocommit:
        :param cursorclass:
        """
        self.user = user
        self.pw = pw
        self.db = db
        self.host = host
        self.port = port
        self.autocommit = autocommit
        self.cursorclass = cursorclass


class MySQLDataService(BaseDataService):
    """
    implements a base class for defining implementations for create, retrieve, update and delete (CRUD) for databases
    and data sources supporting the application. This implementation is for MySQL.
    """

    def __init__(self, config: MySQLDataServiceConfig):
        """

        :param config: An object providing configuration information and dependencies. This is a very simple form
            of dependency injection (https://en.wikipedia.org/wiki/Dependency_injection).
        """

        # TODO I intentionally am not using protected or private properties because having public properties.
        # Using public properties makes simple demos and code walk through easier.
        #
        # If you are not familiar with the concepts, see
        # https://www.tutorialsteacher.com/python/public-private-protected-modifiers
        #
        super().__init__(config)

    def get_connection(self):
        """

        :return: Returns a new connection using the configuration information for the service.
        """

        conn = pymysql.connect(
            user=self.config.user,
            password=self.config.pw,
            db=self.config.db,
            host=self.config.host,
            port=self.config.port,
            autocommit=self.config.autocommit,
            cursorclass=self.config.cursorclass
        )
        return conn

    def run_q(self, sql, args=None, con=None, fetch=False):
        """
        A function that "simplifies" making pymysql SQL calls to the DB.
        :param sql: A SQL statement that may have parameters.
            https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/
        :param args: Arguments for the parameters in the query.
        :param con: A connection for sending commands to the DB.
        :param fetch: If True, return data using fetchall(). If false, return the result of execution.
            https://pymysql.readthedocs.io/en/latest/modules/cursors.html
        :return: Either the result of cursor.execute() for cursor.fetchall()
        """

        con_created = False
        result = None

        # Create a connection if the parameter was None.
        if con is None:
            con = self.get_connection()
            con_created = True

        try:
            cursor = con.cursor()

            # Mogrify inserts args into the query parameters to form the string that will be sent to DB.
            # Printing the string is lazy. We should use logging.
            # An example is: https://philstories.medium.com/fastapi-logging-f6237b84ea64
            full_sql = cursor.mogrify(sql, args)
            print("*** full_sql = ", full_sql, " ***")

            # Execute query with args. The result is normally the number of affected rows.
            #
            res = cursor.execute(sql, args)

            # Get the data if requested.
            if fetch:
                result = cursor.fetchall()
            else:
                result = res

        # This is a sloppy approach to exception handling. Catching all exceptions is lazy and too broad.
        # We catch the exception to ensure that we close the connection on an error.
        #
        except Exception as e:
            pass

        # Close the connection if we created it.
        if con_created:
            con.close()

        return result

    @staticmethod
    def predicate_to_where_clause_args(predicate):
        """

        :param predicate: A dictionary of properties and values.
        :return:
            - A SQL where clause of the form "where k1=%s and k2=%s ..." for keys in the predicate
            - A list of the form [v1, v2, ...] with the values
        """

        # The default is no where clause or args.
        where_clause = ""
        args = None

        if predicate:

            terms = []
            args = []

            # For each key value pair.
            for k, v in predicate.items():

                # Add a clause of the form k=%s to be included in where clause.
                terms.append(k + "=%s")

                # Add the value for k into the args for statement.
                args.append(v)

            # Form the where clause by joing the k=%s into a string separated by AND.
            where_clause = " where " + " and ".join(terms)

        return where_clause, args

    @staticmethod
    def build_select(database, collection, predicate, project):
        """

        Build a select statement.

        :param database: The MySQL database to query.
        :param collection: The table in the database.
        :param predicate: A dictionary of key value pairs.
            A dictionary of the form {k1: v1, k2: v2, k3: v3} result in a where clause of the form
                where k1=v1 and k2=v2 and k3=v3.
        :param project:A list of column names for the select statement.
            [c1, c2, c3] results in "select c1, c2, c3 from ..."
        :return: A parameterized select statement and the args for the statement.
        """
        wc, args = MySQLDataService.predicate_to_where_clause_args(predicate)

        if project:
            select_clause = ",".join(project)
        else:
            select_clause = "*"

        sql = "select " + select_clause + " from " + \
              database + "." + collection + wc

        return sql, args

    @staticmethod
    def build_delete(database, collection, predicate):
        """

        Build a select statement.

        :param database: The MySQL database to query.
        :param collection: The table in the database.
        :param predicate: A dictionary of key value pairs.
            A dictionary of the form {k1: v1, k2: v2, k3: v3} result in a where clause of the form
                where k1=v1 and k2=v2 and k3=v3.
        :return: A parameterized select statement and the args for the statement.
        """

    @staticmethod
    def build_update(database, collection, predicate, new_values):
        """

        Build a select statement.

        :param database: The MySQL database to query.
        :param collection: The table in the database.
        :param predicate: A dictionary of key value pairs.
            A dictionary of the form {k1: v1, k2: v2, k3: v3} result in a where clause of the form
                where k1=v1 and k2=v2 and k3=v3.
        :param The values to set in the rows.
        :return: A parameterized select statement and the args for the statement.
        """

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
        conn = self.get_connection()

        sql, args = self.build_select(database, collection, predicate, project)
        result = self.run_q(sql, args, None, True)
        return result

    def retrieve_by_key(self, database, collection, key_columns):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param key_columns: List of the values for the key columns.
        :return:The resource with the primary key matching the values.
        """
        raise NotImplemented()
    #
    # TODO Students implement the following operations.
    # Will add later when defining HW assignments.
    #

    def delete(self, database, collection, predicate):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :return: A list containing dictionaries of the projected properties for matching entities.
        """

    def update(self, database, collection, predicate, new_data):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :param new_data: The keys and values used to form the set statement in SQL.
        :return: A list containing dictionaries of the projected properties for matching entities.
        """

    def create(self, database, collection, new_data):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param new_data: The data to insert into the table.
        :return: A list containing dictionaries of the projected properties for matching entities.
        """



