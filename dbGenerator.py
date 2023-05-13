import sqlite3

database = "database.db"

def GenerateDataBases():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    db_airport_drop = "DROP TABLE IF EXISTS airports;"
    db_airport_create = "CREATE TABLE airports (code TEXT, lat TEXT, lon TEXT, name TEXT, city TEXT, state TEXT, country TEXT, woeid TEXT, tz TEXT, phone TEXT, type TEXT, email TEXT, url TEXT, runway_length TEXT, elev TEXT, icao TEXT, direct_flights TEXT, carriers TEXT);"
    db_kahoot_drop = "DROP TABLE IF EXISTS preguntas;"
    db_kahoot_create = "CREATE TABLE preguntas (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, opcion_a TEXT NOT NULL, opcion_b TEXT NOT NULL, opcion_c TEXT NOT NULL, opcion_d TEXT NOT NULL, respuesta TEXT NOT NULL);"
    cursor.execute(db_airport_drop)
    cursor.execute(db_airport_create)
    cursor.execute(db_kahoot_drop)
    cursor.execute(db_kahoot_create)
    conn.commit()
    conn.close()

def insertKahootQuest(pregunta, opciones):
    """Inserta una pregunta y sus opciones en la tabla 'preguntas' de la base de datos"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    print(opciones)
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

def get_random_questions(num_preguntas=10):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM preguntas ORDER BY RANDOM() LIMIT {num_preguntas};')
    preguntas = []
    for row in cursor.fetchall():
        pregunta = {
            'id': row[0],
            'pregunta': row[1],
            'opcion_a': row[2],
            'opcion_b': row[3],
            'opcion_c': row[4],
            'opcion_d': row[5],
            'respuesta': row[6]
        }
        preguntas.append(pregunta)
    conn.close()
    return preguntas



