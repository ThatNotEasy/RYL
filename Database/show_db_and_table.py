# Author: Pari Malam

from lib.sqlserver import SQLSERVER
import json
from datetime import datetime
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

def get_all_table_names(database_connection):
    query = '''SELECT name FROM sys.tables;'''
    tables = database_connection.query(query)
    table_names = [table['name'] for table in tables]
    return table_names

if __name__ == "__main__":
    sqlserver = SQLSERVER()
    databases = sqlserver.query('''SELECT name FROM sys.databases;''')
    sqlserver.close()

    results = {}
    for database in databases:
        database_name = database['name']

        if database_name not in ['master', 'tempdb', 'model', 'msdb']:
            sqlserver_db = SQLSERVER(dbname=database_name)

            tables_sqlserver = get_all_table_names(sqlserver_db)

            results[database_name] = tables_sqlserver

            sqlserver_db.close()

    print(Fore.GREEN + json.dumps(results, indent=4, cls=CustomJSONEncoder))
