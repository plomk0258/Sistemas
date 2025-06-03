from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()





def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5433/organigrama'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configurar la carpeta de uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    db.init_app(app)
    Migrate(app, db)

    from .routes import games_bp
    app.register_blueprint(games_bp)

    # Agregar encabezados necesarios para Godot
    @app.after_request
    def agregar_encabezados(response):
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response

    return app