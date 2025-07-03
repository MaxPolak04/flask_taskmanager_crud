from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
STATIC_DIR = BASE_DIR / 'static'
UPLOADS_DIR = STATIC_DIR / 'uploads'


class Config:
    ADMIN_PASSWORD='Pa$$w0rd'
    # Connection to Container:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpass@db:3306/taskmanager'
    # Connection to localhost:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_app:Pa$$w0rd@localhost/task_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '88322916e7e590b9f5d43147bd2507ac5315b83cc5c1aaa5bc3aa8285f4c02c8'
    UPLOAD_FOLDER = str(UPLOADS_DIR)
