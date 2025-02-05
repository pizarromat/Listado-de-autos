# Creada por Pizarro Matias

# Importamos flask, y los modulo "render_template", "request", "redirect", "url_for"  que pertenece al mismo
from flask import Flask, render_template, request, redirect, url_for

# Importamos el modulo "os" para acceder facilmente a los directorios
import os

# Importamos la base de datos como "db"
import database as db

# accedemos al archivo /index.html
# Entramos en la carpeta "templates_dir", siendo "dir" una variable
templates_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# Declaramos una variable y la inicializamos con "Flask"
# Indicamos con "__name__" para iniciar la aplicacion
app = Flask(__name__)

# Rutas de la aplicación --------------------------------------


# Ruta principal -----
@app.route("/")
# Vinculamos una funcion a la ruta principal
def home():
    # Accedemos a la base de datos con el cursor
    cursor = db.database.cursor()
    # Tipo de consulta executo (ejecuta)
    cursor.execute("SELECT * FROM autos")
    # Creamos una variable "myresult" y accedemos mediante el cursor a la funcion "fetchall()"
    myresult = cursor.fetchall()
    # Convertimos los datos de tupla "()" a diccionario "[]"
    insertObject = []
    # Obtenemos los nombres de las columnas
    columnNames = [column[0] for column in cursor.description]
    # Mediante un bucle voy a acceder a los registros que estan dentro de "myresult"
    for record in myresult:
        # Va a agregar los datos al diccionario con la funcion "append()"
        # Transformamos los datos a diccionario con "dict()"
        insertObject.append(dict(zip(columnNames, record)))
    # Cerramos el cursor
    cursor.close()
    return render_template("index.html", data=insertObject)


# Ruta para guardar autos -----
@app.route("/user", methods=["POST"])
def addAutos():
    # Obtenemos la información de cada registro
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    año = request.form["año"]
    precio = request.form["precio"]
    color = request.form["color"]
    kilometraje = request.form["kilometraje"]
    descripcion = request.form["descripcion"]

    # Condicion si tenemos todos los campos
    if marca and modelo and año and precio and color and kilometraje and descripcion:
        # consultamos a la base de datos
        cursor = db.database.cursor()
        # hacemos la consulta
        sql = "INSERT INTO autos (marca, modelo, año, precio, color, kilometraje, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # Indicamos una tupla con los datos
        data = (marca, modelo, año, precio, color, kilometraje, descripcion)
        # Le pasamos los datos con la funcion "execute"
        cursor.execute(sql, data)
        # Hacemos el commit a la base de datos sino no funciona
        db.database.commit()
    return redirect(url_for("home"))


# Ruta para borrar autos con "id"
@app.route("/delete/<string:id>")
def delete(id):
    # consultamos a la base de datos
    cursor = db.database.cursor()
    # Eliminamos sabiendo el id
    sql = "DELETE INTO autos WHERE id=%s"
    # Indicamos una tupla con el id
    data = id
    # Le pasamos los datos con la funcion "execute"
    cursor.execute(sql, data)
    # Hacemos el commit a la base de datos. Sino, no funciona
    db.database.commit()
    return redirect(url_for("home"))


# Ruta para actualizar datos con "id"
@app.route("/edit/<string:id>", methods=["POST"])
def edit(id):
    # Obtenemos la información de cada registro
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    año = request.form["año"]
    precio = request.form["precio"]
    color = request.form["color"]
    kilometraje = request.form["kilometraje"]
    descripcion = request.form["descripcion"]

    # Condicion si tenemos todos los campos
    if marca and modelo and año and precio and color and kilometraje and descripcion:
        # consultamos a la base de datos
        cursor = db.database.cursor()
        # Actualizamos los datos de la base de datos
        sql = "UPDATE autos SET marca = %s, modelo = %s, año = %s, precio = %s, color = %s, kilometraje = %s, descripcion = %s WHERE id = %s"
        # Indicamos una tupla con los datos
        data = (marca, modelo, año, precio, color, kilometraje, descripcion, id)
        # Le pasamos los datos con la funcion "execute"
        cursor.execute(sql, data)
        # Hacemos el commit a la base de datos sino no funciona
        db.database.commit()
    return redirect(url_for("home"))


# Subimos la App
# Le preguntamos si lanzamos como programa principal el __main__
if __name__ == "__main__":
    # Con la función "run" de flask, indicamos que estamos en modo desarrollo "debug=true" y el puerto "port=3000"
    app.run(debug=True, port=4000)
