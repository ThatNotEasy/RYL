from lib.sqlserver import SQLSERVER
from lib.mysql import MYSQL
import os
import json
import base64
from datetime import datetime
from colorama import init, Fore
init(autoreset=True)

EXCLUDED_DATABASES = ['master', 'tempdb', 'model', 'msdb']

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

data_type_mapping = {
    'int': 'INT',
    'nvarchar': 'VARCHAR',
    'datetime': 'DATETIME',
    'binary': 'BINARY',
    'varbinary': 'VARBINARY',
    'text': 'TEXT',
    'blob': 'BLOB',
    'version_number': 'INT',  # Use a different column name here
    # Add more datatype mappings as needed
}

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    mysql_server = MYSQL()

    sql_server = SQLSERVER()
    databases = fetch_databases(sql_server)
    sql_server.close()

    print(f"{Fore.RED}Please wait until it is finished, this might take a while for large databases.{Fore.RESET}")

    results = {}

    for database in databases:
        database_name = database['name']
        if database_name not in EXCLUDED_DATABASES:
            process_database(mysql_server, database_name, results)

    save_results_to_json(results)

    mysql_server.close()

def fetch_databases(sql_server):
    select = "SELECT name FROM sys.databases;"
    databases = sql_server.query(sql=select)
    return databases

def process_database(mysql_server, database_name, results):
    create_database(mysql_server, database_name)
    sql_server = SQLSERVER(dbname=database_name)
    table_info = get_table_info(sql_server)
    table_data = get_table_data(sql_server)
    sql_server.close()

    if table_data:
        results[database_name] = {
            "table_info": table_info,
            "table_data": table_data
        }

def create_database(mysql_server, database_name):
    create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
    mysql_server.execute(sql=create_db_query)
    mysql_server.commit()

def get_table_info(database_connection):
    query = "SELECT name FROM sys.tables;"
    tables = database_connection.query(query)
    table_info = {}

    for table in tables:
        table_name = table['name']
        if table_name != 'sysdiagrams':
            columns = get_table_columns(database_connection, table_name)
            table_info[table_name] = columns
    return table_info

def get_table_columns(database_connection, table_name):
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
    columns = database_connection.query(query)
    column_info = {}

    for column in columns:
        column_name = column['COLUMN_NAME']
        column_info[column_name] = None

    return column_info

def get_table_data(database_connection):
    query = "SELECT name FROM sys.tables;"
    tables = database_connection.query(query)
    table_data = {}

    for table in tables:
        table_name = table['name']
        if table_name != 'sysdiagrams':
            columns = get_table_columns(database_connection, table_name)
            table_data[table_name] = []

            select_query = f"SELECT * FROM {table_name};"
            data_rows = database_connection.query(select_query)

            for row in data_rows:
                row_data = {}
                for column, value in row.items():
                    if isinstance(value, bytes):
                        row_data[column] = base64.b64encode(value).decode('utf-8')
                    else:
                        row_data[column] = value
                table_data[table_name].append(row_data)
    return table_data

def generate_create_table_query(table_name, columns):
    column_definitions = [f"`{column_name}` {data_type}" for column_name, data_type in columns.items()]
    columns_definition = ", ".join(column_definitions)
    return f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_definition});"

def save_results_to_json(results):
    json_output = json.dumps(results, indent=4, cls=CustomJSONEncoder, ensure_ascii=False)
    with open("database.json", "w", encoding='utf-8') as json_file:
        json_file.write(json_output)
    print(Fore.RED + "JSON output:")
    print(json_output)
    print(Fore.GREEN + "Saved into database.json")

    mysql_server = MYSQL()

    for database_name, data in results.items():
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        mysql_server.execute(sql=create_db_query)
        mysql_server.commit()

        use_db_query = f"USE {database_name};"
        mysql_server.execute(sql=use_db_query)
        mysql_server.commit()

        for table_name, table_info in data["table_info"].items():
            create_table_query = generate_create_table_query(table_name, table_info)
            if create_table_query:
                mysql_server.execute(create_table_query)
                mysql_server.commit()

<<<<<<< HEAD:Database/insert.py
                for row in data["table_data"][table_name]:
                    insert_query = generate_insert_query(table_name, row)
                    values = tuple(row.values())
                    mysql_server.execute(sql=insert_query, args=values)
                    mysql_server.commit()

    mysql_server.close()

if __name__ == "__main__":
    clear()
    main()
=======
    finally:
        mysql_server.close()
>>>>>>> 3d37c91c22e19d8e8ac07ec96fd0ec232cc0fe5e:Database/tengah_cuba_insert_semua.py
