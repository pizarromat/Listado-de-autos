# Instalamos mysql-connector
# pip install  mysql-connector-python

# Importamos la base de datos "mysql.connector"
import mysql.connector

# Creamos una variable llamada "conexion", le decimos que la conexion es de "mysql.connector.connect(usuario,contraseña,host,base de datos,puerto)"
database = mysql.connector.connect(
    user="root",
    password="---",
    host="localhost",
    database="---",
    port="---",
)
