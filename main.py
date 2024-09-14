# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template, Environment, FileSystemLoader
import pyodbc

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Set up template environment
env = Environment(loader=FileSystemLoader('templates'))

# Database connection setup (example, adjust for your case)
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=top-insights-dev.database.windows.net;'
        'DATABASE=top-insights-dev-db1;'
        'UID=CloudSA8bd104de;'
        'PWD=KQxaecGh7K6V;'
    )
    return conn

# Define route to render your HTML files
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    template = env.get_template("index.html")
    content = template.render()
    return HTMLResponse(content=content)

# You can add the chatbot endpoint here
@app.post("/chatbot")
async def chatbot_query(request: Request):
    # Handle user input and respond using database or logic
    data = await request.json()
    user_message = data.get('message')
    
    # Connect to DB and get a response from your SQL data (example)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM chatbot_responses WHERE question=?", (user_message,))
    row = cursor.fetchone()

    if row:
        return {"response": row[0]}
    else:
        return {"response": "Sorry, I don't have an answer for that."}
    
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
    