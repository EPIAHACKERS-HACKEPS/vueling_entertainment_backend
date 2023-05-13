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
