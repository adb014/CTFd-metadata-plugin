""" Plugin entry-point """
import json
import os

from CTFd.utils import get_app_config
from .blueprint import load_bp
from .models import Metadata

PLUGIN_PATH = os.path.dirname(__file__)
CONFIG = json.load(open("{}/config.json".format(PLUGIN_PATH)))

def load(app):
    # Create database tables
    app.db.create_all()

    # Register the blueprint containing the routes
    bp = load_bp()
    app.register_blueprint(bp)

