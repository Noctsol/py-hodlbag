"""
    Testing psycopgs 2 functionality
"""
import sys

sys.path.append('.')

import psycopg2
from library import environment

ev = environment.Environment("./secrets.env")
ev.load()

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=ev.get("local_pg_host"),
            port=ev.get("local_pg_port"),
            # dbname=ev.get("local_pg_db"),
            dbname="postgres",
            user=ev.get("local_pg_user"),
            password=ev.get("local_pg_pass")
        )

        # create a cursor
        cur = conn.cursor()

	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        for i in range(1000):
            cur.execute("CONNECT cryptohodl SELECT * FROM test_types")
            results = cur.fetchall()
        print(results)

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


connect()