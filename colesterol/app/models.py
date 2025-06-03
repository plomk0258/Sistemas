from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    archivo_pck = db.Column(db.String(255), nullable=False)
    archivo_html = db.Column(db.String(255), nullable=False)
    icono = db.Column(db.String(255), nullable=False)
    archivo_js = db.Column(db.String(255), nullable=False)
    archivo_worker_js = db.Column(db.String(255), nullable=False)
    archivo_worklet_js = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=db.func.current_timestamp())