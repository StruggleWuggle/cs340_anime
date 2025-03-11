from flask import Flask, render_template, request, jsonify
import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os


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

# helper to execute database queries
def execute_query(query, params=None, fetch=False):
    cur = mysql.connection.cursor()
    cur.execute(query, params) if params else cur.execute(query)
    data = cur.fetchall() if fetch else None
    mysql.connection.commit()
    cur.close()
    return data

# ANIME
@app.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'GET':
        search_query = request.args.get("search")
        if search_query:
            query = "SELECT * FROM anime WHERE title LIKE %s;"
            results = fetch_data(query, (f"%{search_query}%",))
        else:
            query = "SELECT * FROM anime;"
            results = fetch_data(query)
        return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Anime", data=results)

    elif request.method == 'POST':
        data = request.get_json()
    
        # Check if all required fields are present
        required_fields = ["title", "start_date", "service_id", "genre", "maturity_rating", "num_episodes"]
        if not data or any(field not in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Check optional fields
        end_date = data.get("end_date", None)
        trigger_warnings = data.get("trigger_warnings", None)

        query = """INSERT INTO anime (title, start_date, end_date, service_id, genre, 
                                    maturity_rating, trigger_warnings, num_episodes) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

        execute_query(query, (
            data['title'], data['start_date'], end_date, data['service_id'],
            data['genre'], data['maturity_rating'], trigger_warnings, data['num_episodes']
        ))
        return jsonify({"message": "Anime added successfully"}), 201

@app.route('/anime/<int:anime_id>', methods=['PUT'])
def update_anime(anime_id):
    data = request.get_json()

    # Check if data is provided
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # GET prev anime match
    existing_anime = fetch_data("SELECT * FROM anime WHERE anime_id = %s;", (anime_id,))[0]

    # Check for match    
    if not existing_anime:
        return jsonify({"error": "Anime not found"}), 404

    # Compare data body with existing database data. Overwrite any matches
    fields = ["title", "start_date", "end_date", "service_id", "genre", "maturity_rating", "trigger_warnings", "num_episodes"]
    updated_data = {field: data.get(field, existing_anime[field]) for field in fields}

    # Construct the SQL query dynamically
    set_clause = ", ".join(f"{field} = %s" for field in updated_data.keys())
    query = f"UPDATE anime SET {set_clause} WHERE anime_id = %s;"

    execute_query(query, tuple(updated_data.values()) + (anime_id,))
    return jsonify({"message": "Anime updated successfully"}), 200

@app.route('/anime/<int:anime_id>', methods=['DELETE'])
def delete_anime(anime_id):
    # Check if anime exists
    existing_anime = fetch_data("SELECT * FROM anime WHERE anime_id = %s;", (anime_id,))
    if not existing_anime:
        return jsonify({"error": "Anime not found"}), 404

    # Delete anime
    query = "DELETE FROM anime WHERE anime_id = %s;"
    execute_query(query, (anime_id,))
    return jsonify({"message": "Anime deleted successfully"}), 200


# APP USERS
@app.route('/app-users', methods=['GET', 'POST'])
def app_users():
    if request.method == 'GET':
        results = fetch_data("SELECT * FROM app_users;")
        return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="App Users", data=results)
    
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        required_fields = ["name", "password", "age", "gender", "location"]
        
        # Check if all required fields are present
        if not data or any(field not in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        query = """INSERT INTO app_users (name, password, age, gender, location) VALUES (%s, %s, %s, %s, %s);
        """
        execute_query(query, (data['name'], data['password'], data['age'], data['gender'], data['location']))
        return jsonify({"message": "User added successfully"}), 201
    
@app.route('/app-users/<int:user_id>', methods=['PUT'])
def update_app_user(user_id):
    data = request.get_json()

    # Check if data is provided
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Get prev app users match
    existing_user = fetch_data("SELECT * FROM app_users WHERE app_user_id = %s;", (user_id,))[0]

    # Check for match    
    if not existing_user:
        return jsonify({"error": "User not found"}), 404

    # Compare data body with existing database data. Overwrite any matches
    fields = ["name", "password", "age", "gender", "location"]
    updated_data = {field: data.get(field, existing_user[field]) for field in fields}

    # Construct the SQL query dynamically
    set_clause = ", ".join(f"{field} = %s" for field in updated_data.keys())
    query = f"UPDATE app_users SET {set_clause} WHERE app_user_id = %s;"

    execute_query(query, tuple(updated_data.values()) + (user_id,))
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/app-users/<int:user_id>', methods=['DELETE'])
def delete_app_user(user_id):

    # Check if the user exists
    existing_user = fetch_data("SELECT * FROM app_users WHERE app_user_id = %s;", (user_id,))
    
    if not existing_user:
        return jsonify({"error": "User not found"}), 404

    # Delete user
    query = "DELETE FROM app_users WHERE app_user_id = %s;"
    execute_query(query, (user_id,))
    return jsonify({"message": "User deleted successfully"}), 200

    
# STREAMING SERVICES
@app.route('/streaming-services', methods=['GET', 'POST'])
def streaming_services():
    if request.method == 'GET':
        results = fetch_data("SELECT * FROM streaming_services;")
        return render_template("table_template.j2", nav_links=NAV_LINKS, table_title="Streaming Services", data=results)
    
    elif request.method == 'POST':
        data = request.get_json(force=True)
        print(data)
        if not data or 'service_name' not in data:
            return jsonify({"error": "Missing 'service_name' field"}), 400
    
        query = "INSERT INTO streaming_services (service_name) VALUES (%s);"
        execute_query(query, (data['service_name'],))
        return jsonify({"message": "Streaming service added successfully"}), 201
    
@app.route('/streaming-services/<int:service_id>', methods=['PUT'])
def update_streaming_service(service_id):
    data = request.get_json()
    if not data or 'service_name' not in data:
        return jsonify({"error": "Missing 'service_name' field"}), 400

    query = "UPDATE streaming_services SET service_name = %s WHERE id = %s;"
    execute_query(query, (data['service_name'], service_id))
    return jsonify({"message": "Streaming service updated successfully"}), 200

@app.route('/streaming-services/<int:service_id>', methods=['DELETE'])
def delete_streaming_service(service_id):
    query = "DELETE FROM streaming_services WHERE id = %s;"
    execute_query(query, (service_id,))
    return jsonify({"message": "Streaming service deleted successfully"}), 200

# ------------------------
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
