import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_llave_secreta_muy_segura'
    DATABASE_CONFIG = {
        'dbname': 'tienda_don_italo',
        'user': 'postgres',
        'password': '123software',
        'host': 'localhost',
        'port': 5432
    }
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    CLICK_SEND_USERNAME = os.environ.get('CLICK_SEND_USERNAME')
    CLICK_SEND_API_KEY = os.environ.get('CLICK_SEND_API_KEY')