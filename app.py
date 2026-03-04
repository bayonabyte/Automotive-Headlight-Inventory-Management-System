from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import math

app = Flask(__name__)
app.secret_key = "clave_segura"
app.permanent_session_lifetime = timedelta(days=6)

#Base de datos
def get_db():
    conexion = sqlite3.connect('Inventario.db')
    conexion.row_factory = sqlite3.Row
    return conexion

conexion = get_db()
cursor = conexion.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUCTO (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    MARCA TEXT,
    MODELO TEXT,
    YEAR INTEGER,
    LADO TEXT,
    UBICACION TEXT,
    CODIGO TEXT UNIQUE,
    IMAGEN TEXT
)
""")
conexion.commit()
conexion.close()

#Diccionarios
marcas = {
    "AUDI": "AUD",
    "BAIC": "BAIC",
    "BMW": "BMW",
    "CHERY": "CHY",
    "CHEVROLET": "CHV",
    "CITROEN": "CTR",
    "DFSK": "DFK",
    "FIAT": "FIA",
    "FORD": "FRD",
    "GEELY": "GEE",
    "GREAT WALL": "GWM",
    "HONDA": "HND",
    "HYUNDAI": "HYU",
    "JAC": "JAC",
    "JEEP": "JEP",
    "KIA": "KIA",
    "MAZDA": "MZD",
    "MERCEDES-BENZ": "MBZ",
    "MG": "MG",
    "MITSUBISHI": "MTS",
    "NISSAN": "NSN",
    "PEUGEOT": "PGT",
    "RAM": "RAM",
    "RENAULT": "RNL",
    "SUBARU": "SBR",
    "SUZUKI": "SZK",
    "TOYOTA": "TYT",
    "VOLKSWAGEN": "VW",
    "VOLVO": "VOL"
}
modelos = {

    "TOYOTA": {
        "COROLLA": "COR",
        "YARIS": "YRS",
        "HILUX": "HLX",
        "RAV4": "RV4",
        "FORTUNER": "FRT"
    },

    "HYUNDAI": {
        "ACCENT": "ACC",
        "ELANTRA": "ELN",
        "TUCSON": "TUC",
        "SANTA FE": "STF",
        "CRETA": "CRT"
    },

    "KIA": {
        "RIO": "RIO",
        "CERATO": "CER",
        "SPORTAGE": "SPT",
        "SOLUTO": "SOL",
        "SELTOS": "SEL"
    },

    "CHEVROLET": {
        "SPARK": "SPK",
        "AVEO": "AVE",
        "ONIX": "ONX",
        "TRACKER": "TRK",
        "CAPTIVA": "CAP"
    },

    "NISSAN": {
        "SENTRA": "SEN",
        "VERSA": "VER",
        "FRONTIER": "FRO",
        "X-TRAIL": "XTR",
        "KICKS": "KCK"
    },

    "SUZUKI": {
        "SWIFT": "SWF",
        "VITARA": "VIT",
        "ERTIGA": "ERT",
        "S-CROSS": "SCR",
        "JIMNY": "JMY"
    },

    "VOLKSWAGEN": {
        "GOL": "GOL",
        "VOYAGE": "VOY",
        "POLO": "POL",
        "T-CROSS": "TCR",
        "AMAROK": "AMR"
    },

    "MAZDA": {
        "MAZDA2": "MZ2",
        "MAZDA3": "MZ3",
        "CX-3": "CX3",
        "CX-5": "CX5",
        "BT-50": "BT5"
    },

    "MITSUBISHI": {
        "L200": "L20",
        "ASX": "ASX",
        "OUTLANDER": "OUT",
        "MONTERO": "MNT",
        "ECLIPSE CROSS": "ECR"
    },

    "FORD": {
        "RANGER": "RNG",
        "ECOSPORT": "ECO",
        "ESCAPE": "ESC",
        "EXPLORER": "EXP",
        "F-150": "F15"
    },

    "CHERY": {
        "TIGGO 2": "TG2",
        "TIGGO 4": "TG4",
        "TIGGO 7": "TG7",
        "ARRIZO 5": "AR5",
        "QQ": "QQ"
    },

    "GREAT WALL": {
        "POER": "POE",
        "WINGLE 5": "WN5",
        "HAVAL H6": "HH6"
    },

    "JAC": {
        "S2": "JS2",
        "S3": "JS3",
        "S4": "JS4",
        "T6": "JT6"
    },

    "MG": {
        "MG3": "MG3",
        "MG5": "MG5",
        "ZS": "MZS",
        "HS": "MHS"
    },

    "DFSK": {
        "GLORY 560": "G56",
        "GLORY 580": "G58"
    },

    "BAIC": {
        "X35": "BX3",
        "X55": "BX5"
    },

    "GEELY": {
        "GX3": "GX3",
        "COOLRAY": "CLR",
        "AZKARRA": "AZK"
    },

    "SUBARU": {
        "IMPREZA": "IMP",
        "XV": "XV",
        "FORESTER": "FOR",
        "OUTBACK": "OBK"
    },

    "HONDA": {
        "CIVIC": "CVC",
        "CITY": "CTY",
        "CR-V": "CRV",
        "HR-V": "HRV"
    },

    "RENAULT": {
        "LOGAN": "LOG",
        "SANDERO": "SND",
        "DUSTER": "DST",
        "OROCH": "ORC"
    },

    "PEUGEOT": {
        "208": "P208",
        "2008": "P2008",
        "3008": "P3008",
        "PARTNER": "PRT"
    },

    "CITROEN": {
        "C3": "C3",
        "C4": "C4",
        "C-ELYSEE": "CEL"
    },

    "JEEP": {
        "COMPASS": "CMP",
        "RENEGADE": "RNG",
        "WRANGLER": "WRG"
    },

    "RAM": {
        "700": "R700",
        "1500": "R1500"
    },

    "FIAT": {
        "MOBI": "MOB",
        "ARGO": "ARG",
        "STRADA": "STR"
    },

    "BMW": {
        "X1": "X1",
        "X3": "X3",
        "SERIE 3": "S3",
        "SERIE 5": "S5"
    },

    "MERCEDES-BENZ": {
        "CLASE A": "CLA",
        "CLASE C": "CLC",
        "GLA": "GLA",
        "GLC": "GLC"
    },

    "AUDI": {
        "A3": "A3",
        "A4": "A4",
        "Q3": "Q3",
        "Q5": "Q5"
    },

    "VOLVO": {
        "XC40": "XC4",
        "XC60": "XC6",
        "S60": "S60"
    }
}
def generar_codigo(marca, modelo, anio, lado):
    return f"FAR-{marcas[marca]}-{modelos[marca][modelo]}-{anio}-{lado}"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        recordar = request.form.get('recordar')

        if usuario == "Armando Faros" or password == "Taller_Armando":
            if recordar:
                session.permanent = True
            session['usuario'] = usuario
            return redirect("index")
        return render_template('login.html',
                           error="Usuario o contraseña incorrectas")
    return render_template('login.html')

@app.route('/index')
def index():
    conexion = get_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM PRODUCTO")
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT marca) FROM PRODUCTO")
    total_marcas = cursor.fetchone()[0]

    conexion.close()
    return render_template('index.html',
                           total_productos=total_productos,
                           total_marcas=total_marcas,)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    anio_actual = datetime.now().year
    codigo_generado = None
    mensaje_error = None

    if request.method == 'POST':
        marca = request.form['marca'].upper().strip()
        modelo = request.form['modelo'].upper().strip()
        anio = int(request.form['anio'])
        if anio < 2000 or anio > anio_actual:
            mensaje_error = "El año debe estar entre 2000 y el año actual"
            return render_template(
                'registrar.html',
                codigo=None,
                error=mensaje_error,
                anio_actual=anio_actual
            )
        lado = request.form['lado'].upper().strip()
        ubicacion = request.form.get('ubicacion', '').upper().strip()
        imagen = request.files['imagen']

        if marca in marcas and modelo in modelos.get(marca, {}):
            codigo_generado = generar_codigo(marca, modelo, anio, lado)

            try:
                conexion = get_db()
                cursor = conexion.cursor()

                cursor.execute("""
                INSERT INTO PRODUCTO (MARCA, MODELO, YEAR, LADO, UBICACION, CODIGO, IMAGEN)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (marca, modelo, anio, lado, ubicacion, codigo_generado, None))

                conexion.commit()

                if imagen:
                    extension = os.path.splitext(imagen.filename)[1]
                    nombre_imagen = secure_filename(codigo_generado + extension)
                    ruta_guardado = os.path.join('static/uploads', nombre_imagen)
                    imagen.save(ruta_guardado)

                    cursor.execute("""
                    UPDATE PRODUCTO SET IMAGEN = ?
                    WHERE CODIGO = ?
                    """, (nombre_imagen, codigo_generado))

                    conexion.commit()

            except sqlite3.IntegrityError:
                mensaje_error = "Ese producto ya existe en el inventario."
                codigo_generado = None

            finally:
                conexion.close()
        else:
            mensaje_error = "Marca o modelo inválido."

    return render_template(
        'registrar.html',
        codigo=codigo_generado,
        error=mensaje_error,
        anio_actual=anio_actual,
        marcas=marcas,
        modelos=modelos,
    )

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():

    conexion = get_db()
    cursor = conexion.cursor()
    anio_actual = datetime.now().year

    productos_por_pagina = 10
    pagina = request.args.get("page", 1, type=int)
    filtro = request.args.get("busqueda", "").upper().strip()

    offset = (pagina - 1) * productos_por_pagina

    if filtro:
        cursor.execute("""
            SELECT COUNT(*) FROM PRODUCTO
            WHERE MARCA LIKE ?
            OR MODELO LIKE ?
            OR CODIGO LIKE ?
        """, ("%" + filtro + "%", "%" + filtro + "%", "%" + filtro + "%"))

        total_productos = cursor.fetchone()[0]

        cursor.execute("""
            SELECT * FROM PRODUCTO
            WHERE MARCA LIKE ?
            OR MODELO LIKE ?
            OR CODIGO LIKE ?
            LIMIT ? OFFSET ?
        """, ("%" + filtro + "%", "%" + filtro + "%", "%" + filtro + "%",
              productos_por_pagina, offset))
    else:
        cursor.execute("SELECT COUNT(*) FROM PRODUCTO")
        total_productos = cursor.fetchone()[0]

        cursor.execute("""
            SELECT * FROM PRODUCTO
            LIMIT ? OFFSET ?
        """, (productos_por_pagina, offset))

    productos = cursor.fetchall()

    total_paginas = math.ceil(total_productos / productos_por_pagina)

    conexion.close()

    return render_template(
        'buscar.html',
        productos=productos,
        anio_actual=anio_actual,
        marcas=marcas,
        pagina=pagina,
        total_paginas=total_paginas,
        busqueda=filtro
    )

