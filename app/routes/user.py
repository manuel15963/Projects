from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from crud.users import get_users, add_user_to_db, get_user_by_id, update_user_in_db, deactivate_user_in_db, activate_user_in_db
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.before_request
def before_request():
    if not current_user.is_authenticated:
        print("Acceso no autenticado detectado, abortando con 404")
        abort(404)

@user_bp.route('/')
@login_required
def index():
    print("Ruta /users/ index accesada")
    filter_status = request.args.get('status', 'active')
    users = get_users(filter_status)
    return render_template('user/user.html', users=users, filter_status=filter_status)

@user_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    print("Ruta /users/add accesada")
    if request.method == 'POST':
        username = request.form['username']
        last_name = request.form['last_name']
        doc = request.form['doc']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        add_user_to_db(username, last_name, doc, email, phone, password)
        flash('User added successfully!')
        return redirect(url_for('user.index'))
    return render_template('user/add_user.html')

@user_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    print(f"Ruta /users/edit/{id} accesada")
    user = get_user_by_id(id)
    if request.method == 'POST':
        username = request.form['username']
        last_name = request.form['last_name']
        doc = request.form['doc']
        email = request.form['email']
        phone = request.form['phone']
        update_user_in_db(id, username, last_name, doc, email, phone)
        flash('User updated successfully!')
        return redirect(url_for('user.index'))
    return render_template('user/edit_user.html', user=user)

@user_bp.route('/delete/<int:id>')
@login_required
def delete_user(id):
    print(f"Ruta /users/delete/{id} accesada")
    deactivate_user_in_db(id)
    flash('User deactivated successfully!')
    return redirect(url_for('user.index'))

@user_bp.route('/restore/<int:id>')
@login_required
def restore_user(id):
    print(f"Ruta /users/restore/{id} accesada")
    activate_user_in_db(id)
    flash('User restored successfully!')
    return redirect(url_for('user.index'))

@user_bp.route('/<path:invalid_path>')
def handle_invalid_path(invalid_path):
    print(f"Ruta invalida accesada: /users/{invalid_path}")
    abort(404)
