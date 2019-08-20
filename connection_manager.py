import mysql.connector
import config

class ConnectSQL:

    def __init__(self, db_name):
        self._db_name = db_name

    def __enter__(self):
        try:
            self._connection = mysql.connector.connect(database=self._db_name, **config.config)
        except:
            raise Exception("Ooops! Something wrong with connection config")
        self._cursor = self._connection.cursor()
        return self

    def __exit__(self, *args):
        self._cursor.close()
        self._connection.close()
        if args[0] is not None:
            raise Exception("Close Connection Error")

    def fetchall(self):
        return self._cursor.fetchall()

    def exec(self, query, commit=False):
        try:
            self._cursor.execute(query)
            if commit:
                self._connection.commit()
        except Exception as err:
            self._connection.rollback()
            print(err)
            raise Exception("Query execution error")
