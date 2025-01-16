# Author: Pari Malam

from lib.sqlserver import SQLSERVER
from lib.mysql import MYSQL
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

def get_table_columns(database_connection, table_name):
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
    columns = database_connection.query(query)
    column_names = [column['COLUMN_NAME'] for column in columns]
    return column_names

def get_all_table_info(database_connection):
    query = "SELECT name FROM sys.tables;"
    tables = database_connection.query(query)
    table_info = {}

    for table in tables:
        table_name = table['name']
        if table_name != 'sysdiagrams':
            columns = get_table_columns(database_connection, table_name)
            table_info[table_name] = columns

    return table_info

if __name__ == "__main__":
    sql_server = SQLSERVER()
    databases = sql_server.query("SELECT name FROM sys.databases;")
    sql_server.close()

    print(f"{Fore.RED}Please wait until it is finished, this might take a while for large databases.{Fore.RESET}")

    results = {}
    for database in databases:
        database_name = database['name']

        if database_name not in ['master', 'tempdb', 'model', 'msdb']:
            sql_server_db = SQLSERVER(dbname=database_name)
            table_info = get_all_table_info(sql_server_db)
            results[database_name] = table_info
            sql_server_db.close()

    json_output = json.dumps(results, indent=4, cls=CustomJSONEncoder)
    with open("database.json", "w") as json_file:
        json_file.write(json_output)

    print(Fore.RED + json_output)
    print(Fore.GREEN + "Saved into database.json")