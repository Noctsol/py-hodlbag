"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210917

Summary:
    Script to use all historical snapshots. Will pull from scratch if need be. Will backfill anything that is missing.
"""


import psycopg2
import re

from decimal import Decimal



class Ezpostgres():
    """Wrapper around psycopg2 for postgres. This was made for a lazy person to
    quickly use postgres via Python.
    """

    def __init__(self, host, dbname, username, password, port=5432, auto_connect=True) -> None:
        """[summary]

        Args:
            host ([type]): [description]
            dbname ([type]): [description]
            username ([type]): Username to sign in to database
            password ([type]): Password to sign in to database
            port (int, optional): Port used to connect to postgres. Defaults to 5432.
            auto_connect (bool, optional): Will return a connection upon initialization. Defaults to True.
        """
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password
        self.port = port
        self.auto_connect = auto_connect
        self.psycopg2_conn = None

        if self.auto_connect is True:
            self.connect()

    @classmethod
    def from_connection_string(cls, connection_string, auto_connect=True):
        """
        Connects using a traditional connection string like
        postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName

        Yes, I did this. I have no idea why. There's probably some edge cases I didn't
        catch since I literally don't know all the limitations/possibities with each
        field.

        """

        # Set up regex to look for ino
        host_regex = r"(?<=@)[\w\d\-.]+(?=:)"
        db_regex = r"(?<=\/)[\w_]+$"
        user_regex = r"(?<=\/\/)[\w\d._]+(?=:)"
        pw_regex = r"""(?<=:)[\w\s\d!"#$%&'()*+,-.;<=>?@\]\[^_`{|}~]+(?=@)"""
        port_regex = r"(?<=:)[\d]+(?=\/)"

        # Execute regex
        info = []
        for i in [host_regex, db_regex, user_regex, pw_regex, port_regex]:
            conn_i = re.search(i, connection_string)
            info.append(conn_i.group(0))

        return cls(info[0], info[1], info[2], info[3], port=info[4] ,auto_connect=auto_connect)

    def connect(self):
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.username,
            password=self.password
        )

        self.psycopg2_conn = conn

    def select(self, query, formatting="dict"):

        # Sanity check for optional param
        if formatting is not None and formatting != "dict" and formatting != "list":
            raise ValueError("'formatting' argment must be None, 'dict', or 'list'")

        # Setting up cursor
        with self.psycopg2_conn as connection:
            with connection.cursor() as cursor:

                # Executing query
                cursor.execute(query)

                # Grabbing headers/results
                headers = cursor.description
                results = cursor.fetchall()

                if formatting == "dict":
                    return self._to_listdict(headers, results)
                elif formatting == "list":
                    return self._to_listlist(headers, results)

                return (headers, results)

    def execute(self, query):
        with self.psycopg2_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                response = cursor.fetchall()
                return response


    def _standardize_value(self, value):
        """Converts

        Args:
            iterablo (iterable): Any iterable

        Returns:
            list: Returns a list
        """
        if type(value) is Decimal:
                return  float(value)

        return value


    def _to_listlist(self, headers, results):

        # Getting Headers
        headers = [i.name for i in headers]

        # Return container
        table = [headers]

        # Clean Data and append to retun container
        for row in results:
            temp_row = []
            for i in row:
                temp_row.append(self._standardize_value(i))
            table.append(temp_row)

        return table


    def _to_listdict(self, headers, results):

        # Getting Headers
        headers = [i.name for i in headers]

        # Return list of dictionaries mapping headers to values
        return [dict(zip(headers, i)) for i in results]
