import functools
import logging

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


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
                db.execute("""INSERT INTO USER (password, email_address, full_name, short_name)
                    VALUES (?, ?, ?, ?)""",
                           (generate_password_hash(f["password"]), f["email"], f["full_name"], f["short_name"]))
                db.commit()
            except db.IntegrityError:
                flash(f"User with the email address \"{f['email']}\" is already registered.")
            else:
                return redirect(url_for("auth.login"))

    return render_template('auth/register.html', errors=errors)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in user by adding to session."""
    errors = {}
    if request.method == 'POST':
        f = request.form
        db = get_db()
        is_bad_login = False
        errors = {}

        if not f["email"]:
            errors["email"] = "Email address is required"

        if not f["password"]:
            errors["password"] = "Password is required"

        if not errors:
            user = db.execute("""SELECT user_id, email_address, password FROM user 
                    WHERE email_address = ?""", (f["email"],)).fetchone()

            if user is None:
                is_bad_login = True
                logging.debug("Provided email address do not exist in the `user` table")
            elif not check_password_hash(user["password"], f["password"]):
                is_bad_login = True
                logging.debug("Password is incorrect")

            if is_bad_login:
                flash("Email address or password is incorrect.")
            elif not errors:
                # Add the user info to session
                # User stays logged in this way
                session.clear()
                session["user_id"] = user["user_id"]
                return redirect(url_for("chat.index"))
    return render_template('auth/login.html', errors=errors)


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    """Log out user by removing info from session."""
    return "Logout page."
