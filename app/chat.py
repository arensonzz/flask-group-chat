from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Markup
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from .auth import login_required

# Chat is the root blueprint, no url_prefix specified
bp = Blueprint('chat', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    """Display previously entered rooms. Display rooms created by logged in user."""

    # TODO
    # For now redirects to create_room page
    return redirect(url_for("chat.create_room"))


@bp.route('/create-room', methods=('GET', 'POST'))
@login_required
def create_room():
    """Create a unique chat room."""
    if request.method == "POST":
        db = get_db()
        has_error = False
        f = request.form

        if not f["room_name"]:
            flash("Room name is required", "warning")
            has_error = True

        room_name = f["room_name"].strip().lower()

        if not has_error:
            try:
                db.execute("""INSERT INTO chat_room (created_by_user, name, password, description)
                        VALUES (?, ?, ?, ?)""", (session["user_id"], room_name,
                                                 generate_password_hash(f["password"]),
                                                 f["description"].strip()))
                db.commit()
            except db.IntegrityError:
                message = Markup(f"A room with the name <b>{room_name}</b> already exists.")
                flash(message, "warning")
            else:
                message = Markup(f"Successfully created the room: <b>{room_name}</b>")
                flash(message, "info")

    return render_template("chat/create_room.html")


@bp.route('/join-room', methods=('GET', 'POST'))
@login_required
def join_room():
    """Join a chat room."""
    if request.method == "POST":
        db = get_db()
        has_error = False
        f = request.form

        if not f["room_name"]:
            flash("Room name is required", "warning")
            has_error = True

        room_name = f["room_name"].strip().lower()

        if not has_error:
            pass

    return render_template("chat/join_room.html")


@bp.route('/live-chat', methods=('GET', 'POST'))
@login_required
def live_chat():

    return "Chat page"
