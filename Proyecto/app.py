from flask import Flask, render_template, request, redirect, url_for, Response
from Conexion.conexion import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Usuario(UserMixin):
    def __init__(self, id, usuario, password):
        self.id = id
        self.usuario = usuario
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return Usuario(user[0], user[1], user[2])
    return None


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            especie VARCHAR(50) NOT NULL,
            raza VARCHAR(100) NOT NULL,
            edad DECIMAL(3,1) NOT NULL,
            propietario VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mascota_id INT NOT NULL,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            motivo TEXT NOT NULL,
            veterinario VARCHAR(100) NOT NULL,
            estado VARCHAR(20) DEFAULT 'Agendada',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mascota_id INT NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            descripcion TEXT NOT NULL,
            fecha DATE NOT NULL,
            veterinario VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            descripcion TEXT NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            cantidad INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()


def seed_data():
    conn = get_db()
    cursor = conn.cursor()

    # Inserta admin si no existe
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        password_hash = generate_password_hash('admin123')
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", ('admin', password_hash))

    # Inserta mascotas de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM mascotas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO mascotas (nombre, especie, raza, edad, propietario, telefono) VALUES (%s,%s,%s,%s,%s,%s)",
            [
                ('Max', 'Perro', 'Labrador', 3.5, 'Juan Pérez', '123456789'),
                ('Miau', 'Gato', 'Persa', 2.0, 'María Gómez', '987654321'),
                ('Luna', 'Perro', 'Golden Retriever', 4.0, 'Carlos Díaz', '555555555')
            ]
        )

    # Inserta citas de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM citas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO citas (mascota_id, fecha, hora, motivo, veterinario) VALUES (%s,%s,%s,%s,%s)",
            [
                (1, '2026-04-01', '10:00', 'Revisión general', 'Dr. Rodríguez'),
                (2, '2026-04-02', '14:30', 'Vacunación', 'Dra. González')
            ]
        )

    # Inserta historial de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM historial")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO historial (mascota_id, tipo, descripcion, fecha, veterinario) VALUES (%s,%s,%s,%s,%s)",
            [
                (1, 'Vacuna', 'Vacuna antirrábica anual', '2025-12-15', 'Dr. Rodríguez'),
                (2, 'Desparasitación', 'Desparasitación interna', '2025-11-20', 'Dra. González')
            ]
        )

    # Inserta productos de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (%s,%s,%s,%s)",
            [
                ('Alimento Premium Perro', 'Alimento de alta calidad para perros adultos', 45.99, 50),
                ('Collar antipulgas', 'Collar antipulgas efectivo por 8 meses', 35.50, 20),
                ('Vitaminas para gatos', 'Complemento vitamínico para gatos', 28.75, 30)
            ]
        )

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/seed_data')
def seed_data_route():
    try:
        seed_data()
        return 'Datos de prueba insertados correctamente. Usa /login con admin/admin123.'
    except Exception as e:
        return f'Error al cargar datos de prueba: {e}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        if not usuario or not password:
            return render_template('login.html', error='Por favor completa todos los campos')

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[2], password):
                user_obj = Usuario(user[0], user[1], user[2])
                login_user(user_obj)
                return redirect(url_for('productos'))

            return render_template('login.html', error='Usuario o contraseña incorrectos')

        except Exception as e:
            print(f"Error en login: {e}")
            return render_template('login.html', error='Error al validar. Intenta nuevamente')

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if not usuario or len(usuario) < 3:
            return render_template('registro.html', mensaje='El usuario debe tener al menos 3 caracteres')

        if not password or len(password) < 6:
            return render_template('registro.html', mensaje='La contraseña debe tener al menos 6 caracteres')

        if password != password_confirm:
            return render_template('registro.html', mensaje='Las contraseñas no coinciden')

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
            if cursor.fetchone():
                conn.close()
                return render_template('registro.html', mensaje='El usuario ya existe')

            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (%s,%s)",
                (usuario, password_hash)
            )
            conn.commit()
            conn.close()

            return redirect(url_for('login'))

        except Exception as e:
            print(f"Error en registro: {e}")
            return render_template('registro.html', mensaje='Error al registrar. Intenta nuevamente')

    return render_template('registro.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/productos')
@login_required
def productos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=datos)


@app.route('/nuevo')
@login_required
def nuevo():
    return render_template('producto_form.html')


@app.route('/guardar', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (%s,%s,%s,%s)",
        (nombre, descripcion, precio, cantidad)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('productos'))


@app.route('/editar/<int:id>')
@login_required
def editar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('editar_producto.html', producto=producto)


@app.route('/actualizar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s WHERE id=%s",
        (nombre, descripcion, precio, cantidad, id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('productos'))


@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('productos'))


@app.route('/mascotas')
@login_required
def mascotas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mascotas")
    datos = cursor.fetchall()
    conn.close()
    return render_template('mascotas.html', mascotas=datos)


