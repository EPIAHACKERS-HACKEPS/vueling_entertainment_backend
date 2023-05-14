import sys
import os
import re
import json
import time
import openai
import shutil
import sqlite3
import requests
import threading
import dbGenerator as db
from flask import Flask, request as rr , jsonify, abort

APIS_INTRANET = ['2d7e2caa-20f8-45db-b318-3b7aedc3c27a','c42a6bd1-5cab-40a1-9977-931f18bf7bc6','659fd5a8-7692-443a-8cfd-08336128ca53']
# OPENAI DATA
openai.api_type = "azure"
openai.api_key = "YOUR_API_KEY_HERE"
openai.api_base = "https://openaipasionaus.openai.azure.com/"
openai.api_version = "2022-12-01"
ENGINE_MODEL = "textDavinci03Model"

# FLIGHT VARIABLES
origin_city = ""
destination_city = ""
origin_date = ""
destination_date = ""

def getIntranet():
    return """<!DOCTYPE html><html><head><title>Vueling Entertainment Management Intranet</title><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/public/css/style.css"></head><body><header><img src="/public/logo.svg" alt="Logo"></header><center><form action="/setup" method="post" style="padding: 15pt;width:30vw;border-radius:15pt;background:var(--clr-charcoal);margin-bottom: 12pt;"><label for="city_origen">Origin city:</label><input type="text" name="city_origen" placeholder="Origin city" value="New York" style="border: 1pt solid var(--clr-yellow);background:var(--clr-charcoal);color:var(--clr-off-white);"/><br><label for="city_destino">Destination city:</label><input type="text" name="city_destino" placeholder="Destination city" value="Los Angeles" style="border: 1pt solid var(--clr-yellow);background:var(--clr-charcoal);color:var(--clr-off-white);"/><br><label for="fecha_origen">Departure date and time:</label><input type="datetime-local" name="fecha_salida" placeholder="Departure date and time" value="2023-06-01T08:00" style="border: 1pt solid var(--clr-yellow);background:var(--clr-charcoal);color:var(--clr-off-white);"/><br><label for="fecha_llegada">Arrival date and time:</label><input type="datetime-local" name="fecha_llegada" placeholder="Arrival date and time" value="2023-06-01T12:00" min="2023-06-01T08:00" style="border: 1pt solid var(--clr-yellow);background:var(--clr-charcoal);color:var(--clr-off-white);"/><br><input type="submit"/></form></center><footer><p>&copy; 2023 Vueling Entretainment By <a href="https://github.com/EPIAHACKERS-HACKEPS" style="text-decoration:none;color:var(--clr-yellow);"/>EpiaHackers</p>. All rights reserved.</p></footer><script src="/public/js/script.js"></script></body></html>"""
# Define the decorator
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

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
    )['choices'][0]['text'].strip().replace("\n", "").replace("\t", "")


def converJSON(json_text):
    start = json_text.find("{")
    end = json_text.rfind("}")

    if start != -1 and end != -1:
        json_text = json_text[start:end+1]
        try:
            return json.loads(json_text)
        except:
            return {}
    return {}

def create_kahoot_prompt(flight_destination,topic, n = 10):
    # INGLÉS
    prompt = f"Return me a valid JSON containing a list called 'quiz' of {n} objects with the following format:\n- 'question': A question about the city of {flight_destination} and subject {topic}: A valid or invalid answer about the question 'b': Another valid or invalid answer on the question 'c': Another valid or invalid answer on the question 'd': Another valid or invalid answer on the question 'answer': The letter (a, b, c, d) that contains the correct answer to 'question'. Only one can be correct, the others will be false."
    # ESPAÑOL
    #prompt = f"Devuelveme un JSON vàlido que contenga una lista llamada 'quiz' de {n} objetos con el siguiente formato:\n- 'question': Una pregunta sobre la city de {destinacion_vuelo} y de tematica {tematica}\n- 'a': Una respuesta valida o invalida sobre la pregunta\n- 'b': Otra respuesta valida o invalida sobre la pregunta\n- 'c': Otra respuesta valida o invalida sobre la pregunta\n- 'd': Otra respuesta valida o invalida sobre la pregunta\n- 'respuesta': La letra (a, b, c, d) que contenga la respuesa correcta a 'question'. Solo una puede ser la correcta, las demás serán falsas"
    # prompt = f'dame un conjunto de 10 preguntas de opción múltiple sobre la city de {destinacion_vuelo}. Cada pregunta debe tener una sola respuesta correcta y estar relacionada con {tematica}. Usa la información disponible sobre {destinacion_vuelo} para crear preguntas interesantes y desafiantes para los usuarios, que cada pregunta  se represente de la siguiente estructura en formato json: {{"¿En qué año fue fundada Barcelona?": {{"A": "218 a. C.", "B": "78 d. C.", "C": "100 d. C.", "D": "410 d. C.", "respuesta": "A"}}}} en una misma linea'
    return prompt.replace("\n", "").replace("\t", "").replace("\\", "")

