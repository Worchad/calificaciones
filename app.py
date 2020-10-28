import sqlite3
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask import json
from flask.globals import session
from flask.helpers import flash
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
import sqlite3 as sql
from flask import g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import os


app = Flask(__name__)
app.secret_key = 'v}*`KT3:82^dc[|M?.rYs/)QP#:2Bf*0M#WaG"$aq.iPMnA_vph&5=RL;_e"|Br'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path, 'sica.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Usuarios = Base.classes.usuarios
RolesUsuarios = Base.classes.roles_usuarios
Personas = Base.classes.personas
Roles = Base.classes.roles


@app.route('/')
def index():
    titulo = "COLFEAR | INICIO DE SESIÓN"
    return render_template('login.html', titulo=titulo)


@app.route('/procesar_login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        datos = request.form
        if (datos['txtUsuario'] != "" and datos['txtPassword'] != "" and datos['sltRol']):
            if comprobarLogin(datos['txtUsuario'], datos['txtPassword'], datos['sltRol']):
                return redirect(url_for('principal'))
            else:
                 flash(u'Credenciales incorrectas', 'warning')
        else:
         flash(u'Debe ingresar sus credenciales para ingresar al sistema', 'warning')
    return redirect(url_for('index'))


@app.route("/principal")
def principal():
    if session.get('conectado') == 'S':
        titulo = "COLFEAR | PRINCIPAL"
        return render_template('principal.html', titulo=titulo)
    else:
        flash(u'Debe ingresar sus credenciales para ingresar al sistema', 'warning')
        return redirect(url_for('index'))


def comprobarLogin(usuario, password, rol):
    results = db.session.query(Personas,Usuarios,Roles,RolesUsuarios)\
    .filter(Personas.pers_cod == Usuarios.usua_pers_cod,Usuarios.usua_cod == RolesUsuarios.rous_usua_cod,Roles.rol_cod == RolesUsuarios.rous_rol_cod,Personas.pers_nro_doc == usuario, RolesUsuarios.rous_rol_cod == rol).all()
    hash = None
    for r in results:
        session['conectado'] = 'S'
        session['usua_cod'] = r.usuarios.usua_cod
        session['usua_cedula'] = r.personas.pers_nro_doc
        session['usua_nombre'] = r.personas.pers_prim_nombre+' '+r.personas.pers_seg_nombre + \
            ' '+r.personas.pers_prim_apellido+' '+r.personas.pers_seg_apellido
        session['usua_rold'] = r.roles.rol_desc
        hash = r.usuarios.usua_password
        if bcrypt.check_password_hash(hash,password):
            if 'usua_cod' in session:
                return True
            else:
                return False
        else:
           return False

@app.route('/cambio_password')
def cambioPassword():
    titulo = "Cambio de Contraseña"
    return render_template('cambioPassword.html',titulo=titulo)





@app.route('/cerrar_sesion')
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, debug=True)

