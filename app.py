from flask import Flask
# modulo para gestionar sql sin tener que usar directamente instrucciones sql sino de python
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Esta es la aplicación de servidor
# tenemos que configurar donde se encuentra la base de datos que para sqlite es SQLALCHEMY_DATABASE_URI
# Para otras bases de datos hay que consultar la documentación en google sqlalchemy database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'

# crea una instancia o cursor de la base de datos donde puedo hacer consultas, lo llamare db
# Pero aun asi tenemos que crear la base de datos que utilizaremos mysql, sqlite3 etc
# usaremos sqlite3 aparte para crearla solamente (lo hice aparte)
db = SQLAlchemy(app)

# vista inicial nada mas entrar al navegador


@app.route("/")
def home():
    return "<h1>Bienvenido al servidor</h1><br><hr>"


if __name__ == "__main__":
    # debug=True para que cada vez que cambiemos algo el servidor se reinice por si solo
    app.run(debug=True)
