# main.py
from fastapi import FastAPI
import pyodbc

app = FastAPI()

def test_db_connection():
    server = 'top-insights-dev.database.windows.net'
    database = 'top-insights-dev-db1'
    username = 'CloudSA8bd104de'
    password = 'KQxaecGh7K6V'
    driver = '{ODBC Driver 17 for SQL Server}'
    
    try:
        with pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes'
        ) as conn:
            return True
    except Exception as e:
        return str(e)

@app.get("/test-db-connection")
async def test_db():
    result = test_db_connection()
    if result is True:
        return {"status": "Connection successful"}
    else:
        return {"status": "Connection failed", "error": result}
