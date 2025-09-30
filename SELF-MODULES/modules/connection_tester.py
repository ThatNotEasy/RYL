from lib.sqlserver import SQLSERVER

def test_connection():
    db = SQLSERVER()
    result = db.query(sql={"query": "SELECT * FROM sys.databases;"})
    print(result)
    db.close()
    return result

if __name__ == "__main__":
    test_connection()