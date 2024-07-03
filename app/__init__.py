from flask import Flask, render_template
from flask_mail import Mail
from config import Config
from flask_login import LoginManager
from models import User

mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mail.init_app(app)
    login_manager.init_app(app)

    from app.routes.user import user_bp
    from app.routes.auth_bp import auth_bp
    from app.routes.password_reset import password_reset_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(password_reset_bp)
    
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.errorhandler(404)
    def page_not_found(e):
        print("404 Error - Página no encontrada")
        return render_template('error/404.html'), 404
    
    @app.route('/')
    def home():
        return render_template('inicio/inicio.html')
    
    @app.route('/productos')
    def productos():
        return render_template('productos/productos.html')
    
    @app.route('/ropa')
    def ropa():
        return render_template('ropa/ropa.html')
    
    @app.route('/bebidas')
    def bebidas():
        return render_template('bebidas/bebidas.html')
    
    @app.route('/juguetes')
    def juguetes():
        return render_template('juguetes/juguetes.html')
    
    @app.route('/salud')
    def salud():
        return render_template('salud/salud.html')
    
    @app.route('/productos/<string:producto_nombre>')
    def producto_detalle(producto_nombre):
        # Aquí puedes agregar lógica para obtener los detalles del producto desde la base de datos si es necesario
        return render_template(f'/productos/detalle_{producto_nombre}.html')


    return app