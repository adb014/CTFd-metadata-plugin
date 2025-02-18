from CTFd.models import db
from CTFd.utils import get_app_config

class Metadata(db.Model):
    __tablename__ = "metadata"

    id = db.Column(db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True)
    value = db.Column(db.Text)

    def json(self):
        return {'id': self.id,
                'value': self.value}

