import sqlite3
import hashlib
import random
import requests
import json

apikey_weather = 'c609ebc8980942c48e492252231305'
database = "database.db"

def dropTable(tablename):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM "+tablename+" ;")
    conn.commit()
    conn.close()



def get_current_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={apikey_weather}&q={city}&aqi=yes"
        response = requests.get(url)
        data = json.loads(response.text)
        current_weather = {
            "temperature_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"]
        }
    except:
        current_weather = {
            "temperature_c": "NOT AVAILABLE",
            "condition": "NOT AVAILABLE",
            "icon": "NOT AVAILABLE"
        }
    return current_weather

def GenerateDataBases():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    db_users_drop = "DROP TABLE IF EXISTS users;"
    db_places_drop = "DROP TABLE IF EXISTS places;"
    db_airport_drop = "DROP TABLE IF EXISTS airports;"
    db_kahoot_drop = "DROP TABLE IF EXISTS questions;"
    db_incidences_drop = "DROP TABLE IF EXISTS incidents;"
    db_passengers_drop = "DROP TABLE IF EXISTS passengers;"
    db_leaderboard_drop = "DROP TABLE IF EXISTS leaderboard_table;"
    db_places_passagers_drop = "DROP TABLE IF EXISTS places_passagers;"


    db_airport_create = "CREATE TABLE IF NOT EXISTS airports (code TEXT PRIMARY KEY, lat TEXT, lon TEXT, name TEXT, city TEXT, state TEXT, country TEXT, woeid TEXT, tz TEXT, phone TEXT, type TEXT, email TEXT, url TEXT, runway_length TEXT, elev TEXT, icao TEXT, direct_flights TEXT, carriers TEXT);"
    db_kahoot_create = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, option_a TEXT NOT NULL, option_b TEXT NOT NULL, option_c TEXT NOT NULL, option_d TEXT NOT NULL, answer TEXT NOT NULL);"
    db_users_create = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, password TEXT NOT NULL, apikey TEXT NOT NULL);"
    db_leaderboard = "CREATE TABLE IF NOT EXISTS leaderboard_table (id INTEGER PRIMARY KEY, nickname TEXT, seat INTEGER, points INTEGER, FOREIGN KEY (seat) REFERENCES passengers (seat));"
    db_incidents = "CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY, seat TEXT NOT NULL, type TEXT NOT NULL, comments TEXT, active INTEGER DEFAULT 1, timestamp_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, timestamp_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (seat) REFERENCES passengers (seat));"
    db_passengers = "CREATE TABLE IF NOT EXISTS passengers (seat TEXT PRIMARY KEY, name TEXT NOT NULL, surnames TEXT NOT NULL, id_card TEXT NOT NULL, email TEXT NOT NULL);"
    db_places = "CREATE TABLE IF NOT EXISTS places (id INTEGER PRIMARY KEY,campo TEXT,username TEXT,asistentes TEXT);"


    cursor.execute(db_airport_drop)
    cursor.execute(db_kahoot_drop)
    cursor.execute(db_users_drop)
    cursor.execute(db_leaderboard_drop)
    cursor.execute(db_places_drop)
    cursor.execute(db_incidences_drop)
    cursor.execute(db_passengers_drop)
    cursor.execute(db_places_passagers_drop)

    cursor.execute(db_airport_create)
    cursor.execute(db_kahoot_create)
    cursor.execute(db_users_create)
    cursor.execute(db_leaderboard)
    cursor.execute(db_incidents)
    cursor.execute(db_passengers)
    cursor.execute(db_places)
    
    conn.commit()
    conn.close()


def insertKahootQuest(question, options):
    """Inserts a question and its options in the 'questions' table of the database"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer) VALUES (?, ?, ?, ?, ?, ?)''', (question, options[0], options[1], options[2], options[3], options[4]))
    conn.commit()
    conn.close()

def insertAirportsData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO airports (code, lat, lon, name, city, state, country, woeid, tz, phone, type, email, url, runway_length, elev, icao, direct_flights, carriers) VALUES ('AAA', '-17.3595', '-145.494', 'Anaa Airport', 'Anaa', 'Tuamotu-Gambier', 'French Polynesia', '12512819', 'Pacific/Midway', '', 'Airports', '', '', '4921', '7', 'NTGA', '2', '1');"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insertPasajerosData(seat,name,surnames,id_card,email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO passengers (seat, name, surnames, id_card, email) VALUES (?, ?, ?, ?, ?);"
    values = (seat,name,surnames,id_card,email)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()


def insertUserData(user,password):
    password = hashlib.sha256(password.encode()).hexdigest()
    apikey = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = f"INSERT INTO users (user, password, apikey) VALUES ('{user}', '{password}', '{apikey}');"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insertLeaderboardData(nickname, seat, pts):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO leaderboard_table (nickname, seat, points) VALUES (?, ?, ?);"
    cursor.execute(sql, (nickname, seat, pts))
    conn.commit()
    sql = "DELETE FROM leaderboard_table WHERE nickname = '"+nickname+"' AND points < ( SELECT MAX(points) FROM leaderboard_table WHERE nickname = '"+nickname+"');"
    cursor.execute(sql)
    conn.commit()
    conn.close()



def insertIncidenciasData(seat,type,comments="No Comments"):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = f"INSERT INTO incidents (seat, type, comments, active) VALUES ('{seat}', '{type}', '{comments}', 1);"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def updatePassagersData(seat,name,surname,id_card,email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE passengers SET email = ? WHERE id = ?;"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def getLeaderboard():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "SELECT * FROM leaderboard_table ORDER BY points DESC LIMIT 50;"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result




def getPlaces():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "SELECT * FROM places"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

def updatePlaces(place, username):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = f"SELECT asistentes FROM places where campo = '{place}';"
    cursor.execute(sql)
    asistents = cursor.fetchall()[0][0]
    asistents+=(","+username)
    sql = "UPDATE places SET asistentes = ? WHERE campo = ?;"
    cursor.execute(sql, (asistents, place))
    conn.commit()
    conn.close()

def insertPlaces(place, username):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO places (campo, username, asistentes)VALUES ('?', '?', '');"
    cursor.execute(sql,(place,username))
    conn.commit()
    conn.close()

def updateAirportsData(code, name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE airports SET name = ? WHERE code = ?;"
    cursor.execute(sql, (name, code))
    conn.commit()
    conn.close()

def updateUsersData(id, username, password):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE users SET username = ?, password = ? WHERE id = ?;"
    cursor.execute(sql, (username, password, id))
    conn.commit()
    conn.close()

def updateLeaderboardData(id, points):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE leaderboard_table SET points = ? WHERE id = ?;"
    cursor.execute(sql, (points, id))
    conn.commit()
    conn.close()

def updateIncidencesData(id, comments):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE incidents SET comments = ? WHERE id = ?;"
    cursor.execute(sql, (comments, id))
    conn.commit()
    conn.close()

def updatePassagersData(id, email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE passengers SET email = ? WHERE id = ?;"
    cursor.execute(sql, (email, id))
    conn.commit()
    conn.close()


def get_random_questions(num_questions=10):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM questions ORDER BY RANDOM() LIMIT {num_questions};')
    preguntas = []
    for row in cursor.fetchall():
        pregunta = {
            'id': row[0],
            'question': row[1],
            'optionA': row[2],
            'optionB': row[3],
            'optionC': row[4],
            'optionD': row[5],
            'answer': '',
            'correctAnswer': row[6]
        }
        preguntas.append(pregunta)
    conn.close()
    return preguntas




