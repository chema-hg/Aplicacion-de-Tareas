from flask import Flask

app = Flask(__name__)  # Esta es la aplicación de servidor


# vista inicial nada mas entrar al navegador


@app.route("/")
def home():
    return "<h1>Bienvenido al servidor</h1><br><hr>"


if __name__ == "__main__":
    # debug=True para que cada vez que cambiemos algo el servidor se reinice por si solo
    app.run(debug=True)
