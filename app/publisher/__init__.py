"""Publisher blueprint."""
from flask import Blueprint

bp = Blueprint('publisher', __name__)

from app.publisher import routes

