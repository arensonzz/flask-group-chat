from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Markup
)
from werkzeug.security import check_password_hash, generate_password_hash

import logging
from app.db import get_db
from .auth import login_required, load_logged_in_user
from flask_socketio import emit, leave_room, join_room as flask_join_room
from . import socketio

# Uncomment following line to print DEBUG logs
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Chat is the root blueprint, no url_prefix specified
bp = Blueprint('chat', __name__)


# ROUTES
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
            flash("Room name is required.", "warning")
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
                message = Markup(f"Successfully created the room: <b>{room_name}</b>.")
                flash(message, "info")

    return render_template("chat/create_room.html")


@bp.route('/join-room', methods=('GET', 'POST'))
@login_required
def join_room():
    """Join a chat room."""
    if request.method == "POST":
        db = get_db()
        f = request.form

        # Form check
        if not f["room_name"]:
            flash("Room name is required.", "warning")
        else:
            room_name = f["room_name"].strip().lower()
            room = db.execute("""SELECT chat_room_id, password FROM chat_room
                    WHERE name = ?""", (room_name,)).fetchone()

            if room is None:
                message = Markup(f"Could not find a room with the name <b>{room_name}</b>.")
                flash(message, "warning")
            elif not check_password_hash(room["password"], f["password"]):
                flash("Wrong password.", "warning")
            # Correct inputs, redirect to chat_room route
            else:
                room_id = room["chat_room_id"]
                session["room_id"] = room_id
                return redirect(url_for("chat.live_chat", chat_room_id=room_id))

    return render_template("chat/join_room.html")


@bp.route('/live-chat/<int:chat_room_id>', methods=('GET', 'POST'))
@login_required
def live_chat(chat_room_id):
    if "room_id" not in session or session["room_id"] != chat_room_id:
        flash("Unauthorized access to the room. Please enter the password.", "warning")
        return redirect(url_for("chat.join_room"))
    db = get_db()
    room = db.execute("""SELECT * FROM chat_room
            WHERE chat_room_id = ?""", (chat_room_id,)).fetchone()

    if request.method == "POST":
        pass

    # GET Request
    if room is None:
        flash("The owner closed this room.", "warning")
        return redirect("chat.join_room")

    return render_template("chat/live_chat.html", room=room)


# SocketIO Events

@socketio.on('connect', namespace="/live-chat")
def test_connect():
    """Test SocketIO connection by passing message between server and client."""
    logging.debug("SocketIO: Connected to client")


@socketio.on('joined', namespace="/live-chat")
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    if "room_id" not in session:
        return

    room = session["room_id"]
    user = load_logged_in_user()
    flask_join_room(room)

    logging.debug("### on joined")
    emit('status', {'msg': user["short_name"] + ' has entered the room.'}, room=room)


@socketio.on('message', namespace="/live-chat")
def chat_message(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    if "room_id" not in session:
        return

    room = session["room_id"]
    user = load_logged_in_user()

    logging.debug("### on message")
    emit('message', {'user': user["short_name"], 'msg': message['msg']}, room=room)


@socketio.on('left', namespace="/live-chat")
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session['room_id']
    # Revoke access rights to room
    session.pop("room_id")
    user = load_logged_in_user()

    leave_room(room)
    logging.debug("### on left")
    emit('status', {'user': user["short_name"], 'msg': ' has left the room.'}, room=room)
