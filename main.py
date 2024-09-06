# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Report 1 page
@app.get("/report1", response_class=HTMLResponse)
async def report1(request: Request):
    return templates.TemplateResponse("report1.html", {"request": request})

# Report 2 page
@app.get("/report2", response_class=HTMLResponse)
async def report1(request: Request):
    return templates.TemplateResponse("report2.html", {"request": request})

# Report 3 page
@app.get("/report3", response_class=HTMLResponse)
async def report1(request: Request):
    return templates.TemplateResponse("report3.html", {"request": request})