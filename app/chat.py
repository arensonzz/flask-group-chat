import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/index', methods=('GET', 'POST'))
def index():
    """Display previously entered rooms. Display created rooms."""

    return "Index page."


@bp.route('/create_room', methods=('GET', 'POST'))
def create_room():

    return "Create room page."


@bp.route('/join_room', methods=('GET', 'POST'))
def join_room():

    return "Join room page."
