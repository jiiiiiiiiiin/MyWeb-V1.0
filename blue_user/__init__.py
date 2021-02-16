from flask import Blueprint

user_blue = Blueprint('user', __name__)

from blue_user import view
