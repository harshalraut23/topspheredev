from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse  # Import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templating
templates = Jinja2Templates(directory="templates")

# Database connection details
# server = 'top-insights-dev.database.windows.net'
# database = 'top-insights-dev-db1'
# username = 'CloudSA8bd104de'
# password = 'KQxaecGh7K6V'
# connection_string = (
#     f"mssql+pyodbc://{username}:{password}@{server}/{database}"
#     f"?driver=ODBC+Driver+17+for+SQL+Server"
# )

# Create SQLAlchemy engine and session
# engine = create_engine(connection_string)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to fetch data from the database
# def get_data_from_azure_sql(query):
#     with engine.connect() as connection:
#         df = pd.read_sql(query, connection)
#     return df

# Fetch reports data
# query_reports = "SELECT * FROM snow.techops_reports"
# df_reports = get_data_from_azure_sql(query_reports)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home"})

# @app.get("/reports", response_class=HTMLResponse)
# async def reports(request: Request):
#     return templates.TemplateResponse("reports.html", {"request": request, "title": "Reports"})

#@app.get("/documentation", response_class=HTMLResponse)
#async def documentation(request: Request):
#    return templates.TemplateResponse("documentation.html", {"request": request, "title": "Documentation"})

#@app.get("/feedback", response_class=HTMLResponse)
#async def feedback(request: Request):
#    return templates.TemplateResponse("feedback.html", {"request": request, "title": "Feedback"})

#@app.get("/request", response_class=HTMLResponse)
#async def request_page(request: Request):
#    return templates.TemplateResponse("request.html", {"request": request, "title": "Request"})

#@app.get("/brands", response_class=HTMLResponse)
#async def brands(request: Request):
#    return templates.TemplateResponse("brands.html", {"request": request, "title": "Brands"})

#@app.get("/products", response_class=HTMLResponse)
#async def products(request: Request):
#    return templates.TemplateResponse("products.html", {"request": request, "title": "Products"})

# Run the app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
