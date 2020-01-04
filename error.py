from flask import render_template
from flaskr import wapp

@wapp.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', msg="404 error")

@wapp.errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template('error.html', msg="500 error")
