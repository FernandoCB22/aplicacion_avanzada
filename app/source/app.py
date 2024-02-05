from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, and_
import pandas as pd
import tempfile
import os
import io
from openpyxl import load_workbook, Workbook
from openpyxl.styles import NamedStyle

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/aplicacion'  # Cambia según tu configuración
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'  # Cambia por una clave segura

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Modelo de usuario
class User(UserMixin, db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    clave = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comenzar', methods=['GET', 'POST'])
def comenzar():
    if request.method == 'POST':
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        # Verificar las credenciales en la base de datos
        user = User.query.filter_by(usuario=usuario, clave=clave).first()

        if user:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index2'))
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.', 'danger')

    return render_template('login.html')


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    documentacion = db.Column(db.String(9), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Enum('M', 'F'), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    institucion = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.Enum('Coordinador', 'Profesor', 'Tutor', 'Alumno'), nullable=False)
    telefono = db.Column(db.String(25), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    direccionp = db.Column(db.String(150), nullable=False)


@app.route('/index2', methods=['GET', 'POST'])
@login_required
def index2():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        documentacion = request.form['documento']
        fecha_nacimiento = request.form['fecha_nacimiento']
        genero =request.form['genero']
        correo = request.form['correo']
        institucion = request.form['institucion']
        cargo = request.form['cargo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        direccionp = request.form['direccionp']

        # Crear un nuevo usuario y agregarlo a la base de datos
        nuevo_usuario = Usuario(nombre=nombre, apellidos=apellidos, documentacion=documentacion, fecha_nacimiento=fecha_nacimiento, genero=genero, correo=correo, institucion=institucion, cargo=cargo, telefono=telefono, direccion=direccion, direccionp=direccionp)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
    usuarios = Usuario.query.all()
    return render_template('index2.html', usuarios=usuarios)


@app.route('/resultados', methods=['GET'])
def resultados():
    # Obtén los parámetros de búsqueda del formulario
    nombre = request.args.get('nombre', '')
    apellidos = request.args.get('apellidos', '')
    documentacion = request.args.get('documentacion', '')
    fecha_nacimiento = request.args.get('fecha_nacimiento', '')
    genero = request.args.get('genero', '')
    correo = request.args.get('correo', '')
    institucion = request.args.get('institucion', '')
    cargo = request.args.get('cargo', '')
    telefono = request.args.get('telefono', '')
    direccion = request.args.get('direccion', '')
    direccionp = request.args.get('direccionp', '')

    # Construye la consulta SQL basada en los parámetros de búsqueda
    consulta = Usuario.query

    if nombre:
        consulta = consulta.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if apellidos:
        consulta = consulta.filter(Usuario.apellidos.ilike(f"%{apellidos}%"))
    if documentacion:
        consulta = consulta.filter(Usuario.documentacion.ilike(f"%{documentacion}%"))
    if fecha_nacimiento:
        # Puedes ajustar la comparación según tu necesidad
        consulta = consulta.filter(Usuario.fecha_nacimiento == fecha_nacimiento)
    if genero and genero in ('M', 'F'):
        consulta = consulta.filter(Usuario.genero == genero)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()
    if correo:
        consulta = consulta.filter(Usuario.correo.ilike(f"%{correo}%"))
    if institucion:
        consulta = consulta.filter(Usuario.institucion.ilike(f"%{institucion}%"))
    if cargo and cargo in ('Coordinador', 'Profesor', 'Tutor', 'Alumno'):
        consulta = consulta.filter(Usuario.cargo == cargo)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()
    if telefono:
        consulta = consulta.filter(Usuario.telefono.ilike(f"%{telefono}%"))
    if direccion:
        consulta = consulta.filter(Usuario.direccion.ilike(f"%{direccion}%"))
    if direccionp:
        consulta = consulta.filter(Usuario.direccionp.ilike(f"%{direccionp}%"))

    # Obtén los resultados de la consulta
    resultados = consulta.all()

    # Renderiza la plantilla 'resultados.html' con los resultados
    return render_template('resultados.html', resultados=resultados)

# Definir la función para obtener los resultados de la búsqueda
def obtener_resultados(nombre, apellidos, documentacion, fecha_nacimiento, genero, correo, institucion, cargo, telefono, direccion, direccionp):
    # Construir la consulta SQL basada en los parámetros de búsqueda
    consulta = Usuario.query

    if nombre:
        consulta = consulta.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if apellidos:
        consulta = consulta.filter(Usuario.apellidos.ilike(f"%{apellidos}%"))
    if documentacion:
        consulta = consulta.filter(Usuario.documentacion.ilike(f"%{documentacion}%"))
    if fecha_nacimiento:
        # Puedes ajustar la comparación según tu necesidad
        consulta = consulta.filter(Usuario.fecha_nacimiento == fecha_nacimiento)
    if genero and genero in ('M', 'F'):
        consulta = consulta.filter(Usuario.genero == genero)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()
    if correo:
        consulta = consulta.filter(Usuario.correo.ilike(f"%{correo}%"))
    if institucion:
        consulta = consulta.filter(Usuario.institucion.ilike(f"%{institucion}%"))
    if cargo and cargo in ('Coordinador', 'Profesor', 'Tutor', 'Alumno'):
        consulta = consulta.filter(Usuario.cargo == cargo)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()
    if telefono:
        consulta = consulta.filter(Usuario.telefono.ilike(f"%{telefono}%"))
    if direccion:
        consulta = consulta.filter(Usuario.direccion.ilike(f"%{direccion}%"))
    if direccionp:
        consulta = consulta.filter(Usuario.direccionp.ilike(f"%{direccionp}%"))

    resultados = consulta.all()

    return resultados


@app.route('/generar_excel', methods=['GET'])
def generar_excel():
    # Obtén los parámetros de búsqueda del formulario
    nombre = request.args.get('nombre', '')
    apellidos = request.args.get('apellidos', '')
    documentacion = request.args.get('documentacion', '')
    fecha_nacimiento = request.args.get('fecha_nacimiento', '')
    genero = request.args.get('genero', '')
    correo = request.args.get('correo', '')
    institucion = request.args.get('institucion', '')
    cargo = request.args.get('cargo', '')
    telefono = request.args.get('telefono', '')
    direccion = request.args.get('direccion', '')
    direccionp = request.args.get('direccionp', '')

    # Construye la consulta SQL basada en los parámetros de búsqueda
    consulta = Usuario.query

    if nombre:
        consulta = consulta.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if apellidos:
        consulta = consulta.filter(Usuario.apellidos.ilike(f"%{apellidos}%"))
    if documentacion:
        consulta = consulta.filter(Usuario.documentacion.ilike(f"%{documentacion}%"))
    if fecha_nacimiento:
        # Puedes ajustar la comparación según tu necesidad
        consulta = consulta.filter(Usuario.fecha_nacimiento == fecha_nacimiento)
    if genero and genero in ('M', 'F'):
        consulta = consulta.filter(Usuario.genero == genero)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()
    if correo:
        consulta = consulta.filter(Usuario.correo.ilike(f"%{correo}%"))
    if institucion:
        consulta = consulta.filter(Usuario.institucion.ilike(f"%{institucion}%"))
    if cargo and cargo in ('Coordinador', 'Profesor', 'Tutor', 'Alumno'):
        consulta = consulta.filter(Usuario.cargo == cargo)
    else:
            # Si no se proporciona género, no aplicar filtro por género
        consulta = consulta.filter()
    if telefono:
        consulta = consulta.filter(Usuario.telefono.ilike(f"%{telefono}%"))
    if direccion:
        consulta = consulta.filter(Usuario.direccion.ilike(f"%{direccion}%"))
    if direccionp:
        consulta = consulta.filter(Usuario.direccionp.ilike(f"%{direccionp}%"))

    resultados = consulta.all()

    # Crear un DataFrame de pandas con los resultados
    data = {
        'Nombre': [usuario.nombre for usuario in resultados],
        'Apellidos': [usuario.apellidos for usuario in resultados],
        'Documentacion': [usuario.documentacion for usuario in resultados],
        'Fecha de Nacimiento': [usuario.fecha_nacimiento for usuario in resultados],
        'Género': [usuario.genero for usuario in resultados],
        'Correo Electrónico': [usuario.correo for usuario in resultados],
        'Institución': [usuario.institucion for usuario in resultados],
        'Cargo': [usuario.cargo for usuario in resultados],
        'Teléfono': [usuario.telefono for usuario in resultados],
        'Dirección': [usuario.direccion for usuario in resultados],
        'Dirección Personal': [usuario.direccionp for usuario in resultados],
    }

    df = pd.DataFrame(data)

    # Crear un archivo Excel temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        excel_filename = temp_file.name
        df.to_excel(excel_filename, index=False)
        
        # Abrir el libro de trabajo Excel usando openpyxl
        workbook = load_workbook(excel_filename)

        # Obtener la hoja activa
        sheet = workbook.active

        # Establecer el ancho de la columna para la fecha de nacimiento
        for col in range(ord('A'), ord('L')):
            col_letter = chr(col)
            sheet.column_dimensions[col_letter].width = 22
        
        # Guardar los cambios
        workbook.save(excel_filename)

    # Devolver el archivo Excel al usuario
    return send_file(excel_filename, as_attachment=True)


class Licencia(db.Model):
    __tablename__ = 'licencias'
    id = db.Column(db.Integer, primary_key=True)
    nombre_licencia = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_alta = db.Column(db.Date, nullable=False)
    fecha_baja = db.Column(db.Date, nullable=False)

# ...

@app.route('/alta_licencia', methods=['GET'])
@login_required
def alta_licencia():
    usuarios = Usuario.query.all()
    licencias = db.session.query(distinct(Licencia.nombre_licencia)).all()
    
    licencias = [licencia[0] for licencia in licencias]
    
    return render_template('alta_licencia.html', usuarios=usuarios, licencias=licencias)

@app.route('/procesar_alta_licencia', methods=['POST'])
@login_required
def procesar_alta_licencia():
    if request.method == 'POST':
        usuario_id = int(request.form.get('usuario'))
        licencia_nombre = request.form.get('licencia')
        fecha_alta = request.form.get('fecha_alta')
        fecha_baja = request.form.get('fecha_baja')
        
        # Verificar si la licencia ya existe para ese usuario
        licencia_existente = Licencia.query.filter_by(usuario_id=usuario_id, nombre_licencia=licencia_nombre).first()

        if licencia_existente:
            flash('El usuario ya tiene asignada esta licencia', 'danger')
            return redirect(url_for('alta_licencia'))

        # Realizar la inserción en la tabla licencias
        nueva_licencia = Licencia(usuario_id=usuario_id, nombre_licencia=licencia_nombre, fecha_alta=fecha_alta, fecha_baja=fecha_baja)
        db.session.add(nueva_licencia)
        db.session.commit()

        flash('Licencia asignada exitosamente', 'success')
        return redirect(url_for('alta_licencia'))
		
		


@app.route('/index3')
def index3():
    # Llamar a la función obtener_resultados para cada cargo
    coordinadores = obtener_resultados2('Coordinador')
    profesores = obtener_resultados2('Profesor')
    tutores = obtener_resultados2('Tutor')
    alumnos = obtener_resultados2('Alumno')

    return render_template('index3.html', coordinadores=coordinadores, profesores=profesores, tutores=tutores, alumnos=alumnos)


def obtener_resultados2(cargo):
    # Construir la consulta SQL basada en el cargo
    consulta = Usuario.query.filter(Usuario.cargo == cargo)

    resultados = consulta.all()

    return resultados


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)