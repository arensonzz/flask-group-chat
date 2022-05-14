import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register user to database."""
    errors = {}
    if request.method == 'POST':
        f = request.form
        db = get_db()

        if not f["email"]:
            errors["email"] = "Email address is required"

        if not f["password"]:
            errors["password"] = "Password is required"
        elif f["password"] != f["confirmation"]:
            errors["confirmation"] = "Passwords do not match"

        if not f["short_name"]:
            errors["short_name"] = "Short name is required for profile"

        if not errors:
            try:
                db.execute("""INSERT INTO """)

            except db.IntegrityError:
                flash(f"User {f['email']} is already registered.")
            else:
                return redirect(url_for("auth.login"))

    return render_template('auth/register.html', errors=errors)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    return "Login page."


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    return "Logout page."
