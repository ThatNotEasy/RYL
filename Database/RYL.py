from lib.mysql import MYSQL
from lib.sqlserver import SQLSERVER
from colorama import Fore, Style

FY = Fore.YELLOW
FG = Fore.GREEN
FR = Fore.RED
FW = Fore.WHITE
R = Style.RESET_ALL

data_type_mapping = {
    'int': 'INT',
    'nvarchar': 'VARCHAR',
    'datetime': 'DATETIME',
    'binary': 'BINARY',
    'varbinary': 'VARBINARY',
    'text': 'TEXT',
    'blob': 'BLOB',
    # Add more datatype mappings as needed
}

databases = ['ROWadmintool', 'ROWbillingDB', 'ROWgame', 'ROWpay', 'youxiuser']

def create_database(mysql_db, database_name):
    create_db_sql = f"CREATE DATABASE IF NOT EXISTS {database_name.lower()} CHARACTER SET utf8 COLLATE utf8_bin;"
    mysql_db.execute(create_db_sql)
    mysql_db.commit()
    print(f"{FY}[RYL] - {FW}DATABASE: {FR}{database_name} - {FG}[SUCCESS] - {FW}Created In MYSQL.{R}")

def create_table(mysql_db, database_name, table_name, columns):
    create_table_sql = f"CREATE TABLE IF NOT EXISTS `{database_name}`.`{table_name}` ("
    for column in columns:
        column_name = column['COLUMN_NAME']
        data_type = column['DATA_TYPE'].lower()
        max_length = column['CHARACTER_MAXIMUM_LENGTH']

        if max_length and max_length > 255:
            mapped_data_type = 'TEXT'
        else:
            mapped_data_type = data_type_mapping.get(data_type, 'TEXT')

        create_table_sql += f"`{column_name}` {mapped_data_type}"
        if max_length:
            create_table_sql += f"({max_length})"
        create_table_sql += ", "

    create_table_sql = create_table_sql.rstrip(", ") + ");"

    mysql_db.execute(create_table_sql)
    mysql_db.commit()
    print(f"{FY}[RYL] - {FW}TABLE: {FR}{table_name} - {FG}[SUCCESS] - {FW}Create in MYSQL.{R}")

def main():
    for database_name in databases:
        print(f"{FY}Working with database: {database_name}{R}")

        mysql_db = MYSQL()
        create_database(mysql_db, database_name)
        mysql_db.close()

        sqlserver_db = SQLSERVER()
        try:
            tables = sqlserver_db.query(f"SELECT TABLE_NAME FROM {database_name}.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
            print(f"{FY}[RYL] - {FW}Tables in {FR}{database_name}: {tables}{R}")

            for table in tables:
                table_name = table['TABLE_NAME']
                print(f"{FY}[RYL] - TABLE: {table_name}{R}")

                columns_query = f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM {database_name}.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
                columns = sqlserver_db.query(columns_query)

                mysql_db = MYSQL()
                create_table(mysql_db, database_name, table_name, columns)
                mysql_db.close()

        finally:
            sqlserver_db.close()

if __name__ == "__main__":
    main()
