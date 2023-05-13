import json
import sys
import os
import re
import json
import time
import openai
import shutil
import requests
import threading

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
    prompt = f"Genera un conjunto de 10 preguntas de opción múltiple sobre la ciudad de {destinacion_vuelo}. Cada pregunta debe tener una sola respuesta correcta y estar relacionada con {tematica}. Usa la información disponible sobre {destinacion_vuelo} para crear preguntas interesantes y desafiantes para los usuarios. en JSON en OneLine."
    return prompt


def request():
    pass

def cargarJson(jsonString):
    return json.loads(jsonString)

def main():
    res = []
    categorias = ['Cultura', 'Lugares Turísticos', 'Historia', 'Gastronomía', 'Arquitectura']
    for i in range(len(categorias)):
        print("Preguntas Categoria " + categorias[i])
        prompt = create_kahoot_prompt("Barcelona", categorias[i])
        json_string = str(execute_response(prompt)['choices'][0]['text'])
        # Leer el JSON con las preguntas y respuestas
        json_string = '''
            {
                "1.¿En qué año fue inaugurada La Sagrada Família?":["A) 1882","B) 1883","C) 1884","D) 1885"],
                "2.¿Cuál de los siguientes no es uno de los edificios más representativos de Barcelona?":["A) El Palacio de la Música","B) Las Arenas","C) El Palacio Real","D) La Torre Agbar"],
                "3.¿Cuál es la estatua más famosa de Barcelona?":["A) La estatua de Colón","B) La estatua de Gaudí","C) La estatua de Los Tres Porques","D) La estatua de Els Quatre Gats"],
                "4.¿En qué año se creó La Rambla?":["A) 1602","B) 1702","C) 1802","D) 1902"],
                "5.¿Cuál es el museo más importante de Barcelona?":["A) El Museo Picasso","B) El Museo de Arte Contemporáneo","C) El Museo Nacional de Arte de Catalunya","D) El Museo de Historia Natural"],
                "6.¿Cuál de los siguientes no es uno de los edificios modernistas más famosos?":["A) La Casa Batlló","B) La Casa Milà","C) La Catedral de Barcelona","D) La Casa Amatller"],
                "7.¿Cuál de los siguientes no fue un antiguo teatro?":["A) El Teatro Real","B) El Teatro de La Rambla","C) El Teatro Coliseum","D) El Teatro Nacional de Catalunya"],
                "8.¿Cuál es el festival más importante de Barcelona?":["A) La Feria de Abril","B) El Festival Internacional de Teatro","C) El Festival Internacional de Jazz","D) El Festival de Música de Barcelona"],
                "9.¿Cuál de los siguientes no es uno de los grandes parques de Barcelona?":["A) El Parque de La Ciutadella","B) El Parque Güell","C) El Parque de La Ciudadela","D) El Parque del Palau Reial"],
                "10.¿Cuál es el edificio más alto de Barcelona?":["A) Torre Agbar","B) Torre Mapfre","C) Torre de Collserola","D) Torre de Bellesguard"]
            }
        '''
        preguntas_dict = json.loads(json_string)

        # Iterar sobre las preguntas y mostrarlas
        for pregunta, respuestas in preguntas_dict.items():
            print(pregunta)
            for respuesta in respuestas:
                print(respuesta)
            print()  # imprimir línea en blanco para separar las preguntas


if __name__ == "__main__":
    db.GenerateDataBases()
    main()