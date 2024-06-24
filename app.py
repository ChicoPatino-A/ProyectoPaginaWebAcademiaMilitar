from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # La ruta base. 
def home():
    return '¡Bienvenida, estoy en Casa!'

@app.route('/johana') # La ruta base. 
def johana():
    return '¡Bienvenida Johana!'

@app.route('/principal') # nombre de la ruta
def principal(): # funcion que habre la ruta
    return render_template('index.html') # render template -> abrir la plantilla (colocamos la plantilla que queremos abrir)

@app.route('/contacto') # nombre de la ruta
def contacto(): # funcion que habre la ruta
    return render_template('contacto.html')

@app.route('/acercade') # nombre de la ruta
def acercade(): # funcion que habre la ruta
    return render_template('acercade.html')

@app.route('/iniciarsesion') # nombre de la ruta
def iniciarsesion(): # funcion que habre la ruta
    return render_template('iniciarsesion.html')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.69', port=5000)

