import pymysql
from pymysql import Error

def get_db():
    try:
        # Intentar conectar con PyMySQL
        print("Intentando conectar con PyMySQL...")
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            port=3306,
            autocommit=True
        )

        if connection.open:
            print("✅ Conexión exitosa con PyMySQL")

            # Crear la base de datos si no existe
            cursor = connection.cursor()
            try:
                cursor.execute("CREATE DATABASE IF NOT EXISTS veterinaria")
                print("✅ Base de datos 'veterinaria' creada/verificada")
            except Error as e:
                print(f"⚠️ Error al crear BD: {e}")
            finally:
                cursor.close()

            # Cerrar conexión inicial y reconectar a la BD específica
            connection.close()

            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="veterinaria",
                port=3306,
                autocommit=True
            )

            if connection.open:
                return connection

    except Error as e:
        print(f"❌ Error de PyMySQL: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def conectar():
    return get_db()

def desconectar(connection):
    if connection and connection.open:
        connection.close()
