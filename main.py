# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template, Environment, FileSystemLoader


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Set up template environment
env = Environment(loader=FileSystemLoader('templates'))

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
    