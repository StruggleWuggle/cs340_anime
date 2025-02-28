from flask import Flask, render_template, request

import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import db_connector as db


app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = os.environ.get("DB_HOST")
app.config['MYSQL_USER'] = os.environ.get("DB_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("DB_NAME")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
for var in required_vars:
    if not os.environ.get(var):
        raise ValueError(f"Missing required environment variable: {var}")
    
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

def fetch_data(query, params=None):
    cur = mysql.connection.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return results


@app.route('/anime')
def anime():
    search_query = request.args.get("search")
    if search_query:
        query = "SELECT * FROM anime WHERE title LIKE %s;"
        results = fetch_data(query, (f"%{search_query}%",))
    else:
        query = "SELECT * FROM anime;"
        results = fetch_data(query)
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Anime", data=results)

@app.route('/app-users')
def app_users():
    results = fetch_data("SELECT * FROM app_users;")
    return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="App Users", data=results)

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
    app.run(port=5550, debug=True)
