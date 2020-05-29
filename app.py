from flask import Flask, render_template, request, redirect, url_for

# modulo para gestionar sql sin tener que usar directamente instrucciones sql sino de python
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)  # Esta es la aplicación de servidor

# tenemos que configurar donde se encuentra la base de datos que para sqlite es SQLALCHEMY_DATABASE_URI
# Para otras bases de datos hay que consultar la documentación en google sqlalchemy database uri
# Si el dia de mañana en ves de sqlite queremos usar otro tipo de base solo hay que cambiar la linea de abajo
# por la que corresponda.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
# crea una instancia o cursor de la base de datos donde puedo hacer consultas, lo llamare db
# Pero aun asi tenemos que crear la base de datos que utilizaremos mysql, sqlite3 etc
# usaremos sqlite3 aparte para crearla solamente (lo hice aparte)
db = SQLAlchemy(app)


# Vamos a crear un modelo de datos a partir de lo que recibimos del formulario.
# la clase la creamos pq aunque sqlalchemy ya esta conectada a la base de datos db, vamos a modelarlos
# para poder guardarlos. Es decir vamos a definir los campos de la base de datos.

# Creamos la clase Task() y dentro una instancia de la conexion db pa moldearlos
class Task(db.Model):
    # Nuestra tabla se llamara Task
    # Vamos a definir los campos o registros qu estan relacionados con la tarea
    # Estos seran por cada tarea: un id, un contenido y un campo para ver si esta hecha o no.
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)
    # IMPORTANTE: ESTO NO NOS CREA NI LA BASE DE DATOS NI SU ESTRUCTURA. YO LO HE HECHO PREVIAMENTE CON
    # EL PROGRAMA DB BROWSER

# vista inicial nada mas entrar al navegador


@app.route("/")
def home():
    # cada vez que entremos a la pagina inicial vamos a hacer una consulta a la base de datos y mostraremos el
    # resultado en la pantalla. Desde Task voy a consultar por todos los datos que tengo y lo guardare en una variable
    # llamada tasks
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)
    # PARA QUE SE RENDERICEN LAS PLANTILLAS TIENEN QUE ESTAR EN EL DIRECTORIO <TEMPLATES>
    # EN EL DIRECTORIO STATIC ESTARAN LAS IMAGENES CSS ETC, TODO LO ESTATICO


# Vista para guardar lo que nos envie el formulario, con el metodo POST


@app.route("/crear_tarea/", methods=['POST'])
def crear():
    '''funcion para recibir los datos del formulario request.form y crear la tarea (name="contenido) en html'''
    # A la clase task le ponemos lo que queremos añadir.
    # el campo id no necesitamos pasarselo porque lo crea automaticamente la base de datos.
    # creo una nueva tarea en el que el content es lo que me pasa el formulario como contenido
    # Al crear la nueva tarea el done estara en False porque aun no la he realizado
    # la tarea la guardaremos en una variable llamada task en minusculas
    task = Task(content=request.form['contenido'], done=False)
    # la variable task es una instancia de una clase, es decir es un objeto que ya podemos guardar en nuestra
    # base de datos con la sentencia siguiente:
    db.session.add(task)
    db.session.commit()
    # tambien se puede utilizar return redirect(url_for('home')) importando, eso si, url_for
    return redirect("/")

# RUTA PARA TAREA COMPLETADA
@app.route('/done/<id>')
def done(id):
    task=Task.query.filter_by(id=int(id)).first()
    task.done =not(task.done) # Intercambia los valores si es Falso a Verdadero y viceversa.
    db.session.commit()
    return redirect(url_for('home'))


# VISTA PARA BORRAR LAS TAREAS. se va a llamar a la tarea pasando el numero de parametro a borrar, que va a ser recogida
# en la función.
@app.route("/borrar_tarea/<id>")
def borrar(id):
    # Filtramos la base de datos para que busque el registro en que el primer valor que coincida con la id pasada y lo borre.
    # int(id) es para convertir el parametro que siempre es string en un numero
    task=Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    # le devuelto a la pagina principal
    return redirect(url_for('home'))

if __name__ == "__main__":
    # debug=True para que cada vez que cambiemos algo el servidor se reinice por si solo
    app.run(debug=True)

# ejemplo estraido de https://www.youtube.com/watch?v=V9VU1g4IWlg
