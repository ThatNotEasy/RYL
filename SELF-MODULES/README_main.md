# Self-Modules Main CLI

This is the main command-line interface that integrates all the Self-Modules functionality.

## Features

- **File Processing**: Convert TXT files to CSV format (RYL2 itemscript and generic)
- **Database Operations**: Test connections, show tables, migrate data, create tables, restore databases
- **Modular Design**: Each module can be used independently or through the main CLI

## Usage

```bash
python main.py <command> [options]
```

## Available Commands

### File Processing Commands

#### `txt-to-csv`
Convert TXT files to CSV format using the txt_into_csv module.

```bash
python main.py txt-to-csv --input INPUT --output OUTPUT
```

#### `format-itemscript`
Format and convert RYL2 itemscript files to CSV.

```bash
python main.py format-itemscript --input-folder INPUT --output-folder OUTPUT
```

#### `convert-txt`
Convert generic TXT files to CSV (uses default INPUT/OUTPUT folders).

```bash
python main.py convert-txt --input-folder INPUT --output-folder OUTPUT
```

### Database Commands

#### `test-connection`
Test database connections.

```bash
python main.py test-connection
```

#### `show-tables`
Show all database tables and columns.

```bash
python main.py show-tables --database mydb
```

#### `migrate-data`
Migrate data from SQL Server to MySQL.

```bash
python main.py migrate-data
```

#### `create-tables`
Create database tables from SQL Server schema.

```bash
python main.py create-tables
```

#### `restore-db`
Restore database from backup file.

```bash
python main.py restore-db --backup-file backup.bak --server localhost --database master
```

## Installation

### Required Dependencies

For basic file processing (no database features):
- Python 3.6+
- No additional packages required

For database features, install the following:

```bash
pip install mysql-connector-python
pip install pyodbc
pip install colorama
```

### Configuration

1. Copy `config.ini.example` to `config.ini`
2. Update the database connection settings in `config.ini`:

```ini
[MYSQL]
HOSTNAME = localhost
USERNAME = root
PASSWORD = your_mysql_password
PORT = 3306
PLUGIN = mysql_native_password

[SQLSERVER]
DATABASE = master
HOSTNAME = localhost
USERNAME = sa
PASSWORD = your_sqlserver_password
PORT = 1433
VERSION = 11.0
SSL = no
```

## Module Architecture

The main.py integrates the following modules:

- `format_itemscript.py` - RYL2 itemscript file processing
- `txt_into_csv.py` - Generic TXT to CSV conversion
- `mysql.py` - MySQL database operations
- `sqlserver.py` - SQL Server database operations
- `restore_database.py` - Database backup and restore
- `auto_create_db_table_column.py` - Automatic table creation
- `show_all_db_table_column.py` - Database schema inspection
- `tengah_cuba_insert_semua.py` - Data migration tools
- `test_connection.py` - Connection testing utilities

## Error Handling

The CLI gracefully handles missing dependencies:
- Database commands will show clear error messages if dependencies are missing
- File processing commands work without any database dependencies
- Detailed logging is provided in `self_modules.log`

## Examples

### Basic File Processing

```bash
# Convert RYL2 itemscript files
python main.py format-itemscript --input-folder ./input --output-folder ./output

# Convert generic TXT files
python main.py txt-to-csv --input ./txt_files --output ./csv_output
```

### Database Operations (with dependencies installed)

```bash
# Test database connections
python main.py test-connection

# Show all tables in a database
python main.py show-tables --database mydatabase

# Migrate data between databases
python main.py migrate-data

# Create tables from SQL Server schema
python main.py create-tables
```

## Logging

All operations are logged to `self_modules.log` with detailed information about:
- Command execution
- File processing results
- Database operations
- Error messages and warnings

## Exit Codes

- `0`: Success
- `1`: Error (check logs for details)