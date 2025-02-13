from flask import Flask, render_template
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

mysql = MySQL(app)

NAV_LINKS = [
    {"name": "Home", "url": "/"},
    {"name": "Anime", "url": "/anime"},
    {"name": "App Users", "url": "/app-users"},
    {"name": "Streaming Services", "url": "/streaming-services"},
    {"name": "Streaming Anime", "url": "/streaming-anime"},
    {"name": "Streaming Service Users", "url": "/streaming-service-users"},
    {"name": "User Anime Ratings", "url": "/user-anime-ratings"},
]

@app.route('/')
def root():
    return render_template("main.j2", nav_links=NAV_LINKS)

def fetch_data(query):
    db_connection = db.connect_to_database()
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return results

@app.route('/anime')
def anime():
    results = fetch_data("SELECT * FROM anime;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Anime", data=results)

@app.route('/app-users')
def app_users():
    results = fetch_data("SELECT * FROM app_users;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="App Users", data=results)

# TODO decide how to handel junctions

@app.route('/streaming-services')
def streaming_services():
    results = fetch_data("SELECT * FROM streaming_services;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Services", data=results)

@app.route('/streaming-anime')
def streaming_anime():
    results = fetch_data("SELECT * FROM streaming_anime;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Anime", data=results)

@app.route('/streaming-service-users')
def streaming_service_users():
    results = fetch_data("SELECT * FROM streaming_service_users;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Service Users", data=results)

@app.route('/user-anime-ratings')
def user_anime_ratings():
    results = fetch_data("SELECT * FROM user_anime_ratings;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="User Anime Ratings", data=results)

# ------------------------------ RUN APP ------------------------------
if __name__ == "__main__":
    app.run(port=3000, debug=True)
