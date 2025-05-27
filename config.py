from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'


class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATA_DIR / "todo.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'strongPassword'
