from flask import Flask, jsonify, request, render_template
from flask import request
# from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

import mysql.connector
from mysql.connector import errorcode, Error

# esto es para subir archivos de tipo foto al servidor
from werkzeug.utils import secure_filename

import os
import time

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas de la aplicación.

#--------------------------------------------------------------
class Catalogo:
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos. Si no existe, la creamos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            #si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
    
    #una vez que la bd esta establecida,creamos la tabla si no existe
    #MARCA, MODELO, TIPO, ANIO, PRECIO, MOTOR, FOTO, DESCRIPCION,PROVEEDOR,FECHA,PUERTAS, COLOR
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS autos(
        id INT AUTO_INCREMENT PRIMARY KEY,
        marca VARCHAR(100),
        modelo VARCHAR(100),
        tipo VARCHAR(100),
        anio INT,
        precio FLOAT,
        motor VARCHAR(100),
        foto VARCHAR(100),
        descripcion TEXT,
        proveedor VARCHAR(100),
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        puertas INT,
        color VARCHAR(100)
    )''')
        self.conn.commit()

    # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    #--------------------------------------------------------------
    def agregar_autos(self, marca, modelo, tipo, anio, precio, motor, foto, descripcion, proveedor, puertas, color):
        sql = "INSERT INTO autos(marca, modelo, tipo, anio, precio, motor, foto, descripcion, proveedor, puertas, color) VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (marca, modelo, tipo, anio, precio, motor, foto, descripcion, proveedor, puertas, color)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid
    
    #--------------------------------------------------------------
    def consultar_autos(self, id):
        self.cursor.execute(f"SELECT * FROM autos WHERE id=%s", (id,)) 
        # Consultamos un producto a partir de su código
        autos = self.cursor.fetchone()
        return autos
    #en el codigo orgina el profe poneself.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
    #return self.cursor.fetchone()

    #--------------------------------------------------------------
    def modificar_autos (self, id, marca, modelo, tipo, anio, precio, motor, foto, descripcion, proveedor, puertas, color):
        sql = "UPDATE autos SET marca=%s, modelo=%s, tipo=%s, anio=%s, precio=%s, motor=%s, foto=%s, descripcion=%s, proveedor=%s, puertas=%s, color=%s WHERE id=%s"
        valores = (nuevo_marca, nuevo_modelo, nuevo_tipo, nuevo_anio, nuevo_precio, nuevo_motor, nuevo_foto, nuevo_descripcion, nuevo_proveedor, nuevo_puertas, nuevo_color, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount>0
    
    #----------------------------------------------------------------
    def listar_autos(self):
        self.cursor.execute("SELECT * FROM autos")
        autos = self.cursor.fetchall()
        return autos

    #--------------------------------------------------------------
    def eliminar_autos(self, id):
        #eliminamos un producto a partir de su código
        self.cursor.execute(f"DELETE FROM autos WHERE id=%s", (id,))
        self.conn.commit()
        return self.cursor.rowcount>0
    
    #--------------------------------------------------------------
    def mostrar_autos(self, id):
        #mostramos un producto a partir de su código
        autos = self.consultar_auto(id)
        if autos:
            print("-"*40)
            print(f"ID: {autos['id']}")
            print(f"Marca: {autos['marca']}")
            print(f"Modelo: {autos['modelo']}")
            print(f"Tipo: {autos['tipo']}")
            print(f"Año: {autos['anio']}")
            print(f"Precio: {autos['precio']}")
            print(f"Motor: {autos['motor']}")
            print(f"Foto: {autos['foto']}")
            print(f"Descripcion: {autos['descripcion']}")
            print(f"Proveedor: {autos['proveedor']}")
            print(f"Fecha: {autos['fecha']}")
            print(f"Puertas: {autos['puertas']}")
            print(f"Color: {autos['color']}")
            print("-"*40)
        else:
            print("El auto no existe")
    
#--------------------------------------------------------------

#Cuerpo del programa
catalogo = Catalogo(host="localhost", user="root", password="", database="autos")

#carpeta para guardar las fotos
RUTA='static/img/'
#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA = '/home/USUARIO/mysite/static/imagenes'

#--------------------------------------------------------------

#Listar todos los productos

# La ruta Flask /productos con el método HTTP GET está diseñada para proporcionar los detalles de todos los productos almacenados en la base de datos.
# El método devuelve una lista con todos los productos en formato JSON.

@app.route('/autos', methods=['GET'])
def listar_autos():
    autos = catalogo.listar_autos()
    return jsonify(autos)

#--------------------------------------------------------------
#Mostrar un solo auto segun su id

#La ruta Flask /productos/<int:id> con el método HTTP GET está diseñada para proporcionar los detalles de un producto específico basado en su código.
#El método busca en la base de datos el producto con el código especificado y devuelve un JSON con los detalles del producto si lo encuentra, o None si no lo encuentra.
@app.route('/autos/<int:id>', methods=['GET'])
def mostrar_autos(id):
    autos = catalogo.consultar_auto(id)
    if autos:
        return jsonify(autos), 201
    else:
        return jsonify({"mensaje": "El auto no existe"}), 404

#--------------------------------------------------------------
#Agregar un auto
@app.route('/autos', methods=['POST'])
def agregar_autos():
    #obtenemos los datos del formulario
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    tipo = request.form.get('tipo')
    anio = request.form.get('anio')
    precio = request.form.get('precio')
    motor = request.form.get('motor')
    descripcion = request.form.get('descripcion')
    proveedor = request.form.get('proveedor')
    puertas = request.form.get('puertas')
    color = request.form.get('color')
    foto = request.files['foto']
    nombre_foto = ''

    #guardamos el nombre de la imagen

    #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_foto = secure_filename(foto.filename) 
    #Separa el nombre del archivo de su extensión.
    nombre_base, extension = os.path.splitext(nombre_foto) 
    #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
    nombre_foto= f"{nombre_base}_{int(time.time())}{extension}"

    nuevo_id = catalogo.agregar_autos(marca, modelo, tipo, anio, precio, motor, nombre_foto, descripcion, proveedor, puertas, color)
    if nuevo_id:
        foto.save(os.path.join(RUTA, nombre_foto))

        #si el produco se agreaga con exito, se devuelve un json con el mensaje "Producto agregado correctamente" y el código del producto
        return jsonify({"mensaje": "Auto agregado correctamente", "id": nuevo_id, "foto": nombre_foto}), 201
    else:
        #si no se agrega el producto, se devuelve un json con el mensaje "Error al agregar el auto" y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el auto"}), 500
    
#--------------------------------------------------------------
#Modificar un auto segun su id
@app.route('/autos/<int:id>', methods=['PUT'])
#La ruta Flask /productos/<int:id> con el método HTTP PUT está diseñada para actualizar la información de un producto existente en la base de datos, identificado por su código.
#La función modificar_producto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /productos/ seguido de un número (el código del producto).
#La función recibe el código del producto como parámetro y los nuevos datos del producto en el cuerpo de la solicitud.
#La función busca el producto en la base de datos y, si lo encuentra, actualiza los datos del producto con los nuevos datos proporcionados.
#Si el producto se actualiza correctamente, la función devuelve un JSON con el mensaje "Producto modificado correctamente" y un código de estado HTTP 200 (OK).
#Si el producto no se encuentra, la función devuelve un JSON con el mensaje "El producto no existe" y un código de estado HTTP 404 (Not Found).
#Si ocurre un error al intentar actualizar el producto, la función devuelve un JSON con el mensaje "Error al modificar el producto" y un código de estado HTTP 500 (Internal Server Error).
def modificar_autos(id):
    #obtenemos los datos del formulario
    nuevo_marca = request.form.get('marca')
    nuevo_modelo = request.form.get('modelo')
    nuevo_tipo = request.form.get('tipo')
    nuevo_anio = request.form.get('anio')
    nuevo_precio = request.form.get('precio')
    nuevo_motor = request.form.get('motor')
    nuevo_descripcion = request.form.get('descripcion')
    nuevo_proveedor = request.form.get('proveedor')
    nuevo_puertas = request.form.get('puertas')
    nuevo_color = request.form.get('color')

    #verifica si se proporiciono una nueva imagen
    if 'foto' in request.files:
        foto = request.files['foto']
        
        #procesamiento de la foto
        nombre_foto = secure_filename(foto.filename)
        nombre_base, extension = os.path.splitext(nombre_foto)
        nombre_foto = f"{nombre_base}_{int(time.time())}{extension}"

        #guardamos la imagen
        foto.save(os.path.join(RUTA, nombre_foto))

        #busco el auto guardado
        autos = catalogo.consultar_auto(id)
        if autos: #si existe el auto
            foto_anterior = autos['foto']
            #ruta de la foto anterior
            ruta_foto = os.path.join(RUTA, foto_anterior)
            #si existe, elimino la foto anterior
            if os.path.exists(ruta_foto):
                os.remove(ruta_foto)
        else:
            #si no se proporciona una nueva imagen, se mantiene la imagen anterior
            autos = catalogo.consultar_auto(id)
            if autos:
                nombre_foto = autos['foto']

        if catalogo.modificar_autos(id, nuevo_marca, nuevo_modelo, nuevo_tipo, nuevo_anio, nuevo_precio, nuevo_motor, nombre_foto, nuevo_descripcion, nuevo_proveedor, nuevo_puertas, nuevo_color):
            return jsonify({"mensaje": "Auto modificado correctamente"}), 200
        else:
            return jsonify({"mensaje": "Error al modificar el auto"}), 403
    
#--------------------------------------------------------------
#Eliminar un auto segun su id
@app.route('/autos/<int:id>', methods=['DELETE'])
#La ruta Flask /productos/<int:id> con el método HTTP DELETE está diseñada para eliminar un producto existente en la base de datos, identificado por su código.
#La función eliminar_producto se asocia con esta URL y es invocada cuando se realiza una solicitud DELETE a /productos/ seguido de un número (el código del producto).
#La función recibe el código del producto como parámetro y busca el producto en la base de datos.
#Si el producto se encuentra, la función lo elimina y devuelve un JSON con el mensaje "Producto eliminado correctamente" y un código de estado HTTP 200 (OK).
#Si el producto no se encuentra, la función devuelve un JSON con el mensaje "El producto no existe" y un código de estado HTTP 404 (Not Found).
#Si ocurre un error al intentar eliminar el producto, la función devuelve un JSON con el mensaje "Error al eliminar el producto" y un código de estado HTTP 500 (Internal Server Error).
def eliminar_autos(id):
    #buscamos el auto
    autos = catalogo.consultar_autos(id)
    if autos: #si existe, verifica si hay una foto asociada en el servidor
        foto_anterior = autos['foto']
        #ruta de la foto
        ruta_foto = os.path.join(RUTA, foto_anterior)
        #si existe, elimino la foto del servidor
        if os.path.exists(ruta_foto):
            os.remove(ruta_foto)
        #luego, elimina el auto de la base de datos
        if catalogo.eliminar_autos(id):
            return jsonify({"mensaje": "Auto eliminado correctamente"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el auto"}), 500
    else:
        return jsonify({"mensaje": "El auto no existe"}), 404

#--------------------------------------------------------------
#--------------------------------------------------------------------
#esto se coloca al final sino la app no se ejecuta
if __name__ == '__main__':
    app.run(debug=True)