# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy import create_engine, text, Table, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError
import pyodbc
from datetime import datetime  # Ensure proper import


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Set up template environment
env = Environment(loader=FileSystemLoader('templates'))

# Database connection setup (SQLAlchemy example)
DATABASE_URL = "mssql+pyodbc://CloudSA8bd104de:KQxaecGh7K6V@top-insights-dev.database.windows.net/top-insights-dev-db1?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(DATABASE_URL)

# Function to log events into Azure SQL Database
def log_event(user_id, event_type, event_description, page_url, browser_info, ip_address):
    insert_query = """
    INSERT INTO [snow].[topsphere_WebAppLogs] (UserID, EventType, EventDescription, PageURL, BrowserInfo, IPAddress)
    VALUES (:user_id, :event_type, :event_description, :page_url, :browser_info, :ip_address);
    """
    try:
        with engine.connect() as connection:
            print(f"Attempting to execute query: {insert_query}")
            result = connection.execute(
                text(insert_query),
                {"user_id": user_id, "event_type": event_type, "event_description": event_description, "page_url": page_url, "browser_info": browser_info, "ip_address": ip_address}
            )
            connection.commit()  # Explicitly commit the transaction

            print("Query executed successfully.")
            print(f"Result: {result}")
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        # You can also log this error to a file or monitoring system        


# Function to log uptime/downtime events
def log_uptime_event(event_type):
    insert_query = """
    INSERT INTO [snow].[UptimeLogs] (EventType, EventTime)
    VALUES (:event_type, :event_time);
    """
    
    try:
        with engine.connect() as connection:
            print(f"Attempting to log event: {event_type}")
            result = connection.execute(
                text(insert_query),
                {
                    "event_type": event_type,
                    "event_time": datetime.now()  # Correct usage
                }
            )
            connection.commit()  # Explicitly commit the transaction
            print("Uptime event logged successfully.")
            print(f"Result: {result}")
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        # Optionally, log the error to a monitoring system or a file

# Example usage
log_uptime_event('Uptime')  

# Function to log uptime/downtime events
# Function to log uptime/downtime events
def log_uptime_event(event_type):
    insert_query = """
    INSERT INTO [snow].[topsphere_application_Logs] (EventType, EventTime)
    VALUES (:event_type, :event_time);
    """
    
    try:
        with engine.connect() as connection:
            print(f"Attempting to log event: {event_type}")
            result = connection.execute(
                text(insert_query),
                {
                    "event_type": event_type,
                    "event_time": datetime.now()
                }
            )
            connection.commit()  # Explicitly commit the transaction
            print("Uptime event logged successfully.")
            print(f"Result: {result}")
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        # Optionally, log the error to a monitoring system or a file

# Example usage
log_uptime_event('Uptime')

# Chatbot route (POST request to handle user input)
@app.post("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request, user_input: str = Form(...)):
    # Connect to the database
    with engine.connect() as connection:
        # Query the FAQ table for a matching response
        query = text(f"SELECT answer FROM [snow].[chatbot_faq] WHERE question LIKE :input")
        result = connection.execute(query, {"input": f"%{user_input}%"})
        response = result.fetchone()

    # Return the response to the template
    #return templates.TemplateResponse("chat.html", {"request": request, "user_input": user_input, "bot_response": bot_response})
    # Return the response to the template
    return HTMLResponse(content=f"""
        <div class="chatbot-message">{response}</div>
    """)


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

# Define the Snowgate page route
@app.get("/snowgate", response_class=HTMLResponse)
async def snowgate(request: Request):

    user_id = "example_user"  # Replace with actual user identification
    page_url = request.url.path
    browser_info = request.headers.get('User-Agent', 'Unknown')
    ip_address = request.client.host
    
    # Log page visit
    log_event(user_id, "Page Visit", "Visited the Snowgate page", page_url, browser_info, ip_address)
    
    return templates.TemplateResponse("snowgate.html", {"request": request})


