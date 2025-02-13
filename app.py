from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file and check that all requred enviormental variables are present
load_dotenv()

required_vars = ["340DBHOST", "340DBUSER", "340DBPW", "340DB"]
for var in required_vars:
    if not os.environ.get(var):
        raise ValueError(f"Missing required environment variable: {var}")


app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    query = "SELECT * FROM diagnostic;"
    query1 = 'DROP TABLE IF EXISTS diagnostic;';
    query2 = 'CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);';
    query3 = 'INSERT INTO diagnostic (text) VALUES ("MySQL is working for yourONID!")';
    query4 = 'SELECT * FROM diagnostic;';
    cur = mysql.connection.cursor()
    cur.execute(query1)
    cur.execute(query2)
    cur.execute(query3)
    cur.execute(query4)
    results = cur.fetchall()

    return "<h1>MySQL Results</h1>" + str(results[0])


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=3000, debug=True)