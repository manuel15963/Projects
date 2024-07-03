# run.py
from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

print("MAIL_USERNAME:", os.environ.get('MAIL_USERNAME'))
print("MAIL_PASSWORD:", os.environ.get('MAIL_PASSWORD'))
print("MAIL_DEFAULT_SENDER:", os.environ.get('MAIL_DEFAULT_SENDER'))
print("CLICK_SEND_API_KEY:", os.environ.get('CLICK_SEND_API_KEY'))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