@app.route('/nueva_mascota')
@login_required
def nueva_mascota():
    return render_template('nueva_mascota.html')


@app.route('/guardar_mascota', methods=['POST'])
@login_required
def guardar_mascota():
    nombre = request.form.get('nombre')
    especie = request.form.get('especie')
    raza = request.form.get('raza')
    edad = request.form.get('edad')
    propietario = request.form.get('propietario')
    telefono = request.form.get('telefono')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mascotas (nombre, especie, raza, edad, propietario, telefono) VALUES (%s,%s,%s,%s,%s,%s)",
        (nombre, especie, raza, edad, propietario, telefono)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('mascotas'))


@app.route('/editar_mascota/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_mascota(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        especie = request.form.get('especie')
        raza = request.form.get('raza')
        edad = request.form.get('edad')
        propietario = request.form.get('propietario')
        telefono = request.form.get('telefono')

        cursor.execute(
            "UPDATE mascotas SET nombre=%s, especie=%s, raza=%s, edad=%s, propietario=%s, telefono=%s WHERE id=%s",
            (nombre, especie, raza, edad, propietario, telefono, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('mascotas'))

    cursor.execute("SELECT * FROM mascotas WHERE id=%s", (id,))
    mascota = cursor.fetchone()
    conn.close()

    if not mascota:
        return redirect(url_for('mascotas'))

    return render_template('editar_mascota.html', mascota=mascota)


@app.route('/eliminar_mascota/<int:id>', methods=['POST'])
@login_required
def eliminar_mascota(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mascotas WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('mascotas'))


@app.route('/citas')
@login_required
def citas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT c.id, m.nombre, c.fecha, c.hora, c.motivo, c.veterinario, c.estado FROM citas c JOIN mascotas m ON c.mascota_id=m.id")
    datos = cursor.fetchall()
    conn.close()
    return render_template('citas.html', citas=datos)


@app.route('/nueva_cita')
@login_required
def nueva_cita():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM mascotas")
    mascotas_data = cursor.fetchall()
    conn.close()
    return render_template('nueva_cita.html', mascotas=mascotas_data)


@app.route('/guardar_cita', methods=['POST'])
@login_required
def guardar_cita():
    mascota_id = request.form.get('mascota_id')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    motivo = request.form.get('motivo')
    veterinario = request.form.get('veterinario')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO citas (mascota_id, fecha, hora, motivo, veterinario) VALUES (%s,%s,%s,%s,%s)",
        (mascota_id, fecha, hora, motivo, veterinario)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('citas'))


@app.route('/detalle_cita/<int:id>')
@login_required
def detalle_cita(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT c.id, m.nombre, c.fecha, c.hora, c.motivo, c.veterinario, c.estado FROM citas c JOIN mascotas m ON c.mascota_id=m.id WHERE c.id=%s", (id,))
    cita = cursor.fetchone()
    conn.close()

    if not cita:
        return redirect(url_for('citas'))

    return render_template('detalle_cita.html', cita=cita)


@app.route('/editar_cita/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cita(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo')
        veterinario = request.form.get('veterinario')

        cursor.execute(
            "UPDATE citas SET fecha=%s, hora=%s, motivo=%s, veterinario=%s WHERE id=%s",
            (fecha, hora, motivo, veterinario, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('citas'))

    cursor.execute("SELECT c.id, m.nombre, c.fecha, c.hora, c.motivo, c.veterinario, c.estado FROM citas c JOIN mascotas m ON c.mascota_id=m.id WHERE c.id=%s", (id,))
    cita = cursor.fetchone()
    conn.close()

    if not cita:
        return redirect(url_for('citas'))

    return render_template('editar_cita.html', cita=cita)


@app.route('/cancelar_cita/<int:id>', methods=['POST'])
@login_required
def cancelar_cita(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE citas SET estado='cancelada' WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('citas'))


@app.route('/historial')
@login_required
def historial():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT h.id, m.nombre, h.tipo, h.descripcion, h.fecha, h.veterinario FROM historial h JOIN mascotas m ON h.mascota_id=m.id")
    datos = cursor.fetchall()
    conn.close()
    return render_template('historial.html', historial=datos)


@app.route('/detalle_historial/<int:id>')
@login_required
def detalle_historial(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT h.id, m.nombre, h.tipo, h.descripcion, h.fecha, h.veterinario FROM historial h JOIN mascotas m ON h.mascota_id=m.id WHERE h.id=%s", (id,))
    registro = cursor.fetchone()
    conn.close()

    if not registro:
        return redirect(url_for('historial'))

    return render_template('detalle_historial.html', registro=registro)


@app.route('/editar_historial/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_historial(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        veterinario = request.form.get('veterinario')

        cursor.execute(
            "UPDATE historial SET tipo=%s, descripcion=%s, fecha=%s, veterinario=%s WHERE id=%s",
            (tipo, descripcion, fecha, veterinario, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('historial'))

    cursor.execute("SELECT h.id, m.nombre, h.tipo, h.descripcion, h.fecha, h.veterinario FROM historial h JOIN mascotas m ON h.mascota_id=m.id WHERE h.id=%s", (id,))
    registro = cursor.fetchone()
    conn.close()

    if not registro:
        return redirect(url_for('historial'))

    return render_template('editar_historial.html', registro=registro)


@app.route('/eliminar_historial/<int:id>', methods=['POST'])
@login_required
def eliminar_historial(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM historial WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('historial'))


@app.route('/nuevo_historial')
@login_required
def nuevo_historial():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM mascotas")
    mascotas_data = cursor.fetchall()
    conn.close()
    return render_template('nuevo_historial.html', mascotas=mascotas_data)


@app.route('/guardar_historial', methods=['POST'])
@login_required
def guardar_historial():
    mascota_id = request.form.get('mascota_id')
    tipo = request.form.get('tipo')
    descripcion = request.form.get('descripcion')
    fecha = request.form.get('fecha')
    veterinario = request.form.get('veterinario')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO historial (mascota_id, tipo, descripcion, fecha, veterinario) VALUES (%s,%s,%s,%s,%s)",
        (mascota_id, tipo, descripcion, fecha, veterinario)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('historial'))


# ----------------------------------
# Rutas para reporte PDF
# ----------------------------------
@app.route('/reportes')
@login_required
def reportes():
    return render_template('reportes.html')


@app.route('/reportes/generar', methods=['POST'])
@login_required
def generar_reporte():
    tipo = request.form.get('tipo_reporte')
    if not tipo:
        return redirect(url_for('reportes'))

    opciones = {
        'productos': {
            'titulo': 'Reporte de Productos',
            'sql': 'SELECT id, nombre, descripcion, precio, cantidad FROM productos',
            'encabezados': ['ID', 'Nombre', 'Descripción', 'Precio', 'Cantidad']
        },
        'mascotas': {
            'titulo': 'Reporte de Mascotas',
            'sql': 'SELECT id, nombre, especie, raza, edad, propietario, telefono FROM mascotas',
            'encabezados': ['ID', 'Nombre', 'Especie', 'Raza', 'Edad', 'Propietario', 'Teléfono']
        },
        'citas': {
            'titulo': 'Reporte de Citas',
            'sql': 'SELECT id, mascota_id, fecha, hora, motivo, veterinario, estado FROM citas',
            'encabezados': ['ID', 'Mascota ID', 'Fecha', 'Hora', 'Motivo', 'Veterinario', 'Estado']
        },
        'historial': {
            'titulo': 'Reporte de Historial Médico',
            'sql': 'SELECT id, mascota_id, tipo, descripcion, fecha, veterinario FROM historial',
            'encabezados': ['ID', 'Mascota ID', 'Tipo', 'Descripción', 'Fecha', 'Veterinario']
        },
        'usuarios': {
            'titulo': 'Reporte de Usuarios',
            'sql': 'SELECT id_usuario, usuario FROM usuarios',
            'encabezados': ['ID Usuario', 'Usuario']
        }
    }

    if tipo != 'general' and tipo not in opciones:
        return redirect(url_for('reportes'))

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 8, 'Reporte General Veterinaria DAG' if tipo == 'general' else opciones[tipo]['titulo'], 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'Fecha de generación: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 1, 'C')
    pdf.ln(6)

    def dibujar_seccion(titulo_seccion, headers, rows):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 7, titulo_seccion, 0, 1, 'L')

        page_width = 297 - 20 - 20
        width = page_width / len(headers)

        pdf.set_font('Arial', 'B', 10)
        for h in headers:
            pdf.cell(width, 7, str(h), 1, 0, 'C')
        pdf.ln()

        pdf.set_font('Arial', '', 9)
        row_height = 8
        if rows:
            for row in rows:
                # for each field in row, crear celda en la misma línea
                for i, c in enumerate(row):
                    texto = str(c) if c is not None else ''
                    pdf.cell(width, row_height, texto, 1, 0, 'C')
                pdf.ln(row_height)
        else:
            pdf.cell(0, 8, 'No existen registros disponibles para este reporte.', 1, 1, 'C')
        pdf.ln(4)

    if tipo == 'general':
        for key in ['productos', 'mascotas', 'citas', 'historial']:
            info = opciones[key]
            conn = get_db(); cursor = conn.cursor(); cursor.execute(info['sql']); filas = cursor.fetchall(); conn.close()
            dibujar_seccion(info['titulo'], info['encabezados'], filas)
    else:
        info = opciones[tipo]
        conn = get_db(); cursor = conn.cursor(); cursor.execute(info['sql']); filas = cursor.fetchall(); conn.close()
        dibujar_seccion(info['titulo'], info['encabezados'], filas)

    # Generar el contenido final del PDF como bytes
    pdf_bytes = pdf.output(dest='S').encode('latin-1')

    nombre = f'{tipo}_reporte_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename={nombre}'
        }
    )


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
