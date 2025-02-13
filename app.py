from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import database.db_connector as db

app = Flask(__name__)

# Load environment variables and validate
load_dotenv()

required_vars = ["340DBHOST", "340DBUSER", "340DBPW", "340DB"]
for var in required_vars:
    if not os.environ.get(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Database configuration
app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

db_connection = db.connect_to_database()
mysql = MySQL(app)

# ------------------------------ NAVIGATION BAR ------------------------------
NAV_LINKS = [
    {"name": "Home", "url": "/"},
    {"name": "Anime", "url": "/anime"},
    {"name": "App Users", "url": "/app-users"},
    {"name": "Streaming Services", "url": "/streaming-services"},
    {"name": "Streaming Anime", "url": "/streaming-anime"},
    {"name": "Streaming Service Users", "url": "/streaming-service-users"},
    {"name": "User Anime Ratings", "url": "/user-anime-ratings"},
]

# ------------------------------ ROUTES ------------------------------

@app.route('/')
def root():
    return render_template("main.j2", nav_links=NAV_LINKS)

@app.route('/anime')
def anime():
    query = "SELECT * FROM anime;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Anime", data=results)

@app.route('/app-users')
def app_users():
    query = "SELECT * FROM app_users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="App Users", data=results)

@app.route('/streaming-services')
def streaming_services():
    query = "SELECT * FROM streaming_services;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Services", data=results)

@app.route('/streaming-anime')
def streaming_anime():
    query = "SELECT * FROM streaming_anime;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Anime", data=results)

@app.route('/streaming-service-users')
def streaming_service_users():
    query = "SELECT * FROM streaming_service_users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Service Users", data=results)

@app.route('/user-anime-ratings')
def user_anime_ratings():
    query = "SELECT * FROM user_anime_ratings;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="User Anime Ratings", data=results)

# ------------------------------ RUN APP ------------------------------
if __name__ == "__main__":
    app.run(port=3000, debug=True)