@app.route("/modificar")
def modificar():

    conexion = get_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM PRODUCTO")
    total = cursor.fetchone()[0]

    if total == 0:
        conexion.close()
        return render_template("modificar.html",
                               productos=[],
                               buscar=None,
                               mensaje="No hay productos registrados para modificar")

    buscar = request.args.get("buscar")

    if buscar:
        cursor.execute("""
            SELECT * FROM PRODUCTO
            WHERE MARCA LIKE ?
            OR MODELO LIKE ?
            OR YEAR LIKE ?
            OR CODIGO LIKE ?
        """, (f"%{buscar}%", f"%{buscar}%", f"%{buscar}%", f"%{buscar}%"))

        productos = cursor.fetchall()
    else:
        productos = []

    conexion.close()

    return render_template("modificar.html",
                           productos=productos,
                           buscar=buscar,
                           mensaje=None)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conexion = get_db()
    cursor = conexion.cursor()

    if request.method == "POST":

        marca = request.form["marca"]
        modelo = request.form["modelo"]
        anio = request.form["anio"]
        lado = request.form["lado"]
        ubicacion = request.form["ubicacion"]

        nuevo_codigo = generar_codigo(marca, modelo, anio, lado)

        cursor.execute("SELECT CODIGO, IMAGEN FROM PRODUCTO WHERE ID=?", (id,))
        producto_actual = cursor.fetchone()

        codigo_viejo = producto_actual["CODIGO"]
        imagen_vieja = producto_actual["IMAGEN"]

        cursor.execute("SELECT id FROM PRODUCTO WHERE codigo=? AND id!=?",
                       (nuevo_codigo, id))
        existe = cursor.fetchone()

        if existe:
            conexion.close()
            return "Ya existe un producto con ese código."

        if codigo_viejo != nuevo_codigo and imagen_vieja:

            extension = os.path.splitext(imagen_vieja)[1]

            ruta_vieja = os.path.join("static/uploads", imagen_vieja)
            nueva_imagen = nuevo_codigo + extension
            ruta_nueva = os.path.join("static/uploads", nueva_imagen)

            if os.path.exists(ruta_vieja):
                os.rename(ruta_vieja, ruta_nueva)

            imagen_vieja = nueva_imagen

        cursor.execute("""
            UPDATE PRODUCTO
            SET MARCA=?, MODELO=?, YEAR=?, LADO=?, UBICACION=?, CODIGO=?, IMAGEN=?
            WHERE ID=?
        """, (marca, modelo, anio, lado, ubicacion, nuevo_codigo, imagen_vieja, id))

        conexion.commit()
        conexion.close()

        return redirect("/modificar")

    cursor.execute("SELECT * FROM PRODUCTO WHERE id=?", (id,))
    producto = cursor.fetchone()

    conexion.close()

    return render_template(
        "editar.html",
        producto=producto,
        marcas=marcas,
        modelos=modelos
    )

