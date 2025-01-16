from configparser import ConfigParser
import pyodbc

config = ConfigParser()
config.read('config.ini')

DATABASE = config['SQLSERVER']["DATABASE"]
HOSTNAME = config['SQLSERVER']["HOSTNAME"]
USERNAME = config['SQLSERVER']["USERNAME"]
PASSWORD = config['SQLSERVER']["PASSWORD"]
PORT = config['SQLSERVER']["PORT"]
VERSION = config['SQLSERVER']['VERSION']
SSL = config['SQLSERVER']['SSL']

login_timeout = 30  # Increased timeout value

class SQLSERVER():
    
    def __init__(self,
                 dbname=DATABASE,
                 hostname=HOSTNAME,
                 username=USERNAME,
                 password=PASSWORD,
                 port=PORT,
                 version=VERSION,
                 is_ssl=SSL
                 ):
        self.hostname = hostname
        self.dbname = dbname
        self.username = username
        self.password = password
        self.port = port
        self.version = version
        self.is_ssl = is_ssl

        self.connstring = (
            f"DRIVER={{SQL Server Native Client {self.version}}};"
            f"SERVER={self.hostname};"
            f"DATABASE={self.dbname};UID={self.username};"
            f"PWD={self.password};Encrypt={'yes' if self.is_ssl.lower() == 'yes' else 'no'};"
            f"TrustServerCertificate=yes;"
        )
        try:
            self.conn = pyodbc.connect(
                self.connstring,
                timeout=login_timeout
            )
            self.cur = self.conn.cursor()
        except Exception as err:
            print(f'DATABASE on MAIN CODE - {err}', 'error')
            self.close()

    def query(self, sql, args=(), one=False):
        self.cur.execute(sql, args)
        r = [dict((self.cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in self.cur.fetchall()]
        return (r[0] if r else None) if one else r

    def execute(self, sql, args=()):
        self.cur.execute(sql, args)

    def commit(self):
        self.conn.commit()

    def close(self):
        if hasattr(self, 'cur'):
            self.cur.close()  # Close the cursor
        if hasattr(self, 'conn'):
            self.conn.close()  # Close the connection