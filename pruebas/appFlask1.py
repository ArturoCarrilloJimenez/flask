from flask import Flask; # Importo Flask
app = Flask(__name__);

# Defino la ruta principal, la raiz
@app.route('/')
def hello_word():
    return 'Hello, Word!';

# Le indico la ip y el puerto asociado
if __name__ == '__main__':
    app.run('0.0.0.0',8080);

