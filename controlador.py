from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask.globals import session
from flask.helpers import flash
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from form import FormCambioPassword,FormRegistroPersona
import datetime
import base64



app = Flask(__name__)
app.config.from_object('config')
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


Base = automap_base()
Base.prepare(db.engine, reflect=True)
Usuarios = Base.classes.usuarios
RolesUsuarios = Base.classes.roles_usuarios
Personas = Base.classes.personas
Roles = Base.classes.roles
Carreras = Base.classes.carreras
Materias = Base.classes.materias
CarrerasMaterias = Base.classes.carrera_materias
TitularMaterias = Base.classes.titular_materias
AlumnoMaterias = Base.classes.alumno_materias


fecha = datetime.datetime.now()
fechaActual = fecha.strftime("%d/%m/%Y %H:%M:%S");


@app.route('/')
def index():
    if session.get('conectado') == 'S':
        titulo = "COLFEAR | PRINCIPAL"
        return render_template('principal.html', titulo=titulo)
    else:
        titulo = "COLFEAR | INICIO DE SESIÓN"
        return render_template('login.html', titulo=titulo)

@app.route('/procesar_login', methods=['POST'])
def login():
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
            session['usua_nombre'] = r.personas.pers_prim_nombre+' '+r.personas.pers_prim_apellido
            session['usua_rold'] = r.roles.rol_desc
            session['usua_rol'] = r.roles.rol_cod
            hashpassword = r.usuarios.usua_password
            if bcrypt.check_password_hash(hashpassword,password):
                if 'usua_cod' in session:
                    return True
                else:
                    return False
            else:
                return False

@app.route('/cambio_password')
def cambioPassword():
    if session.get('conectado') == 'S':
        titulo = "Cambio de Contraseña"
        return render_template('cambioPassword.html',titulo=titulo)
    else:
        flash(u'Debe ingresar sus credenciales para ingresar al sistema', 'warning')
        return redirect(url_for('index'))