def request():
    pass

def cargarJson(jsonString):
    return json.loads(jsonString)

def setupInfo(city="Barcelona"):
    res = []
    categories = ['Culture', 'Tourist Sites', 'History', 'Gastronomy', 'Architecture']
    #categories = ['Cultura', 'Lugares Turísticos', 'Historia', 'Gastronomía', 'Arquitectura']
    print("Extracting data from "+city)
    for i in range(len(categories)):
        print("Generating questions from " + categories[i]+" from "+city)
        prompt = create_kahoot_prompt(city, categories[i],2)
        ok = True
        while(ok):
            response = execute_response(prompt)
            data = converJSON(response)
            if 'quiz' in data:
                data = data['quiz']
                #print(data)
                for _ in data:
                    #print([_['question'],_['a'],_['b'],_['c'],_['d'],_['respuesta']])
                    res.append([_['question'],_['a'],_['b'],_['c'],_['d'],_['answer']])
                    ok = False;
            else:
                ok = True;

    for dato in res:
        # process each question
        question_text = dato[0]
        options = [dato[1],dato[2],dato[3],dato[4],dato[5]]
        db.insertKahootQuest(question_text, options)
    print("Data from "+city+" imported")


app = Flask(__name__,static_folder='public')
app.config['API_KEYS'] = APIS_INTRANET


    
# Aplica el decorador a todas las respuestas de la aplicación
@app.after_request
def after_request(response):
    return add_cors_headers(response)


# @app.before_request
# def protect_url():
#     if rr.path == '/':
#         return check_api_key()
    

# Establece la ruta de la raíz de la API
@app.route('/')
def index():
    api_key = rr.args.get('api_key')
    if api_key not in app.config['API_KEYS']:
        response = jsonify({'error': 'Clave API inválida'})
        response.status_code = 401
        abort(403)
        return response
    else: 
        return getIntranet()



@app.route('/setup', methods=['POST'])
def setup():
    global origin_city
    global destination_city
    global origin_date
    global destination_date
    #print(rr.headers)
    #api_key = rr.headers.get('apikey')
    #if api_key == 'kajsdfhlkaeshfdjkhsdjkahskl':
    origin_city = rr.form.get('city_origen')
    destination_city  = rr.form.get('city_destino')
    origin_date = rr.form.get('fecha_salida')
    destination_date = rr.form.get('fecha_llegada')
    
    setupInfo(destination_city)
    return 'Status: Working!'

# Ruta para insertar preguntas en la tabla 'preguntas' de la base de datos
# @app.route('/questions', methods=['POST'])
# def insertar_preguntas():
#     pregunta = rr.form.get('pregunta')
#     opciones = rr.form.get('opciones')
#     db.insertKahootQuest(pregunta, opciones)
#     return json.dumps({"status": "OK"})

@app.route('/info', methods=['GET'])
def generalInfo():
    weather = db.get_current_weather(destination_city)
    data = [origin_city,destination_city,origin_date,destination_date,weather['temperature_c'],weather['condition'],weather['icon']]
    keys = ["origin_city", "destination_city", "origin_date", "destination_date","temperature","condition","icon"]
    result = {}
    for i in range(len(data)):
        result[keys[i]] = data[i]
    return json.dumps(result)

