#!/usr/bin/env python3
"""
Main entry point for Self-Modules
Integrates all database and file processing modules with command line interface
"""

import argparse
import sys
import os
import json
import logging
from datetime import datetime
from typing import Optional

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('self_modules.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import all the modules
try:
    from modules.ryl2_itemscript_converter import (
        is_valid_ryl2_txt,
        convert_to_csv,
        process_txt_files,
        auto_detect_convert_and_save
    )
    from modules.text_to_csv_converter import convert_txt_to_csv, main as txt_to_csv_main

    # Database modules (optional - require dependencies)
    try:
        from modules.mysql_connector import MYSQL
        MYSQL_AVAILABLE = True
    except ImportError:
        MYSQL_AVAILABLE = False
        logger.warning("MySQL connector not available - install mysql-connector-python")

    try:
        from modules.sqlserver_connector import SQLSERVER
        SQLSERVER_AVAILABLE = True
    except ImportError:
        SQLSERVER_AVAILABLE = False
        logger.warning("SQL Server connector not available - install pyodbc")

    try:
        from modules.database_restorer import restore_database_and_create_table, setup_logging
        RESTORE_AVAILABLE = True
    except ImportError:
        RESTORE_AVAILABLE = False
        logger.warning("Database restorer not available - install pyodbc")

    try:
        from modules.schema_table_creator import main as create_tables_main
        TABLES_AVAILABLE = True
    except ImportError:
        TABLES_AVAILABLE = False
        logger.warning("Schema table creator not available - missing dependencies")

    try:
        from modules.database_schema_inspector import get_all_table_info, CustomJSONEncoder
        SHOW_TABLES_AVAILABLE = True
    except ImportError:
        SHOW_TABLES_AVAILABLE = False
        logger.warning("Database schema inspector not available - missing dependencies")

    try:
        from modules.data_migration_tool import main as migrate_data_main
        MIGRATE_AVAILABLE = True
    except ImportError:
        MIGRATE_AVAILABLE = False
        logger.warning("Data migration tool not available - missing dependencies")

    try:
        from modules.connection_tester import test_connection
        TEST_CONNECTION_AVAILABLE = True
    except ImportError:
        TEST_CONNECTION_AVAILABLE = False
        logger.warning("Connection tester not available - missing dependencies")

except ImportError as e:
    print(f"Error importing core modules: {e}")
    print("Please ensure all required Python files are available")
    sys.exit(1)


class SelfModulesCLI:
    """Main CLI class for Self-Modules"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Self-Modules - Database and File Processing Tools",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py txt-to-csv --input INPUT --output OUTPUT
  python main.py format-itemscript --input-folder INPUT --output-folder OUTPUT
  python main.py test-connection
  python main.py show-tables --database mydb
  python main.py migrate-data
  python main.py create-tables
  python main.py restore-db --backup-file backup.bak
            """
        )
        self.setup_arguments()

    def setup_arguments(self):
        """Setup command line arguments"""
        subparsers = self.parser.add_subparsers(dest='command', help='Available commands')

        # TXT to CSV conversion (format_itemscript)
        txt_parser = subparsers.add_parser('txt-to-csv', help='Convert TXT files to CSV')
        txt_parser.add_argument('--input', '-i', required=True, help='Input folder containing TXT files')
        txt_parser.add_argument('--output', '-o', required=True, help='Output folder for CSV files')

        # Format itemscript conversion
        format_parser = subparsers.add_parser('format-itemscript', help='Format and convert RYL2 itemscript files')
        format_parser.add_argument('--input-folder', required=True, help='Input folder containing RYL2 txt files')
        format_parser.add_argument('--output-folder', required=True, help='Output folder for converted CSV files')

        # Test database connection
        test_parser = subparsers.add_parser('test-connection', help='Test database connections')

        # Show database tables and columns
        show_parser = subparsers.add_parser('show-tables', help='Show all database tables and columns')
        show_parser.add_argument('--database', '-d', help='Specific database name (optional)')

        # Migrate data from SQL Server to MySQL
        migrate_parser = subparsers.add_parser('migrate-data', help='Migrate data from SQL Server to MySQL')

        # Create database tables
        create_parser = subparsers.add_parser('create-tables', help='Create database tables from SQL Server schema')

        # Restore database
        restore_parser = subparsers.add_parser('restore-db', help='Restore database from backup file')
        restore_parser.add_argument('--backup-file', required=True, help='Path to backup file')
        restore_parser.add_argument('--server', default='localhost', help='SQL Server name')
        restore_parser.add_argument('--database', default='master', help='Database name to restore to')
        restore_parser.add_argument('--username', help='Username for database connection')
        restore_parser.add_argument('--password', help='Password for database connection')

        # Generic TXT to CSV (from txt_into_csv module)
        generic_txt_parser = subparsers.add_parser('convert-txt', help='Convert generic TXT files to CSV')
        generic_txt_parser.add_argument('--input-folder', default='INPUT', help='Input folder (default: INPUT)')
        generic_txt_parser.add_argument('--output-folder', default='OUTPUT', help='Output folder (default: OUTPUT)')

    def run(self):
        """Run the CLI application"""
        if len(sys.argv) == 1:
            self.parser.print_help()
            return

        args = self.parser.parse_args()

        try:
            if args.command == 'txt-to-csv':
                self.txt_to_csv(args.input, args.output)
            elif args.command == 'format-itemscript':
                self.format_itemscript(args.input_folder, args.output_folder)
            elif args.command == 'test-connection':
                if not TEST_CONNECTION_AVAILABLE:
                    print("Error: Test connection module not available. Install required dependencies.")
                    sys.exit(1)
                self.test_db_connection()
            elif args.command == 'show-tables':
                if not SHOW_TABLES_AVAILABLE:
                    print("Error: Show tables module not available. Install required dependencies.")
                    sys.exit(1)
                self.show_database_tables(args.database)
            elif args.command == 'migrate-data':
                if not MIGRATE_AVAILABLE:
                    print("Error: Data migration module not available. Install required dependencies.")
                    sys.exit(1)
                self.migrate_database_data()
            elif args.command == 'create-tables':
                if not TABLES_AVAILABLE:
                    print("Error: Table creation module not available. Install required dependencies.")
                    sys.exit(1)
                self.create_database_tables()
            elif args.command == 'restore-db':
                if not RESTORE_AVAILABLE:
                    print("Error: Database restore module not available. Install required dependencies.")
                    sys.exit(1)
                self.restore_database(args)
            elif args.command == 'convert-txt':
                self.convert_generic_txt(args.input_folder, args.output_folder)
            else:
                self.parser.print_help()

        except Exception as e:
            logger.error(f"Error executing command: {e}")
            sys.exit(1)

    def txt_to_csv(self, input_folder: str, output_folder: str):
        """Convert TXT files to CSV using txt_into_csv module"""
        logger.info(f"Converting TXT files from {input_folder} to CSV in {output_folder}")

        if not os.path.exists(input_folder):
            logger.error(f"Input folder {input_folder} does not exist")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"Created output folder: {output_folder}")

        txt_to_csv_main()
        logger.info("TXT to CSV conversion completed")

    def format_itemscript(self, input_folder: str, output_folder: str):
        """Format and convert RYL2 itemscript files"""
        logger.info(f"Formatting RYL2 itemscript files from {input_folder} to {output_folder}")

        if not os.path.exists(input_folder):
            logger.error(f"Input folder {input_folder} does not exist")
            return

        auto_detect_convert_and_save(input_folder, output_folder)
        logger.info("RYL2 itemscript formatting completed")

    def test_db_connection(self):
        """Test database connections"""
        logger.info("Testing database connections")
        try:
            test_connection()
            logger.info("Database connection test completed")
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise

    def show_database_tables(self, database: Optional[str] = None):
        """Show all database tables and columns"""
        logger.info("Retrieving database tables and columns information")

        try:
            sql_server = SQLSERVER()
            if database:
                sql_server_db = SQLSERVER(dbname=database)
                table_info = get_all_table_info(sql_server_db)
                results = {database: table_info}
                sql_server_db.close()
            else:
                databases = sql_server.query("SELECT name FROM sys.databases;")
                sql_server.close()

                results = {}
                for db in databases:
                    database_name = db['name']
                    if database_name not in ['master', 'tempdb', 'model', 'msdb']:
                        sql_server_db = SQLSERVER(dbname=database_name)
                        table_info = get_all_table_info(sql_server_db)
                        results[database_name] = table_info
                        sql_server_db.close()

            # Save to JSON file
            json_output = json.dumps(results, indent=4, cls=CustomJSONEncoder)
            with open("database.json", "w") as json_file:
                json_file.write(json_output)

            print("Database information saved to database.json")
            logger.info("Database tables information retrieved successfully")

        except Exception as e:
            logger.error(f"Failed to retrieve database information: {e}")
            raise

    def migrate_database_data(self):
        """Migrate data from SQL Server to MySQL"""
        logger.info("Starting data migration from SQL Server to MySQL")
        try:
            migrate_data_main()
            logger.info("Data migration completed successfully")
        except Exception as e:
            logger.error(f"Data migration failed: {e}")
            raise

    def create_database_tables(self):
        """Create database tables from SQL Server schema"""
        logger.info("Creating database tables from SQL Server schema")
        try:
            create_tables_main()
            logger.info("Database table creation completed")
        except Exception as e:
            logger.error(f"Database table creation failed: {e}")
            raise

    def restore_database(self, args):
        """Restore database from backup file"""
        logger.info(f"Restoring database from {args.backup_file}")

        # Update global variables in database_restorer module
        import modules.database_restorer as database_restorer
        database_restorer.server = args.server
        database_restorer.database = args.database
        database_restorer.username = args.username or 'your_username'
        database_restorer.password = args.password or 'your_password'
        database_restorer.backup_file = args.backup_file

        try:
            setup_logging()
            restore_database_and_create_table()
            logger.info("Database restoration completed successfully")
        except Exception as e:
            logger.error(f"Database restoration failed: {e}")
            raise

    def convert_generic_txt(self, input_folder: str, output_folder: str):
        """Convert generic TXT files to CSV"""
        logger.info(f"Converting generic TXT files from {input_folder} to {output_folder}")

        if not os.path.exists(input_folder):
            logger.error(f"Input folder {input_folder} does not exist")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"Created output folder: {output_folder}")

        txt_to_csv_main()
        logger.info("Generic TXT to CSV conversion completed")

def main():
    """Main entry point"""
    try:
        cli = SelfModulesCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()