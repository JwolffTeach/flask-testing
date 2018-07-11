from flask import Blueprint

bp = Blueprint('valves', __name__)

from app.valves import routes