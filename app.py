from flask import Flask, redirect, url_for, render_template, request
from flask.helpers import flash
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'v}*`KT3:82^dc[|M?.rYs/)QP#:2Bf*0M#WaG"$aq.iPMnA_vph&5=RL;_e"|Br'
app.config['SESSION_TYPE'] = 'filesystem'
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    titulo = "COLFEAR | INICIO DE SESIÓN"
    return render_template('login.html', titulo=titulo)

@app.route('/procesar_login', methods=['POST'])
def login():
    error = None
    if request.method=='POST':
        datos = request.form
        if (datos['txtUsuario']!="" and datos['txtPassword']!=""):
            if comprobarLogin(datos['txtUsuario'],datos['txtPassword']):
                flash('Login realizado con exito')
                return redirect(url_for('principal'))
            else:
                 error = "Usuario o contraseña incorrectos"
        else:
            error = "Ingrese sus credenciales por favor"
    return redirect(url_for('index'))

@app.route("/principal")
def principal():
    titulo = "COLFEAR | PRINCIPAL"
    return render_template('principal.html', titulo=titulo)

def comprobarLogin(usuario,password):

    if (usuario=="ajcolman" and bcrypt.check_password_hash('$2y$12$CBGt2N9p.FtMqKdRXW3HQ.V6qNs6jeYzn2RgvHZ7LdWuAMPIwFxdu',password)):
        return True
    else:
        return False

@app.route('/cerrar_sesion')
def cerrarSesion():
    return redirect(url_for('index'))

if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, debug=True)

