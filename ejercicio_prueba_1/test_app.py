from urllib.parse import urlencode

import pytest
from app import app


@pytest.mark.parametrize(
    argnames=['oracion', 'letra', 'repeticiones_esperadas'],
    argvalues=[
        ('holaaa', 'a', 3),
        ('chauuu', 'u', 3),
        ('Rufus', 'r', 0),
    ],
)
def test_que_cuenta_bien_las_repeticiones(oracion, letra, repeticiones_esperadas):
    with app.test_client() as client:
        querystring = urlencode({'oracion': oracion, 'letra': letra})
        resp = client.get(f'/contar?{querystring}')

    assert resp.status_code == 200
    assert resp.json == {
        'oracion': oracion,
        'letra': letra,
        'repeticiones': repeticiones_esperadas,
    }


def test_que_falta_parametro_letra():  # parametrize
    with app.test_client() as client:
        resp = client.get('/contar?oracion=holaaa')

    assert resp.status_code == 400
    assert resp.json == {
        'error': 'La letra no fue ingresada'
    }


def test_que_falta_parametro_oracion():
    with app.test_client() as client:
        resp = client.get('/contar?letra=X')

    assert resp.status_code == 400
    assert resp.json == {
        'error': 'La oración no fue ingresada'
    }


def test_con_simbolos_raros():
    pass


def test_con_parametro_letra_que_no_es_letra():
    with app.test_client() as client:
        resp = client.get('/contar?oracion=holaaa&letra=1')

    assert resp.status_code == 400
    assert resp.json == {
        'error': 'El parámetro letra no es una letra'
    }


def test_encuentra_personaje_solicitado():
    with app.test_client() as client:
        resp = client.get("/disney?nombre=.GIFfany")

    assert resp.status_code == 200
    assert resp.json == {
        "enemies": [],
        "films": [],
        "nombre": ".GIFfany",
        "tvShows": ["Gravity Falls"],
    }


def test_no_envio_nombre_personaje():
    with app.test_client() as client:
        resp = client.get("/disney")
    assert resp.status_code == 400
    assert resp.json == {
        "error": "No se envio el nombre del personaje"
    }

def test_personaje_no_existe_en_base_de_datos():
    with app.test_client() as client:
        resp = client.get("/disney?nombre=Rufus")
    assert resp.status_code == 400
    assert resp.json == {
        "error": "El personaje solicitado no se encuentra en la base de datos"
    }