from flask_mail import Message
from app import mail

def send_reset_email(to, reset_link):
    msg = Message("Password Reset Request",
                  sender="adolfo.berrocal@vallegrande.edu.pe",
                  recipients=[to])
    msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_link}'
    try:
        mail.send(msg)
        print(f"Correo de restablecimiento de contraseña enviado a {to}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
