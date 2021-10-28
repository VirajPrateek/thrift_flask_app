from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from thrift.auth import login_required
from thrift.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    if g.user:
        return render_template('home.html')
    else:
        return render_template('landing.html')
