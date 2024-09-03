from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Function to get data from Azure SQL
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

# Data model for response
class Report(BaseModel):
    title: str
    section: str
    weburl: str

@app.get("/reports", response_model=Dict[str, List[Report]])
async def get_reports():
    query_reports = "SELECT * FROM snow.techops_reports where section <> 'Success Stories'"
    df_reports = get_data_from_azure_sql(query_reports)
    
    # Group reports by section
    grouped_reports = df_reports.groupby('section').apply(lambda x: x.to_dict(orient='records')).to_dict()
    
    # Convert to the desired format
    reports = {section: [Report(**report) for report in reports_list] 
               for section, reports_list in grouped_reports.items()}
    
    return reports

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