# Ruta para insertar preguntas en la tabla 'preguntas' de la base de datos
@app.route('/leadborard', methods=['POST'])
def insert_leaderboard():
    seat = rr.form.get('seat')
    #points = rr.form.get('points')
    username = rr.form.get('username')
    questions = rr.form.get('questions')
    questions = json.loads(questions)
    points = 0
    for question in questions:
        if question['answer'] == question['correctAnswer']:
            points += 1
    
    try:
        db.insertLeaderboardData(username,seat,points)
        return json.dumps({"status": "200"})
    except:
        return json.dumps({"status": "400"})


# Ruta para insertar preguntas en la tabla 'preguntas' de la base de datos
@app.route('/leadborard', methods=['GET'])
def get_leaderborard():
    results = db.getLeaderboard()
    # Creamos un diccionario con las claves correspondientes
    keys = ["id", "nickname", "seat", "points"]
    # Convertimos cada lista en un diccionario
    result_dicts = []
    for r in results:
        result_dict = {keys[i]: r[i] for i in range(len(keys))}
        result_dicts.append(result_dict)
    # Convertimos la lista de diccionarios en una lista de objetos JSON
    return json.dumps(result_dicts)

# Ruta para obtener preguntas aleatorias de la tabla 'preguntas' de la base de datos
@app.route('/questions', methods=['GET'])
def obtener_preguntas():
    return json.dumps(db.get_random_questions())


@app.route('/places', methods=['GET'])
def getPlaces():
    results = db.getPlaces()
    # Creamos un diccionario con las claves correspondientes
    keys = ["id", "place", "username", "assitants"]
    # Convertimos cada lista en un diccionario
    result_dicts = []
    for r in results:
        result_dict = {keys[i]: r[i] for i in range(len(keys))}
        result_dicts.append(result_dict)
    # Convertimos la lista de diccionarios en una lista de objetos JSON
    return json.dumps(result_dicts)

# Ruta para insertar preguntas en la tabla 'preguntas' de la base de datos
@app.route('/places', methods=['POST'])
def postPlaces():
    place = rr.form.get('place')
    username = rr.form.get('username')
    try:
         db.updatePlaces(place,username)
         return json.dumps({"status": "200"})
    except:
         return json.dumps({"status": "400"})


@app.route('/genPlace', methods=['POST'])
def genPlace():
    place = rr.form.get('place')
    username = rr.form.get('username')
    try:
         db.insertPlaces(place,username)
         return json.dumps({"status": "200"})
    except:
         return json.dumps({"status": "400"})



@app.route('/assist', methods=['GET'])
def getAssist():
    results = db.getPlaces()
    # Creamos un diccionario con las claves correspondientes
    keys = ["id", "place", "username", "assitants"]
    # Convertimos cada lista en un diccionario
    result_dicts = []
    for r in results:
        result_dict = {keys[i]: r[i] for i in range(len(keys))}
        result_dicts.append(result_dict)
    # Convertimos la lista de diccionarios en una lista de objetos JSON
    return json.dumps(result_dicts)


# Ruta para insertar preguntas en la tabla 'preguntas' de la base de datos
@app.route('/assist', methods=['POST'])
def asist():
    place = rr.form.get('place')
    username = rr.form.get('username')
    try:
         db.updatePlaces(place,username)
         return json.dumps({"status": "200"})
    except:
         return json.dumps({"status": "400"})



if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 80

    ruta_archivo = os.getcwd()+db.database
    
    if not os.path.exists(ruta_archivo):
        # Generar Base de Datos
        db.GenerateDataBases()
        print("DATABASE GENERATED as "+db.database)
        # Generar Usuario Admin con Contraseña: !$Admin1234$!
        #db.insertUserData('admin','!$Admin1234$!')
        #print("GENERATED [USERNAME = admin] with [PASSWORD = !$Admin1234$!]")
        # MOSTRAR LAS API KEYS DE INTRANET
        print('API KEYS DE INTRANET')
        print(APIS_INTRANET)
        
    app.run(host=ip, port=port,debug=False)

