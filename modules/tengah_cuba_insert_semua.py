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
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        elif isinstance(obj, datetime): 
            return obj.isoformat()
        return super().default(obj)

data_type_mapping = {
    'int': 'INT',
    'bigint': 'BIGINT',
    'smallint': 'SMALLINT',
    'tinyint': 'TINYINT',
    'float': 'FLOAT',
    'real': 'REAL',
    'decimal': 'DECIMAL',
    'numeric': 'NUMERIC',
    'money': 'DECIMAL',  # You might need to adjust this based on MySQL precision and scale
    'smallmoney': 'DECIMAL',  # You might need to adjust this based on MySQL precision and scale
    'char': 'CHAR',
    'varchar': 'VARCHAR',
    'nvarchar': 'VARCHAR',
    'text': 'TEXT',
    'ntext': 'TEXT',
    'date': 'DATE',
    'datetime': 'DATETIME',
    'datetime2': 'DATETIME',
    'datetimeoffset': 'DATETIME',
    'smalldatetime': 'DATETIME',
    'time': 'TIME',
    'timestamp': 'TIMESTAMP',
    'binary': 'BINARY',
    'varbinary': 'VARBINARY',
    'image': 'BLOB',
    # Add more data type mappings as needed
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
            print(f"{Fore.YELLOW}Processing database: {database_name}")
            process_database(mysql_server, database_name, results)

    save_results_to_json(results)

    mysql_server.close()

def fetch_databases(sql_server):
    select = "SELECT name FROM sys.databases;"
    databases = sql_server.query(sql=select)
    return databases

def process_database(mysql_server, database_name, results):
    print(f"{Fore.YELLOW}Processing tables in database: {database_name}")
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
        print(f"{Fore.GREEN}Processed database: {database_name}")

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
    query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
    columns = database_connection.query(query)
    column_info = {}

    for column in columns:
        column_name = column['COLUMN_NAME']
        data_type = column['DATA_TYPE']
        column_info[column_name] = data_type

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
    column_definitions = []
    for column_name, data_type in columns.items():
        mapped_data_type = data_type_mapping.get(data_type, 'TEXT')
        column_definitions.append(f"`{column_name}` {mapped_data_type}")
    columns_definition = ", ".join(column_definitions)
    return f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_definition});"

def generate_insert_query(table_name, row):
    columns = ', '.join([f'[{column}]' for column in row.keys()])
    placeholders = ', '.join(['?'] * len(row))
    query = f"INSERT INTO [{table_name}] ({columns}) VALUES ({placeholders});"
    return query

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

        use_db_query = f"USE `{database_name}`;"
        mysql_server.execute(sql=use_db_query)
        mysql_server.commit()

        for table_name, table_info in data["table_info"].items():
            create_table_query = generate_create_table_query(table_name, table_info)
            if create_table_query:
                mysql_server.execute(create_table_query)
                mysql_server.commit()

                for row in data["table_data"][table_name]:
                    insert_query = generate_insert_query(table_name, row)
                    values = tuple(row.values())
                    mysql_server.execute(sql=insert_query, args=values)
                    mysql_server.commit()
                    print(Fore.CYAN + f"Inserted row into table {table_name}: {row}")

    mysql_server.close()

if __name__ == "__main__":
    clear()
    mysql_server = MYSQL()
    print(Fore.MAGENTA + "Starting data migration process...")
    main()
    print(Fore.MAGENTA + "Data migration process completed.")
    mysql_server.close()
