<!-- # Vueling_Entretainment_BACKEND -->
# **Vueling** : Entretainment **[BACKEND]**_
Este es un proyecto de simulación de una aerolínea ficticia llamada Kahoot! Airlines. El objetivo es proporcionar un programa de línea de comandos (CLI) que permita a los usuarios interactuar con diferentes características de la aerolínea, como reservar vuelos, ver la información del aeropuerto, jugar juegos de preguntas de Kahoot, ver el estado del tiempo, entre otras cosas.

## **Instalación**
Para ejecutar el programa, se deben seguir los siguientes pasos:

## **Clonar este repositorio en su máquina local.**
Instalar los paquetes requeridos para el proyecto. Esto se puede hacer ejecutando el siguiente comando en la terminal:
```css
pip install -r requirements.txt
```

Ejecutar el archivo principal main.py con Python 3.
```css
python main.py
```

## **Características**
Las características principales del programa son las siguientes:

### **Reservar vuelos**
Los usuarios pueden buscar y reservar vuelos de Kahoot! Airlines. Se pueden buscar vuelos por origen, destino y fecha. Si hay asientos disponibles en el vuelo seleccionado, se reservará el asiento y se generará un número de confirmación.

### **Ver información de aeropuertos**
Los usuarios pueden buscar información de aeropuertos, como su ubicación, código de aeropuerto, estado y país. La información se obtiene de una base de datos interna del programa que contiene información sobre varios aeropuertos.

### **Jugar juegos de preguntas de Kahoot**
Los usuarios pueden jugar juegos de preguntas de Kahoot desde la línea de comandos. Los juegos se obtienen de una base de datos interna del programa que contiene preguntas y respuestas. Los usuarios pueden seleccionar el juego que deseen y responder las preguntas.

### **Ver estado del tiempo**
Los usuarios pueden ver el estado del tiempo actual de una ciudad especificada. La información del tiempo se obtiene de la API de WeatherAPI y se muestra en la terminal.

### **Ver y agregar incidencias**
Los usuarios pueden ver una lista de las incidencias activas en los vuelos y agregar nuevas incidencias. Las incidencias pueden incluir comentarios sobre el problema y se pueden marcar como resueltas más tarde.

### **Ver y actualizar tabla de líderes**
Los usuarios pueden ver una tabla de líderes que muestra los nombres y las puntuaciones de los usuarios que han reservado vuelos en Kahoot! Airlines. Los usuarios también pueden actualizar su puntuación si han reservado un vuelo más recientemente.

### **Iniciar sesión y crear cuenta de usuario**
Los usuarios pueden crear una cuenta y iniciar sesión en el programa. Los datos del usuario se almacenan en una base de datos interna del programa y se utilizan para identificar al usuario al reservar vuelos o ver la tabla de líderes.

## **Contribuyendo**
Si desea contribuir al proyecto, puede hacerlo mediante la apertura de un PR (pull request) o una Issue en el repositorio. Cualquier contribución es bienvenida.

## **Licencia**
Este proyecto está bajo la Licencia MIT. Puedes leer la licencia completa en el archivo LICENSE.
