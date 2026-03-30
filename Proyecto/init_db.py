#!/usr/bin/env python3
"""
Script para inicializar las tablas de la base de datos veterinaria
"""
from Conexion.conexion import get_db

def init_database():
    conn = get_db()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return False

    cursor = conn.cursor()

    try:
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Tabla 'usuarios' creada")

        # Tabla de mascotas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mascotas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                especie VARCHAR(50) NOT NULL,
                raza VARCHAR(100) NOT NULL,
                edad INT,
                peso DECIMAL(5,2),
                propietario VARCHAR(100),
                telefono VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Tabla 'mascotas' creada")

        # Tabla de citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_mascota INT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                motivo TEXT,
                veterinario VARCHAR(100),
                estado ENUM('pendiente', 'confirmada', 'cancelada', 'completada') DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_mascota) REFERENCES mascotas(id) ON DELETE CASCADE
            )
        ''')
        print("✅ Tabla 'citas' creada")

        # Tabla de historial médico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_mascota INT,
                fecha DATE NOT NULL,
                diagnostico TEXT,
                tratamiento TEXT,
                medicamentos TEXT,
                observaciones TEXT,
                veterinario VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_mascota) REFERENCES mascotas(id) ON DELETE CASCADE
            )
        ''')
        print("✅ Tabla 'historial' creada")

        # Tabla de productos/inventario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                precio DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0,
                categoria VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Tabla 'productos' creada")

        conn.commit()
        print("✅ Todas las tablas creadas exitosamente")

        # Insertar datos de prueba
        insert_sample_data(cursor)
        conn.commit()

        return True

    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def insert_sample_data(cursor):
    try:
        # Usuario de prueba
        cursor.execute('''
            INSERT IGNORE INTO usuarios (usuario, password) VALUES
            ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeCt1uB0Y1uEXeCmW')
        ''')
        print("✅ Usuario de prueba insertado")

        # Mascotas de prueba
        cursor.execute('''
            INSERT IGNORE INTO mascotas (nombre, especie, raza, edad, peso, propietario, telefono) VALUES
            ('Max', 'Perro', 'Labrador', 3, 25.5, 'Juan Pérez', '555-0101'),
            ('Luna', 'Gato', 'Siamés', 2, 4.2, 'María García', '555-0102'),
            ('Rocky', 'Perro', 'Bulldog', 5, 30.0, 'Carlos López', '555-0103')
        ''')
        print("✅ Mascotas de prueba insertadas")

        # Productos de prueba
        cursor.execute('''
            INSERT IGNORE INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
            ('Vacuna antirrábica', 'Vacuna preventiva contra la rabia', 25.00, 50, 'Vacunas'),
            ('Desparasitante', 'Tratamiento antiparasitario interno', 15.50, 30, 'Medicamentos'),
            ('Shampoo para perros', 'Shampoo especial para piel sensible', 12.00, 20, 'Higiene'),
            ('Alimento premium', 'Alimento balanceado para perros adultos', 45.00, 100, 'Alimentos')
        ''')
        print("✅ Productos de prueba insertados")

    except Exception as e:
        print(f"⚠️ Error al insertar datos de prueba: {e}")

if __name__ == "__main__":
    print("🚀 Inicializando base de datos...")
    if init_database():
        print("✅ Base de datos inicializada correctamente")
    else:
        print("❌ Error al inicializar la base de datos")