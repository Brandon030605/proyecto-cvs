import sqlite3

conexion = sqlite3.connect("cvs.db")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM cvs")
registros = cursor.fetchall()

for registro in registros:
    print(registro)

conexion.close()

