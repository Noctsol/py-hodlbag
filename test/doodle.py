

import sys

sys.path.append('.')

from library.ezpostgres import Ezpostgres

import psycopg2
import quikenv
import re


ev = quikenv.ezload()


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    ev.get("postgres_conn_str")
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    # conn = psycopg2.connect(
    #     host=ev.get("local_pg_host"),
    #     port=ev.get("local_pg_port"),
    #     # dbname=ev.get("local_pg_db"),
    #     dbname="postgres",
    #     user=ev.get("local_pg_user"),
    #     password=ev.get("local_pg_pass")
    # )

    conn = psycopg2.connect(ev.get("postgres_conn_str"))



# pretend_string = "postgres://noctsol1:some password@ez.mode.db:5432/some_db"

# # Yes, I wrote the regex for all of this
# user_regex = r"(?<=\/\/)[\w\d._]+(?=:)"
# pw_regex = r"""(?<=:)[\w\s\d!"#$%&'()*+,-.;<=>?@\]\[^_`{|}~]+(?=@)"""
# host_regex = r"(?<=@)[\w\d\-.]+(?=:)"
# port_regex = r"(?<=:)[\d]+(?=\/)"
# db_regex = r"(?<=\/)[\w_]+$"

# [user_regex, pw_regex, host_regex, port_regex, db_regex]

# for i in [user_regex, pw_regex, host_regex, port_regex, db_regex]:
#     someword = re.search(i, pretend_string)
#     print(someword.group(0))

pg = Ezpostgres.from_connection_string(ev.get("postgres_conn_str"))

x = pg.select("SELECT * FROM test_types", formatting=None)


for i in x:
    print(i)


# formatting =  (None, "dict", "list")

# formatting = "nONE"

# if formatting is not None and formatting != "dict" and formatting != "list":
#     print("THROW ERROR")
# else:
#     print("PASS")