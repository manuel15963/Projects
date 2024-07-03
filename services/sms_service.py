import clicksend_client
from clicksend_client.rest import ApiException
from decouple import config

# Configurar el cliente ClickSend
username = config('CLICK_SEND_USERNAME')
api_key = config('CLICK_SEND_API_KEY')

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
        print(f"SMS sent successfully: {response}")
    except ApiException as e:
        print(f"Failed to send SMS: {e}")
