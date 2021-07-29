import json

from flask import Flask, request, make_response
import requests

app = Flask(__name__)


def error(error_dict, status=400):
    return make_response(error_dict, status)


@app.route('/contar')
def contar():
    """Se usa: /contar?oracion=hola&letra=b   (querystring)"""
    oracion = request.args.get('oracion')
    letra = request.args.get('letra')
    if oracion is None:
        return error({'error': 'La oración no fue ingresada'})
    if letra is None:
        return error({'error': 'La letra no fue ingresada'})
    if not letra.isalpha():
        return error({'error': 'El parámetro letra no es una letra'})

    repeticiones = oracion.count(letra)
    return {
        'letra': letra,
        'oracion': oracion,
        'repeticiones': repeticiones
    }
@app.route('/disney')
def personajes_disney():
    URL = "https://api.disneyapi.dev/characters"
    r = requests.get(url=URL)
    nombre_personaje = request.args.get('nombre')
    if nombre_personaje is None:
        return error({"error": "No se envio el nombre del personaje"})
    data = json.loads(r.text)
    for element in data["data"]:
        if element["name"] == nombre_personaje:
            return {
                "nombre": element["name"],
                "enemies": element["enemies"],
                "films": element["films"],
            }
    return error({"error": "El personaje solicitado no se encuentra en la base de datos"})

if __name__ == '__main__':
    app.run()
