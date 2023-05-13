import sys
import os
import re
import json
import time
import openai
import sqlite3
import shutil
import requests
import threading

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
    cursor.execute('''INSERT INTO preguntas (question, opcion_a, opcion_b, opcion_c, opcion_d, respuesta) VALUES (?, ?, ?, ?, ?, ?)''', (pregunta, opciones['A'], opciones['B'], opciones['C'], opciones['D'], opciones['respuesta']))
    conn.commit()
    conn.close()

def insertAirportsData():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "INSERT INTO airports (code, lat, lon, name, city, state, country, woeid, tz, phone, type, email, url, runway_length, elev, icao, direct_flights, carriers) VALUES ('AAA', '-17.3595', '-145.494', 'Anaa Airport', 'Anaa', 'Tuamotu-Gambier', 'French Polynesia', '12512819', 'Pacific/Midway', '', 'Airports', '', '', '4921', '7', 'NTGA', '2', '1');"
    cursor.execute(sql)
    conn.commit()
    conn.close()




#files
import dbGenerator as db

openai.api_type = "azure"
openai.api_key = "9cae1236e81e43138b8895ead77acb12"
openai.api_base = "https://openaipasionaus.openai.azure.com/"
openai.api_version = "2022-12-01"
ENGINE_MODEL = "textDavinci03Model"

def OpenAiReConfig(API_TYPE_NEW,API_KEY_NEW,API_BASE_NEW,API_VERSION_NEW,ENGINE_MODEL_NEW):
    global openai
    global ENGINE_MODEL
    openai.API_TYPE = API_TYPE_NEW
    openai.api_key = API_KEY_NEW
    openai.API_BASE = API_BASE_NEW
    openai.API_VERSION = API_VERSION_NEW
    ENGINE_MODEL = ENGINE_MODEL_NEW


def execute_response(pompt, engine = ENGINE_MODEL, max_tokens = 1024, temperature = 0.7):
    return openai.Completion.create(
        engine = engine,
        prompt = pompt,
        max_tokens = max_tokens,
        temperature = temperature
    )


def create_kahoot_prompt(destinacion_vuelo,tematica):
    prompt = f'dame un conjunto de 10 preguntas de opción múltiple sobre la ciudad de {destinacion_vuelo}. Cada pregunta debe tener una sola respuesta correcta y estar relacionada con {tematica}. Usa la información disponible sobre {destinacion_vuelo} para crear preguntas interesantes y desafiantes para los usuarios, que cada pregunta  se represente de la siguiente estructura en formato json: {{"¿En qué año fue fundada Barcelona?": {{"A": "218 a. C.", "B": "78 d. C.", "C": "100 d. C.", "D": "410 d. C.", "respuesta": "A"}}}} en una misma linea'
    return prompt.replace("\n", "").replace("\t", "").replace("\\", "")


def request():
    pass

def cargarJson(jsonString):
    return json.loads(jsonString)

def main():
    res = []
    categorias = ['Cultura', 'Lugares Turísticos', 'Historia', 'Gastronomía', 'Arquitectura']
    while(len(res)<10):
        for i in range(len(categorias)):
            print("Preguntas Categoria " + categorias[i])
            prompt = create_kahoot_prompt("Barcelona", categorias[i])
            response = execute_response(prompt)['choices'][0]['text']
            #print(response)
            

            preguntas_dict_list = response.replace("}, {", "}|{").replace("[{", "").replace("}]", "").split("|")
            try:
                for question_options in preguntas_dict_list:
                    pregunta = json.loads(question_options)
                    res.append(pregunta)
            except ValueError as e:
                pass

            
        #print(res)
        for pregunta in res:
            try:
                pregunta_texto = pregunta['question']
                opciones = pregunta['options']
                db.insertKahootQuest(pregunta_texto, opciones)
            except KeyError as e:
                #print("La pregunta no tiene el formato correcto.")
                print(e)
                pass



if __name__ == "__main__":
    db.GenerateDataBases()
    main()
