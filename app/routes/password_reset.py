# password_reset.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from services.mail_service import send_reset_email
from crud.users import get_user_by_email, update_user_password
from app.forms import RequestResetForm, ResetPasswordForm

password_reset_bp = Blueprint('password_reset', __name__)

@password_reset_bp.route('/password_reset/request_reset', methods=['GET', 'POST'])
def request_reset():
    form = RequestResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = get_user_by_email(email)
        if user:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(email, salt='password-reset-salt')
            reset_link = url_for('password_reset.reset_token', token=token, _external=True)
            print(f"Generated reset link: {reset_link}")
            send_reset_email(email, reset_link)
            flash('Se ha enviado un correo electrónico para restablecer la contraseña.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Correo electrónico no encontrado.', 'error')
    return render_template('auth/request_reset.html', form=form)

@password_reset_bp.route('/password_reset/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    form = ResetPasswordForm()
    try:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadSignature):
        flash('El enlace de restablecimiento de contraseña es inválido o ha expirado.', 'error')
        return redirect(url_for('password_reset.request_reset'))

    if form.validate_on_submit():
        password = form.password.data
        update_user_password(email, password)
        flash('Tu contraseña ha sido actualizada.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form, token=token)
