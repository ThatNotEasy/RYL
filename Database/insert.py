# Author: Pari Malam

from lib.sqlserver import SQLSERVER
from lib.mysql import MYSQL
import json
from datetime import datetime
from colorama import init, Fore
import mysql.connector

# Initialize colorama
init(autoreset=True)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

def get_table_info(database_connection, table_name):
    query = f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';'''
    columns = database_connection.query(query)
    column_names = [column['COLUMN_NAME'] for column in columns]
    return column_names

def get_all_table_names_and_columns(database_connection):
    query = '''SELECT name FROM sys.tables;'''
    tables = database_connection.query(query)
    table_info = {}

    for table in tables:
        table_name = table['name']
        if table_name not in ['sysdiagrams']:  # Skip certain system tables
            columns = get_table_info(database_connection, table_name)
            table_info[table_name] = columns

    return table_info

if __name__ == "__main__":
    sqlserver = SQLSERVER()
    databases = sqlserver.query('''SELECT name FROM sys.databases;''')
    sqlserver.close()
    print(f"\n{Fore.RED}Please wait until it is finished, it is possible that your database size is too large{Fore.RESET}")

    results = {}
    for database in databases:
        database_name = database['name']

        if database_name not in ['master', 'tempdb', 'model', 'msdb']:
            sqlserver_db = SQLSERVER(dbname=database_name)

            table_info = get_all_table_names_and_columns(sqlserver_db)

            results[database_name] = table_info

            sqlserver_db.close()

    json_output = json.dumps(results, indent=4, cls=CustomJSONEncoder)

    mysql_server = MYSQL()

    try:
        # Assuming you have a MySQL database and table named "json_data"
        db_name = "api"  # Replace with your actual database name
        mysql_server.execute(f"USE {db_name};")
        insert_query = "INSERT INTO json_data (data) VALUES (%s)"
        mysql_server.execute(insert_query, (json_output,))
        mysql_server.commit()

        print(Fore.GREEN + "JSON data inserted into MySQL database successfully!")

    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")

    finally:
        mysql_server.close()