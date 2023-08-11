from configparser import ConfigParser
import mysql.connector

config = ConfigParser()
config.sections()
config.read('config.ini')

# DATABASE = config['MYSQL']["DATABASE"]
HOSTNAME = config['MYSQL']["HOSTNAME"]
USERNAME = config['MYSQL']["USERNAME"]
PASSWORD = config['MYSQL']["PASSWORD"]
PORT = config['MYSQL']["PORT"]
PLUGIN = config['MYSQL']['PLUGIN']

class MYSQL():

    def __init__(self, host=HOSTNAME, username=USERNAME, password=PASSWORD, port=PORT, plugin=PLUGIN):
        self.host = host
        self.username = username
        self.password = password
        self.plugin = plugin
        self.port = port
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password, 
            port=self.port, 
            auth_plugin=self.plugin
            )
            self.cur = self.conn.cursor()
        except Exception as err:
            print(f"Error at connection, Error info: {err}")
    
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
        self.conn.close()
