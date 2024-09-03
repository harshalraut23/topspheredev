# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
import pandas as pd
import os
from jinja2 import Template


app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Function to connect to Azure SQL Database and fetch data
# def get_data_from_azure_sql(query):
#     server = 'top-insights-dev.database.windows.net'
#     database = 'top-insights-dev-db1'
#     username = 'CloudSA8bd104de'
#     password = 'KQxaecGh7K6V'
    
#     connection_string = (
#         f"mssql+pyodbc://{username}:{password}@{server}/{database}"
#         f"?driver=ODBC+Driver+17+for+SQL+Server"
#     )
    
#     engine = create_engine(connection_string)
#     df = pd.read_sql(query, engine)
#     return df

# # Fetch reports data from Azure SQL
# query_reports = "SELECT * FROM snow.techops_reports"
# df_reports = get_data_from_azure_sql(query_reports)

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     # Generate the HTML content
#     # with open("templates/index.html") as file:
#     #     template = Template(file.read())
#     # reports_links = '\n'.join(f'<li><a href="/reports/{row["id"]}">{row["report_name"]}</a></li>' for index, row in df_reports.iterrows())
#     # html_content = template.render(title="techOps sphere", reports_links=reports_links)
#     return HTMLResponse(content=html_content)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

# @app.get("/reports/{report_id}", response_class=HTMLResponse)
# async def read_report(report_id: int):
#     # Fetch and render specific report details here
#     return HTMLResponse(content=f"<h1>Report ID: {report_id}</h1>")
