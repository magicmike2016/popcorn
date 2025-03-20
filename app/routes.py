import os
import csv
import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Movie, Comment, User
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@main_bp.route('/catalogo')
def catalogo():
    """Muestra todas las películas disponibles"""
    movies = Movie.query.all()
    return render_template('catalogo.html', peliculas=movies)

@main_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """Ruta que muestra el panel de usuario o moderador después de iniciar sesión"""
    user_identity = get_jwt_identity()

    # Convertimos la cadena JSON a diccionario si es necesario
    if isinstance(user_identity, str):
        user_identity = json.loads(user_identity)

    user = User.query.get(user_identity["id"])

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    movies = Movie.query.all()

    if user.is_moderator:
        return render_template('moderator_dashboard.html', user=user, movies=movies)
    else:
        return render_template('user_dashboard.html', user=user, movies=movies)

@main_bp.route('/movies/<int:movie_id>/rate', methods=['POST'])
@jwt_required()
def rate_movie(movie_id):
    """Permite a los usuarios calificar una película"""
    user_identity = get_jwt_identity()
    
    if isinstance(user_identity, str):
        user_identity = json.loads(user_identity)

    user = User.query.get(user_identity["id"])
    
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Película no encontrada"}), 404

    rating = request.form.get('rating')
    try:
        rating = float(rating)
        if rating < 0 or rating > 10:
            return jsonify({"message": "La calificación debe estar entre 0 y 10"}), 400
    except ValueError:
        return jsonify({"message": "Calificación no válida"}), 400

    movie.rating = rating
    db.session.commit()

    return redirect(url_for('main.dashboard'))

@main_bp.route('/movies/<int:movie_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(movie_id):
    """Permite a los usuarios agregar comentarios a una película"""
    user_identity = get_jwt_identity()
    
    if isinstance(user_identity, str):
        user_identity = json.loads(user_identity)

    user = User.query.get(user_identity["id"])
    
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    content = request.form.get('content')
    if not content:
        return jsonify({"message": "El comentario no puede estar vacío"}), 400

    new_comment = Comment(content=content, user_id=user.id, movie_id=movie_id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('main.dashboard'))

@main_bp.route('/movies/rated', methods=['GET'])
@jwt_required()
def rated_movies():
    """Muestra las películas calificadas y su calificación promedio"""
    movies = Movie.query.filter(Movie.rating.isnot(None)).all()

    movies_data = [
        {
            "title": movie.title,
            "year": movie.year,
            "rating": movie.rating,
            "director": movie.director
        }
        for movie in movies
    ]

    return render_template('rated_movies.html', movies=movies_data)

@main_bp.route('/movies', methods=['POST'])
@jwt_required()
def add_movie():
    """Permite a los moderadores agregar una nueva película"""
    user_identity = get_jwt_identity()
    
    if isinstance(user_identity, str):
        user_identity = json.loads(user_identity)

    user = User.query.get(user_identity["id"])
    
    if not user or not user.is_moderator:
        return jsonify({"message": "Solo los moderadores pueden agregar películas"}), 403

    data = request.form
    new_movie = Movie(
        title=data.get('title'),
        description=data.get('description'),
        director=data.get('director'),
        year=int(data.get('year')) if data.get('year') else None,
        created_by=user.id
    )
    db.session.add(new_movie)
    db.session.commit()
    
    return redirect(url_for('main.dashboard'))

@main_bp.route('/movies/<int:movie_id>/delete', methods=['POST'])
@jwt_required()
def delete_movie(movie_id):
    """Permite a los moderadores eliminar una película"""
    user_identity = get_jwt_identity()
    
    if isinstance(user_identity, str):
        user_identity = json.loads(user_identity)

    user = User.query.get(user_identity["id"])
    
    if not user or not user.is_moderator:
        return jsonify({"message": "Solo los moderadores pueden eliminar películas"}), 403

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Película no encontrada"}), 404

    db.session.delete(movie)
    db.session.commit()
    
    return redirect(url_for('main.dashboard'))

def importar_datos():
    """Importa datos desde un archivo CSV a la base de datos"""
    ruta_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../imdb.csv')

    if not os.path.exists(ruta_csv):
        return {"message": "Archivo CSV no encontrado."}, 400

    if Movie.query.first():
        return {"message": "Los datos ya fueron importados previamente."}, 200

    with open(ruta_csv, encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        for fila in lector_csv:
            movie = Movie(
                title=fila.get('Title'),
                description=fila.get('Description'),
                director=fila.get('Director'),
                year=int(fila.get('Year')) if fila.get('Year') else None,
                created_by=1
            )
            db.session.add(movie)
        db.session.commit()
    
    return {"message": "Datos importados correctamente."}, 201

@main_bp.route('/importar', methods=['GET'])
def importar():
    """Ruta para importar datos desde un CSV"""
    resultado = importar_datos()
    return jsonify(resultado)