@app.route("/eliminar", methods=["GET"])
def eliminar():

    conexion = get_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM PRODUCTO")
    total = cursor.fetchone()[0]

    if total == 0:
        conexion.close()
        return render_template("eliminar.html",
                               productos=[],
                               buscar=None,
                               mensaje="No hay productos registrados para eliminar")

    buscar = request.args.get("buscar")

    if buscar:
        cursor.execute("""
            SELECT * FROM PRODUCTO
            WHERE MARCA LIKE ?
            OR MODELO LIKE ?
            OR YEAR LIKE ?
            OR CODIGO LIKE ?
        """, (f"%{buscar}%", f"%{buscar}%", f"%{buscar}%", f"%{buscar}%"))

        productos = cursor.fetchall()
    else:
        productos = []

    conexion.close()

    return render_template("eliminar.html",
                           productos=productos,
                           buscar=buscar,
                           mensaje=None)

@app.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conexion = get_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT IMAGEN FROM PRODUCTO WHERE ID=?", (id,))
    producto = cursor.fetchone()

    if producto and producto["IMAGEN"]:
        ruta = os.path.join("static/uploads", producto["IMAGEN"])

        if os.path.exists(ruta):
            os.remove(ruta)

    cursor.execute("DELETE FROM PRODUCTO WHERE ID=?", (id,))
    conexion.commit()
    conexion.close()

    return redirect("/eliminar")

if __name__ == '__main__':
    app.run()