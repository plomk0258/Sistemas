import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5433/organigrama")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
