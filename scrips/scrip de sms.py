import clicksend_client
from clicksend_client.rest import ApiException

# Configurar el cliente ClickSend
username = 'Marilyn12'
api_key = '6475E3FC-9F72-C441-8758-48F611CE5B26'

configuration = clicksend_client.Configuration()
configuration.username = username
configuration.password = api_key

client = clicksend_client.ApiClient(configuration)
sms_api = clicksend_client.SMSApi(client)

def send_sms(to, body):
    sms_message = clicksend_client.SmsMessage(
        source='python',
        body=body,
        to=to
    )
    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
    
    try:
        response = sms_api.sms_send_post(sms_messages)
        print(f"SMS enviado con éxito: {response}")
    except ApiException as e:
        print(f"Fallo al enviar SMS: {e}")

if __name__ == "__main__":
    to = input("Introduce el número de teléfono (incluyendo el código de país, ej. +51955084718): ")
    body = input("Introduce el mensaje que deseas enviar: ")
    send_sms(to, body)
