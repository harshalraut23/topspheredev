# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
import pandas as pd

# Function to connect to Azure SQL Database and fetch data
def get_data_from_azure_sql(query):
    server = 'top-insights-dev.database.windows.net'
    database = 'top-insights-dev-db1'
    username = 'CloudSA8bd104de'
    password = 'KQxaecGh7K6V'
    
    connection_string = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )
    
    engine = create_engine(connection_string)
    df = pd.read_sql(query, engine)
    return df

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Fetch reports data from Azure SQL
    query_reports = "SELECT * FROM snow.techops_reports WHERE section <> 'Success Stories'"
    df_reports = get_data_from_azure_sql(query_reports)
    
    # Process the data into sections and reports
    sections = {}
    for _, row in df_reports.iterrows():
        section = row['section']
        if section not in sections:
            sections[section] = []
        sections[section].append({
            "title": row['title'],
            "weburl": row['weburl']
        })
    
    # Pass sections to the template
    return templates.TemplateResponse("index.html", {"request": request, "sections": sections})