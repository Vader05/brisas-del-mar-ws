from flask import Flask, render_template, jsonify, Response
from flask_cors import CORS
from controller import Controller
from configuration import *
from dbconnection import Connection

app= Flask(__name__)
CORS(app)
PORT= 5000
DEBUG=True

def connect_bd():
    con = Connection(
        DATABASE["DB_HOST"],
        DATABASE["DB_SERVICE"],
        DATABASE["DB_USER"],
        DATABASE["DB_PASSWORD"],
    )
    con.connect()
    return con

con = connect_bd()

@app.errorhandler(404)
def not_found (error):
    return "Not found"

@app.route('/', methods=['GET'])
def index ():
    return '''<ul>
        <li>Endpoint para anuncios de tabla oferta: /api/v1/regiones </li>
        <li>Endpoint para restaurantes que pertenecen a una region: /api/v1/restaurantes_region/<int:region> </li>
        </ul>'''

@app.route('/api/v1/regiones', methods=['GET'])
def api_all():
    controller = Controller()
    response=[]
    regiones= controller.obtener_keyword_search(con)
    i = 1
    for region in regiones:
        anuncio = {
            'id': i,
            'region': region[0],
            'titulo': region[1]
        }
        response.append(anuncio)
        i = i+1
    return jsonify(response)

@app.route('/api/v1/restaurantes_region/<int:region>', methods=['GET'])
def apiGetRestaurantesByRegion(region=None):
    controller = Controller()
    response=[]
    restaurantes= controller.obtener_restaurantes_by_region(con,region)
    for rest in restaurantes:
        anuncio = {
            'id': rest[0],
            'nombre': rest[1],
            'especialidad': rest[2],
            'departamento': rest[3],
            'capital_departamento':rest[4],
            'rango_precio': rest[5],
            'horario_atencion': rest[6],
            'pagina_web': rest[7],
            'direccion': rest[8],
            'platillos': rest[9]
        }
        response.append(anuncio)
    return jsonify(response)

@app.route('/start' ,methods=['GET'])
def webscraping():
    # principal.webscraping_sd()
    return "iniciando webscraping"

if __name__=="__main__":
    app.run(port=PORT, debug=DEBUG)