@app.route('/procesar_cambio_password',methods=['POST'])
def procesarCambioPassword():
    mensajes = []
    if session.get('conectado') == 'S':
        form = FormCambioPassword(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            datos = request.form
            passActual = datos['txtPasswordActual']
            passNueva  = datos['txtPasswordNueva']
            comprobar = cambiarPassword(passActual,passNueva)
            if comprobar==True:
                mensajes = "correcto"
            else:
                mensajes = "incorrecto"
        for error in form.errors.items():
            mensajes.append(error)
    else:
        mensajes = "incorrecto"
    return jsonify(mensajes)


def cambiarPassword(passActual,passNueva):
    if session.get('conectado') == 'S':
        usuarioCod = session.get('usua_cod')
        usuario = db.session.query(Usuarios).filter(Usuarios.usua_cod==usuarioCod).first()
        if bcrypt.check_password_hash(usuario.usua_password,passActual):
            usuario.usua_password = bcrypt.generate_password_hash(passNueva)
            usuario.usua_fecha_modificacion = fechaActual
            usuario.usua_cod_modificacion = session.get('usua_cod')
            db.session.commit()
            return True
        else:
            return False
    else:
        return False


@app.route('/registrar_persona')
def registrarPersona():
    if session.get('conectado')=='S':
        titulo = "COLFEAR | Registrar Personas"
        carreras = db.session.query(Carreras).all()
        return render_template('registrarPersona.html',titulo=titulo,carreras=carreras)
    else:
        flash(u'Debe ingresar sus credenciales para ingresar al sistema', 'warning')
        return redirect(url_for('index'))

@app.route('/obtener_materias_alumnos',methods=['POST'])
def obtenerMateriasAlumnos():
    resultado = None
    if request.method=='POST':
        datos = request.form
        carrera = datos['carrera']
        query = db.session.query(Materias,CarrerasMaterias).filter(CarrerasMaterias.came_mate_cod==Materias.mate_cod,CarrerasMaterias.came_carr_cod==carrera).all()
        resultado = {}
        i = 0
        for q in query:
            resultado.update({i:{'cod_came':q.carrera_materias.came_cod,'desc_mate':q.materias.mate_desc}})
            i = i + 1

    return resultado

@app.route('/obtener_titular_materias',methods=['POST'])
def obtenerTitularMaterias():
    resultado = None
    if request.method=='POST':
        datos = request.form
        materia = datos['materia']
        anio = fecha.strftime("%Y");
        query = db.session.query(TitularMaterias,Personas).filter(TitularMaterias.tima_pers_cod==Personas.pers_cod,TitularMaterias.tima_came_cod==materia,TitularMaterias.tima_anio==anio,TitularMaterias.tima_estado=='A').all()
        resultado = {}
        i = 0
        for q in query:
            resultado.update({i:{'tima_cod':q.titular_materias.tima_cod,'profesor':q.personas.pers_prim_nombre+' '+q.personas.pers_prim_apellido,'turno':q.titular_materias.tima_turno,'grupo':q.titular_materias.tima_grupo,'modalidad':q.titular_materias.tima_modalidad,'hora_inicio':q.titular_materias.tima_horario_inicio,'hora_culminacion':q.titular_materias.tima_horario_culminacion}})
            i = i + 1

    return resultado

@app.route('/registrar_persona',methods=['POST'])
def procesarRegistroPersona():
    mensajes = []
    form = FormRegistroPersona(request.form)
    if request.method=='POST' and form.validate_on_submit():
        datos = request.form
        primerNombre = datos['txtPrimerNombre']
        segundoNombre = datos['txtSegundoNombre']
        primerApellido = datos['txtPrimerApellido']
        segundoApellido = datos['txtSegundoApellido']
        nroCedula = datos['txtNroCedula']
        sexo = datos['sltSexo']
        fechaNacimiento = datos['txtFechaNacimiento']
        if fechaNacimiento!="":
            fechaNacimiento = datetime.datetime.strptime(datos['txtFechaNacimiento'], '%Y-%m-%d').strftime('%d/%m/%Y')
        else:
            fechaNacimiento = None
        estadoCivil = datos['sltEstadoCivil']
        alumno = request.form.get('chkAlumno')
        profesor = request.form.get('chkProfesor')
        titular = request.form.getlist('txtTitular')
        materiasProfesor = request.form.getlist('txtMateriaProfesor[]')
        turnosProfesor = request.form.getlist('txtTurnoProfesor[]')
        gruposProfesor = request.form.getlist('txtGrupoProfesor[]')
        modosProfesor = request.form.getlist('txtModoProfesor[]')
        horaInicio = request.form.getlist('txtHoraInicioProfesor[]')
        horaFin = request.form.getlist('txtHoraFinProfesor[]')
        cantidad = db.session.query(Personas).filter(Personas.pers_prim_nombre==primerNombre.upper(),Personas.pers_seg_nombre==segundoNombre.upper(),Personas.pers_prim_apellido==primerApellido.upper(),Personas.pers_seg_apellido==segundoApellido.upper(),Personas.pers_nro_doc==nroCedula,Personas.pers_sexo==sexo,Personas.pers_fecha_nacimiento==fechaNacimiento,Personas.pers_estado_civil==estadoCivil).count()
        if cantidad==0:
            try:
                db.session.add(Personas(
                    pers_prim_nombre = primerNombre.upper(),
                    pers_seg_nombre = segundoNombre.upper(),
                    pers_prim_apellido = primerApellido.upper(),
                    pers_seg_apellido = segundoApellido.upper(),
                    pers_nro_doc = nroCedula,
                    pers_sexo = sexo,
                    pers_fecha_nacimiento = fechaNacimiento,
                    pers_estado_civil = estadoCivil,
                    pers_alumno = alumno,
                    pers_profesor = profesor,
                    pers_fecha_registro = fechaActual,
                    pers_usua_cod_registro = session.get('usua_cod')
                ))
                db.session.flush()
                ultimoCod = db.session.query(Personas).order_by(Personas.pers_cod.desc()).first()
                cantAlumno = len(titular)
                cantProfesor = len(materiasProfesor)
                if alumno!=None:
                   recorrido = 0
                   while recorrido<cantAlumno:
                     db.session.add(AlumnoMaterias(
                        alma_pers_cod = ultimoCod.pers_cod,
                        alma_tima_cod = titular[recorrido],))
                     recorrido +=1
                     db.session.flush()
                if profesor!=None:
                    recorrido = 0
                    while recorrido<cantProfesor:
                        db.session.add(TitularMaterias(
                            tima_pers_cod = ultimoCod.pers_cod,
                            tima_came_cod = materiasProfesor[recorrido],
                            tima_turno = turnosProfesor[recorrido],
                            tima_grupo = gruposProfesor[recorrido],
                            tima_modalidad = modosProfesor[recorrido],
                            tima_horario_inicio = horaInicio[recorrido],
                            tima_horario_culminacion = horaFin[recorrido],
                            tima_anio = fecha.strftime("%Y")
                        ))
                        recorrido +=1
                        db.session.flush()
                db.session.commit()
                mensajes = "correcto"
            except:
                db.session.rollback()
                mensajes = "incorrecto"
        else:
            mensajes = "existe"
    for error in form.errors.items():
        mensajes.append(error)
    return jsonify(mensajes)

@app.route('/listado_personas')
def listadoPersonas():
    if session.get('conectado')=='S':
        titulo = "COLFEAR | Listado Personas"
        personas = db.session.query(Personas).all()
        return render_template('listadoPersonas.html',titulo=titulo,personas=personas)
    else:
        flash(u'Debe ingresar sus credenciales para ingresar al sistema', 'warning')
        return redirect(url_for('index'))

@app.route('/modificar_datos_personas/<cod>')
def modificarDatosPersonas(cod):
    persCod = base64.b64decode(cod)
    carreras = db.session.query(Carreras).all()
    personas = db.session.query(Personas).filter(Personas.pers_cod==persCod).first()
    alumno = db.session.query(AlumnoMaterias).filter(AlumnoMaterias.alma_pers_cod==persCod).all()
    profesor = db.session.query(TitularMaterias).filter(TitularMaterias.tima_pers_cod==persCod).all()
    return render_template('modificarPersona.html', carreras=carreras,personas=personas,alumno=alumno,profesor=profesor)

@app.route('/cerrar_sesion')
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))
