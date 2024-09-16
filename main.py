# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy import create_engine, text
import pyodbc


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Set up template environment
env = Environment(loader=FileSystemLoader('templates'))

# Database connection setup (SQLAlchemy example)
DATABASE_URL = "mssql+pyodbc://CloudSA8bd104de:KQxaecGh7K6V@top-insights-dev.database.windows.net/top-insights-dev-db1?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)

# Chatbot route (POST request to handle user input)
@app.post("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request, user_input: str = Form(...)):
    # Connect to the database
    with engine.connect() as connection:
        # Query the FAQ table for a matching response
        query = text(f"SELECT response FROM [snow].[chatbot_faq] WHERE question LIKE :input")
        result = connection.execute(query, {"input": f"%{user_input}%"})
        response = result.fetchone()

    if response:
        bot_response = response[0]
    else:
        bot_response = "Sorry, I don't understand your question."

    # Return the response to the template
    return templates.TemplateResponse("chat.html", {"request": request, "user_input": user_input, "bot_response": bot_response})


# Define route to render your HTML files
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    template = env.get_template("index.html")
    content = template.render()
    return HTMLResponse(content=content)

       
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Report 1 page
@app.get("/report1", response_class=HTMLResponse)
async def report1(request: Request):
    return templates.TemplateResponse("report1.html", {"request": request})

# Report 2 page
@app.get("/report2", response_class=HTMLResponse)
async def report2(request: Request):
    return templates.TemplateResponse("report2.html", {"request": request})

# Report 3 page
@app.get("/report3", response_class=HTMLResponse)
async def report3(request: Request):
    return templates.TemplateResponse("report3.html", {"request": request})

# Define the TOPVista page route
@app.get("/topvista", response_class=HTMLResponse)
async def topvista(request: Request):
    return templates.TemplateResponse("topvista.html", {"request": request})
    