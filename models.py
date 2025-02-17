from CTFd.models import db
from CTFd.utils import get_app_config

class Metadata(db.Model):
    __tablename__ = "metadata"
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)

