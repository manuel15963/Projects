# auth_bp.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from crud.users import get_user_by_username, add_user_to_db
from services.sms_service import send_sms
from flask_login import login_user, logout_user, login_required
from models import User
from app.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_data = get_user_by_username(username)
        print(f"Intento de inicio de sesión con usuario: {username}")
        if user_data and check_password_hash(user_data['password'], password):
            user = User(id=user_data['id'], username=user_data['username'], email=user_data.get('email', ''))
            login_user(user)
            flash('Inicio de sesión exitoso')
            return redirect(url_for('user.index'))
        else:
            error = "Nombre de usuario o contraseña incorrectos"
            print("Nombre de usuario o contraseña incorrectos")
            flash('Nombre de usuario o contraseña incorrectos')
    return render_template('auth/login.html', form=form, error=error)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        last_name = form.last_name.data
        doc = form.doc.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data
        success, message = add_user_to_db(username, last_name, doc, email, phone, password)
        if success:
            # Enviar SMS
            send_sms(phone, 'Gracias por registrarte!')
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            return jsonify({"status": "error", "message": message})
    return render_template('user/add_user.html', form=form)
