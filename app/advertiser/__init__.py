"""Advertiser blueprint."""
from flask import Blueprint

bp = Blueprint('advertiser', __name__)

from app.advertiser import routes

