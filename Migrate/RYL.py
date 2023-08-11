# Author: Pari Malam

from lib.mysql import MYSQL
from lib.sqlserver import SQLSERVER
from colorama import Fore, Style

if __name__ == "__main__":
    data_type_mapping = {
        'int': 'INT',
        'nvarchar': 'VARCHAR',
        'datetime': 'DATETIME',
        'binary': 'BINARY',
        'varbinary': 'VARBINARY',
        'text': 'TEXT',
        'blob': 'BLOB',
        # important: adjust ur datatype
        # handle datatype at line 53
    }

    databases = ['ROWadmintool', 'ROWbillingDB', 'ROWgame', 'ROWpay', 'youxiuser']

    for database_name in databases:
        print(f"{Fore.YELLOW}Working with database: {database_name}{Style.RESET_ALL}")

        mysql_db = MYSQL()

        create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8 COLLATE utf8_bin;"
        mysql_db.execute(create_db_sql)
        mysql_db.commit()
        print(f"{Fore.GREEN}Database '{database_name}' created in MySQL.{Style.RESET_ALL}")
        mysql_db.close()

        select_query = f'''SELECT TABLE_NAME FROM {database_name}.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';'''

        sqlserver_db = SQLSERVER()
        try:
            tables = sqlserver_db.query(select_query)
            print(f"{Fore.GREEN}Tables in {database_name}:{Style.RESET_ALL}", tables)

            for table in tables:
                table_name = table['TABLE_NAME']
                print(f"{Fore.CYAN}Table: {table_name}{Style.RESET_ALL}")

                columns_query = f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM {database_name}.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
                columns = sqlserver_db.query(columns_query)

                mysql_db = MYSQL()

                create_table_sql = f"CREATE TABLE IF NOT EXISTS `{database_name}`.`{table_name}` ("
                for column in columns:
                    column_name = column['COLUMN_NAME']
                    data_type = column['DATA_TYPE'].lower()
                    max_length = column['CHARACTER_MAXIMUM_LENGTH']
                    mapped_data_type = data_type_mapping.get(data_type, 'TEXT')
                    create_table_sql += f"`{column_name}` {mapped_data_type}"
                    if max_length:
                        create_table_sql += f"({max_length})"
                    create_table_sql += ", "
                create_table_sql = create_table_sql.rstrip(", ") + ");"

                mysql_db.execute(create_table_sql)
                mysql_db.commit()
                print(f"{Fore.GREEN}Table '{table_name}' created in MySQL.{Style.RESET_ALL}")
                mysql_db.close()

        finally:
            sqlserver_db.close()
