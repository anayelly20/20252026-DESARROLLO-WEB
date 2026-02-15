from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! Inicio de proyecto Semana 09'

@app.route('/saludo')
def saludo():
    return '¡Hola! inicio del proyecto clinica veterinaria DAG 09'

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

if __name__ == '__main__':
    app.run(debug=True)

