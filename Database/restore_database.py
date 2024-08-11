import pyodbc
import os
import coloredlogs, logging

# Configuration
server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
backup_file = 'path_to_your_backup_file.bak'

# Extract table name from backup file name
def get_table_name_from_backup(backup_file):
    base_name = os.path.basename(backup_file)
    table_name, _ = os.path.splitext(base_name)
    # Adjust the table name if needed (e.g., remove invalid characters)
    table_name = table_name.replace(' ', '_').replace('-', '_')
    return table_name

# Connection string
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

# SQL to restore the database
restore_sql = f"""
RESTORE DATABASE [{database}]
FROM DISK = N'{backup_file}'
WITH 
    FILE = 1, 
    NOUNLOAD, 
    REPLACE, 
    STATS = 10;
"""

# SQL to create a table based on the backup filename
def create_table_sql(table_name):
    return f"""
    CREATE TABLE [{database}].[dbo].[{table_name}] (
        id INT PRIMARY KEY IDENTITY,
        created_at DATETIME DEFAULT GETDATE()
    );
    """

# Configure logging
def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    coloredlogs.install(level='INFO', fmt=log_format)

def restore_database_and_create_table():
    table_name = get_table_name_from_backup(backup_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Connect to SQL Server
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            
            # Restore the database
            logger.info("Restoring the database...")
            cursor.execute(restore_sql)
            conn.commit()
            logger.info(f"Database '{database}' restored successfully from '{backup_file}'.")

            # Create a new table
            logger.info(f"Creating table '{table_name}'...")
            create_table_sql_command = create_table_sql(table_name)
            cursor.execute(create_table_sql_command)
            conn.commit()
            logger.info(f"Table '{table_name}' created successfully in the database '{database}'.")

    except pyodbc.Error as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    setup_logging()
    restore_database_and_create_table()
