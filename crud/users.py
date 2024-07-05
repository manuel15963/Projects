import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from db.connection import connect_db

def get_users(status='active'):
    connection = connect_db()
    if connection:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if status == 'inactive':
                query = "SELECT id, username, last_name, doc, email, phone, active FROM users WHERE active = 'I'"
            else:
                query = "SELECT id, username, last_name, doc, email, phone, active FROM users WHERE active = 'A'"
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return users
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            cursor.close()
            connection.close()
    return []

def add_user_to_db(username, last_name, doc, email, phone, password):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE doc = %s OR email = %s OR phone = %s", (doc, email, phone))
            existing_user = cursor.fetchone()
            if existing_user:
                if existing_user[3] == doc:
                    return False, "El DNI ya está registrado no te creas habil."
                elif existing_user[4] == email:
                    return False, "El correo electrónico ya está registrado no te creas habil ."
                elif existing_user[5] == phone:
                    return False, "El teléfono ya está registrado no te creas habil."

            hashed_password = generate_password_hash(password)
            query = """
                INSERT INTO users (username, last_name, doc, email, phone, password, active)
                VALUES (%s, %s, %s, %s, %s, %s, 'A')
            """
            cursor.execute(query, (username, last_name, doc, email, phone, hashed_password))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Usuario registrado exitosamente."
        except Exception as e:
            cursor.close()
            connection.close()
            return False, f"Error al agregar usuario a la base de datos: {e}"
        
        
def get_user_by_id(user_id):
    connection = connect_db()
    if connection:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "SELECT id, username, email FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            cursor.close()
            connection.close()
    return None

def update_user_in_db(user_id, username, last_name, doc, email, phone):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
                UPDATE users
                SET username = %s, last_name = %s, doc = %s, email = %s, phone = %s
                WHERE id = %s
            """
            cursor.execute(query, (username, last_name, doc, email, phone, user_id))
            connection.commit()
            print(f"User updated in database: {username}")
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            cursor.close()
            connection.close()

def deactivate_user_in_db(user_id):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            query = "UPDATE users SET active = 'I' WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            print(f"User deactivated: {user_id}")
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error al desactivar el usuario: {e}")
            cursor.close()
            connection.close()

def activate_user_in_db(user_id):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            query = "UPDATE users SET active = 'A' WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            print(f"User activated: {user_id}")
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error al activar el usuario: {e}")
            cursor.close()
            connection.close()

def get_user_by_username(username):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            query = "SELECT id, username, email, password FROM users WHERE username = %s AND active = 'A'"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'password': user[3]
                }
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            cursor.close()
            connection.close()
    return None


def get_user_by_email(email):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Exception as e:
            print(f"Error al obtener el usuario por email: {e}")
            cursor.close()
            connection.close()
    return None

def update_user_password(email, password):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            hashed_password = generate_password_hash(password)
            print(f"Generated hashed password for reset: {hashed_password}")
            query = "UPDATE users SET password = %s WHERE email = %s"
            cursor.execute(query, (hashed_password, email))
            connection.commit()
            print(f"Password updated for user with email: {email}")
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error al actualizar la contraseña: {e}")
            cursor.close()
            connection.close()
