from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity, jwt_required
from datetime import timedelta
import json

from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para registrar un nuevo usuario"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        is_moderator = data.get('is_moderator') == 'on'

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="El usuario ya existe")

        new_user = User(username=username, is_moderator=is_moderator)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login_page'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """Ruta para iniciar sesión y generar un token JWT almacenado en cookies"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            user_identity = json.dumps({"id": user.id, "is_moderator": user.is_moderator})
            token = create_access_token(identity=user_identity, expires_delta=timedelta(hours=1))

            response = make_response(redirect(url_for('main.dashboard')))
            response.set_cookie('access_token_cookie', token, httponly=True)
            return response
        else:
            return render_template('login.html', error="Credenciales incorrectas")

    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Ruta para cerrar sesión eliminando la cookie JWT"""
    response = make_response(redirect(url_for('main.index')))
    unset_jwt_cookies(response)
    return response


