from flask import Blueprint, redirect, render_template, request, url_for
from CTFd.utils.decorators import admins_only

from CTFd.models import Challenges, db
from .models import Metadata
import json

plugin_bp = Blueprint('metadata', __name__, template_folder='templates', static_folder='static', static_url_path='/static/metadata')

def load_bp():

    @plugin_bp.route('/admin/metadata')
    @admins_only
    def metadata_list():
        q = request.args.get("q")
        field = request.args.get("field")
        filters = []

        if q:
            # The field exists as an exposed column
            if Challenges.__mapper__.has_property(field):
                filters.append(getattr(Challenges, field).like("%{}%".format(q)))

        query = Challenges.query.filter(*filters).order_by(Challenges.id.asc())
        challenges = query.all()
        total = query.count()

        for challenge in challenges:
            metadata = Metadata.query.filter_by(id=challenge.id).first()
            if metadata:
                challenge.metadata = metadata.value
            else:
                challenge.metadata = ""

        return render_template(
            "metadata_list.html",
            challenges=challenges,
            total=total,
            q=q,
            field=field,
        )

    @plugin_bp.route('/admin/metadata/<int:challenge_id>')
    @admins_only
    def metadata_detail(challenge_id):
        challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()
        metadata = Metadata.query.filter_by(id=challenge_id).first()
        if not metadata:
            # There is no metadata text for this challenge yet. Create it
            metadata = Metadata(id=challenge_id, value="")
            db.session.add(metadata)
            db.session.commit()
            db.session.flush()

        return render_template(
            "metadata.html",
            challenge=challenge,
            metadata=metadata,
        )

    @plugin_bp.route("/api/v1/metadata", methods = ['GET'])
    @admins_only
    def metadatas_api():
        metadata = Metadata.query.all()
        data = []
            for client in clients:
                data.append(metadata.json())
            if data:
                return {"success": True, "data": data}
            else:
                return {"success": False}

    @plugin_bp.route("/api/v1/metadata/<int:challenge_id>", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
    @admins_only
    def metadata_api(challenge_id):
        if request.method == 'GET':
            data = Metadata.query.filter(Metadata.id == challenge_id).first_or_404()
            if data:
                try:
                    return {"success": True, "data": {"id": data.id,
                                           "metadata": json.loads(data.value)}}
                except:
                    return {"success": True, "data": {"id": data.id,
                                           "metadata": data.value}}

            else:
                return {"success": False}
        elif request.method == 'DELETE':
            data = Metadata.query.filter_by(id=challenge_id).first_or_404()
            if data:
                db.session.delete(data)
                db.session.commit()
                db.session.flush()
                return {"success": True}
            else:
                return {"success": False}, 404
        elif request.method == 'PATCH':
            data = Metadata.query.filter_by(id=challenge_id).first()
            req = request.get_json()
            if not data:
                # There is no metadata text for this challenge yet. Create it
                data = Metadata(id=challenge_id, metadata="")
                db.session.add(data)
                db.session.commit()
                db.session.flush()
            if "metadata" in req:
                if type(req["metadata"]) == str:
                    data.value = req["metadata"]
                else:
                    data.value = json.dumps(req["metadata"])
            db.session.commit()
            db.session.flush()
            try:
                return {"success": True, "data": {"id": data.id,
                                              "metadata": json.loads(data.value)}}
            except:
                return {"success": True, "data": {"id": data.id,
                                              "metadata": data.value}}
        elif request.method == 'POST':
            data = Metadata.query.filter_by(id=challenge_id).first()
            req = request.get_json()
            if data:
                # Create element, but allow overwriting of existing elements
                db.session.delete(data)
            metadata = Metadata(id=challenge_id, metadata="")
            if "metadata" in req:
                if type(req["metadata"]) == str:
                    data.value = req["metadata"]
                else:
                    data.value = json.dumps(req["metadata"])
            db.session.commit()
            db.session.flush()
            try:
                return {"success": True, "data": {"id": data.id,
                                              "metadata": json.loads(data.value)}}
            except:
                return {"success": True, "data": {"id": data.id,
                                              "metadata": data.value}}
        else:
            return {"success": False, "errors": "Permission denied"}, 400

    return plugin_bp
