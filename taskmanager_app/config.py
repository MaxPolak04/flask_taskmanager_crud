from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'
STATIC_DIR = BASE_DIR / 'static'
UPLOADS_DIR = STATIC_DIR / 'uploads'


class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATA_DIR / "todo.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '88322916e7e590b9f5d43147bd2507ac5315b83cc5c1aaa5bc3aa8285f4c02c8'
    UPLOAD_FOLDER = str(UPLOADS_DIR)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # maks 2MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
