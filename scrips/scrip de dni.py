import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

API_KEY = "fc71a2aabd01f9e1cccce39f4c14e491ad6115339ab1df7324c2e22e1d192938"
BASE_URL = "https://apiperu.dev/api"

def get_dni_info(dni):
    url = f"{BASE_URL}/dni/{dni}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

if __name__ == "__main__":
    dni = input("Ingrese el número de DNI: ")
    info = get_dni_info(dni)
    
    if info:
        print("Información del DNI:")
        print(info)
    else:
        print("No se pudo obtener la información del DNI.")
