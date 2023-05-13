import sys
import os
import re
import json
import time
import openai
import shutil
import requests
import threading
from flask import Flask
import sqlite3
#files
import dbGenerator as db

# OPENAI DATA
openai.api_type = "azure"
openai.api_key = "9cae1236e81e43138b8895ead77acb12"
openai.api_base = "https://openaipasionaus.openai.azure.com/"
openai.api_version = "2022-12-01"
ENGINE_MODEL = "textDavinci03Model"

# VARIABLES VUELO
origin_city = ""
destination_city = ""
origin_date = ""
destination_date = ""

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

def create_kahoot_prompt(destinacion_vuelo,tematica, n = 10):
    prompt = f"Devuelveme un JSON vàlido que contenga una lista llamada 'quiz' de {n} objetos con el siguiente formato:\n- 'question': Una pregunta sobre la ciudad de {destinacion_vuelo} y de tematica {tematica}\n- 'a': Una respuesta valida o invalida sobre la pregunta\n- 'b': Otra respuesta valida o invalida sobre la pregunta\n- 'c': Otra respuesta valida o invalida sobre la pregunta\n- 'd': Otra respuesta valida o invalida sobre la pregunta\n- 'respuesta': La letra (a, b, c, d) que contenga la respuesa correcta a 'question'. Solo una puede ser la correcta, las demás serán falsas"
    # prompt = f'dame un conjunto de 10 preguntas de opción múltiple sobre la ciudad de {destinacion_vuelo}. Cada pregunta debe tener una sola respuesta correcta y estar relacionada con {tematica}. Usa la información disponible sobre {destinacion_vuelo} para crear preguntas interesantes y desafiantes para los usuarios, que cada pregunta  se represente de la siguiente estructura en formato json: {{"¿En qué año fue fundada Barcelona?": {{"A": "218 a. C.", "B": "78 d. C.", "C": "100 d. C.", "D": "410 d. C.", "respuesta": "A"}}}} en una misma linea'
    return prompt.replace("\n", "").replace("\t", "").replace("\\", "")

def request():
    pass

def cargarJson(jsonString):
    return json.loads(jsonString)

def setupInfo(ciudad="Barcelona"):
    res = []
    categorias = ['Cultura', 'Lugares Turísticos', 'Historia', 'Gastronomía', 'Arquitectura']
    print("Refrescando Datos de "+ciudad)
    for i in range(len(categorias)):
        print("Preguntas Categoria " + categorias[i])
        prompt = create_kahoot_prompt(ciudad, categorias[i],2)
        ok = True
        while(ok):
            response = execute_response(prompt)
            data = converJSON(response)
            if 'quiz' in data:
                data = data['quiz']
                for _ in data:
                    #print([_['question'],_['a'],_['b'],_['c'],_['d'],_['respuesta']])
                    res.append([_['question'],_['a'],_['b'],_['c'],_['d'],_['respuesta']])
                    ok = False;
            else:
                ok = True;

    for dato in res:
        # procesar cada pregunta
        pregunta_texto = dato[0]
        opciones = [dato[1],dato[2],dato[3],dato[4],dato[5]]
        db.insertKahootQuest(pregunta_texto, opciones)
    print("Datos de "+ciudad+" Refrescados")



app = Flask(__name__)

# Establece la ruta de la raíz de la API
@app.route('/')
def index():
    return 'Bienvenido a la API de mi aplicación!'


@app.route('/setup', methods=['POST'])
def setup():
    global origin_city
    global destination_city
    global origin_date
    global destination_date

    origin_city = request.form.get('ciudad_origen')
    destination_city  = request.form.get('ciudad_destino')
    origin_date = request.form.get('fecha_salida')
    destination_date = request.form.get('fecha_llegada')

    setupInfo(destination_city)
    return 'Status: Working!'

# Ruta para insertar preguntas en la tabla 'preguntas' de la base de datos
@app.route('/preguntas', methods=['POST'])
def insertar_preguntas():
    pregunta = request.json['pregunta']
    opciones = request.json['opciones']
    db.insertKahootQuest(pregunta, opciones)
    return json.dumps({"status": "OK"})

# Ruta para obtener preguntas aleatorias de la tabla 'preguntas' de la base de datos
@app.route('/preguntas', methods=['GET'])
def obtener_preguntas():
    return json.dumps(db.get_random_questions())

if __name__ == '__main__':
    db.GenerateDataBases()
    setupInfo("Barcelona")
    time.sleep(10)
    app.run(host='192.168.137.1', port=80,debug=False)

