from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'


class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATA_DIR / "todo.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '88322916e7e590b9f5d43147bd2507ac5315b83cc5c1aaa5bc3aa8285f4c02c8'
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # maks 2MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
