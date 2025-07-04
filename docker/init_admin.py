from taskmanager_app import create_app, db
from taskmanager_app.utils import create_admin_if_missing

app = create_app()

with app.app_context():
    create_admin_if_missing()
