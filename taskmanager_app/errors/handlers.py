from . import errors_bp
from flask import render_template


@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


# @errors_bp.app_errorhandler(Exception)
# def handle_exception(error):
#     return render_template("errors/500.html", error=error), 500
