import psycopg2
from psycopg2 import extras, Error
from werkzeug.security import generate_password_hash


def connect_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="",
            host="localhost",  # o el host donde se encuentra la BD
            port="5432",       # el puerto por defecto de PostgreSQL
            database="tienda_don_italo"
        )
        print("Conexión a la base de datos establecida")
        return connection
    except (Exception, Error) as error:
        print("Error al conectar a PostgreSQL", error)
        return None

def execute_query(query, params=None):
    connection = connect_db()
    if connection:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            connection.close()
    return []

def execute_non_query(query, params=None):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            connection.close()

#ESTE SCRIP SOLO LO EJECUTAS UNA SOLA VEZ LUEGO DE A VER  CORRIDO LA BASE DE DATOS LUEGO DE ESO LO VUELVES A COMENTAR   
# Comentado o eliminado después de la ejecución inicial


# def update_passwords():
#     connection = connect_db()
#     if connection:
#         cursor = connection.cursor()
#         try:
#             cursor.execute("SELECT id, password FROM users")
#             users = cursor.fetchall()

#             for user in users:
#                 user_id, password = user
#                 if not password.startswith('pbkdf2:sha256:'):
#                     hashed_password = generate_password_hash(password)
#                     cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))

#             connection.commit()
#             cursor.close()
#             connection.close()
#             print("Contraseñas actualizadas correctamente.")
#         except Exception as e:
#             print(f"Error al actualizar las contraseñas: {e}")
#             cursor.close()
#             connection.close()

# if __name__ == "__main__":
#     update_passwords()