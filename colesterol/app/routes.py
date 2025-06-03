from flask import Blueprint, current_app, render_template, request, jsonify, send_from_directory
import os
from .models import db, Game

games_bp = Blueprint('games', __name__)

@games_bp.route('/')
def home():
    return render_template('index.html')

@games_bp.route("/login")
def login():
    return render_template("login.html")

@games_bp.route("/citas")
def citas():
    return render_template("citas.html")

@games_bp.route("/agregardoc")
def agregardoc():
    return render_template("agregardoc.html")

@games_bp.route("/historialcl")
def historialcl():
    return render_template("historialcl.html")

@games_bp.route('/games', methods=['GET'])
def obtener_juegos():
    juegos = Game.query.all()
    data = [
        {
            'id': j.id,
            'nombre': j.nombre,
            'categoria': j.categoria,
            'descripcion': j.descripcion,   
            'archivo_pck': j.archivo_pck,
            'archivo_html': j.archivo_html,
            'icono': j.icono,
            'archivo_js': j.archivo_js,
            'archivo_worker_js': j.archivo_worker_js,
            'archivo_worklet_js': j.archivo_worklet_js
        }
        for j in juegos
    ]
    return jsonify(data)

@games_bp.route('/uploads/<path:filename>')
def descargar_archivo(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {filename}")
        return jsonify({'error': f'El archivo {filename} no se encontró en el servidor.'}), 404

@games_bp.route('/games', methods=['POST'])
def crear_juego():
    data = request.form
    file = request.files.get('gameFile')

    if not file:
        return jsonify({'error': 'No se subió ningún archivo'}), 400

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    relative_file_path = f'uploads/{file.filename}'

    nuevo_juego = Game(
        nombre=data['gameName'],
        categoria=data['category'],
        descripcion=data.get('description', ''),
        file_path=relative_file_path
    )
    db.session.add(nuevo_juego)
    db.session.commit()

    return jsonify({'mensaje': 'Juego creado exitosamente', 'id': nuevo_juego.id}), 201

@games_bp.route('/games/<int:id>', methods=['PUT'])
def actualizar_juego(id):
    data = request.json
    juego = Game.query.get(id)

    if juego:
        juego.nombre = data.get('nombre', juego.nombre)
        juego.categoria = data.get('categoria', juego.categoria)
        juego.descripcion = data.get('descripcion', juego.descripcion)
        juego.archivo_pck = data.get('nombre', juego.archivo_pck)
        juego.archivo_html = data.get('categoria', juego.archivo_html)
        juego.icono = data.get('descripcion', juego.icono)
        juego.archivo_js = data.get('archivo_js', juego.archivo_js)
        juego.archivo_worker_js = data.get('archivo_worker_js', juego.archivo_worker_js)
        juego.archivo_worklet_js = data.get('archivo_worklet_js', juego.archivo_worklet_js)
        
        db.session.commit()
        return jsonify({'mensaje': 'Juego actualizado'}), 200

    return jsonify({'error': 'Juego no encontrado'}), 404

@games_bp.route('/games/<int:id>', methods=['DELETE'])
def eliminar_juego(id):
    juego = Game.query.get(id)

    if juego:
        db.session.delete(juego)
        db.session.commit()
        return jsonify({'mensaje': 'Juego eliminado'}), 200

    return jsonify({'error': 'Juego no encontrado'}), 404
