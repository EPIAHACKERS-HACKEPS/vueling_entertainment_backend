import sqlite3

database = "database.db"

def dropTable(tablename):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE IF EXISTS "+tablename+" ;")
    conn.commit()
    conn.close()

def GenerateDataBases():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    db_airport_drop = "DROP TABLE IF EXISTS airports;"
    db_kahoot_drop = "DROP TABLE IF EXISTS preguntas;"
    db_users_drop = "DROP TABLE IF EXISTS usuarios;"
    db_leaderboard_drop = "DROP TABLE IF EXISTS leaderboard_table;"
    db_incidencias_drop = "DROP TABLE IF EXISTS incidencias;"
    db_passagers_drop = "DROP TABLE IF EXISTS pasajeros;"

    db_airport_create = "CREATE TABLE IF NOT EXISTS airports (code TEXT PRIMARY KEY, lat TEXT, lon TEXT, name TEXT, city TEXT, state TEXT, country TEXT, woeid TEXT, tz TEXT, phone TEXT, type TEXT, email TEXT, url TEXT, runway_length TEXT, elev TEXT, icao TEXT, direct_flights TEXT, carriers TEXT);"
    db_kahoot_create = "CREATE TABLE preguntas (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, opcion_a TEXT NOT NULL, opcion_b TEXT NOT NULL, opcion_c TEXT NOT NULL, opcion_d TEXT NOT NULL, respuesta TEXT NOT NULL);"
    db_users_create = "CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL, contrasena TEXT NOT NULL, apikey TEXT NOT NULL)"
    db_leaderboard = "CREATE TABLE IF NOT EXISTS leaderboard_table (id INTEGER PRIMARY KEY, nickname TEXT, asiento INTEGER, puntos INTEGER, FOREIGN KEY (asiento) REFERENCES pasajeros (seat));"
    db_incidencias = "CREATE TABLE IF NOT EXISTS incidencias ( id INTEGER PRIMARY KEY, seat TEXT NOT NULL, type TEXT NOT NULL, comments TEXT, active INTEGER DEFAULT 1, timestamp_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, timestamp_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (seat) REFERENCES pasajeros (seat));"
    db_passagers = "CREATE TABLE IF NOT EXISTS pasajeros (seat TEXT PRIMARY KEY, name TEXT NOT NULL, surnames TEXT NOT NULL, id_card TEXT NOT NULL, email TEXT NOT NULL);"




    cursor.execute(db_airport_drop)
    cursor.execute(db_kahoot_drop)
    cursor.execute(db_users_drop)
    cursor.execute(db_leaderboard_drop)
    cursor.execute(db_incidencias_drop)
    cursor.execute(db_passagers_drop)

    cursor.execute(db_airport_create)
    cursor.execute(db_kahoot_create)
    cursor.execute(db_users_create)
    cursor.execute(db_leaderboard)
    cursor.execute(db_incidencias)
    cursor.execute(db_passagers)

    conn.commit()
    conn.close()

def insertKahootQuest(pregunta, opciones):
    """Inserta una pregunta y sus opciones en la tabla 'preguntas' de la base de datos"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO preguntas (question, opcion_a, opcion_b, opcion_c, opcion_d, respuesta) VALUES (?, ?, ?, ?, ?, ?)''', (pregunta, opciones[0], opciones[1], opciones[2], opciones[3], opciones[4]))
    conn.commit()
    conn.close()

def insertAirportsData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO airports (code, lat, lon, name, city, state, country, woeid, tz, phone, type, email, url, runway_length, elev, icao, direct_flights, carriers) VALUES ('AAA', '-17.3595', '-145.494', 'Anaa Airport', 'Anaa', 'Tuamotu-Gambier', 'French Polynesia', '12512819', 'Pacific/Midway', '', 'Airports', '', '', '4921', '7', 'NTGA', '2', '1');"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insertPasajerosData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO pasajeros (seat, name, surnames, id_card, email) VALUES (?, ?, ?, ?, ?);"
    values = ("1A", "Juan", "Pérez Sánchez", "12345678A", "juanperez@example.com")
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def insertUserData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (usuario, contrasena, apikey) VALUES ('user1', 'pass1', 'key1');"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insertLeaderboardData(seat,pts,nickname):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO leaderboard_table (nickname, asiento, puntos) VALUES ('?', '?', ?);", (nickname, seat, pts)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insertIncidenciasData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO incidences (seat, type, comments, active) VALUES ('1A', 'delay', 'Flight delayed 2 hours', 1);"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def insertPasajerosData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO pasajeros (seat, name, surnames, id_card, email) VALUES ('1A', 'John', 'Doe', '12345678A', 'johndoe@example.com');"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def getLeaderboard():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "SELECT * FROM leaderboard_table ORDER BY puntos DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result


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
    sql = "UPDATE usuarios SET usuario = ?, contrasena = ? WHERE id = ?;"
    cursor.execute(sql, (username, password, id))
    conn.commit()
    conn.close()

def updateLeaderboardData(id, points):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE leaderboard_table SET puntos = ? WHERE id = ?;"
    cursor.execute(sql, (points, id))
    conn.commit()
    conn.close()

def updateIncidencesData(id, comments):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE incidences SET comments = ? WHERE id = ?;"
    cursor.execute(sql, (comments, id))
    conn.commit()
    conn.close()

def updatePassagersData(id, email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "UPDATE pasajeros SET email = ? WHERE id = ?;"
    cursor.execute(sql, (email, id))
    conn.commit()
    conn.close()









def get_random_questions(num_preguntas=10):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM preguntas ORDER BY RANDOM() LIMIT {num_preguntas};')
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




