from flask import Flask, request, redirect, url_for, jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from forms import RecordForm
from models import Record
from key import get_secret_key
import json
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.secret_key = get_secret_key()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)
api = Api(app)

def convert_to_json(object):
    json = {
        'id': object.id,
        'name': object.name,
        'surname': object.surname,
        'phone_number': object.phone_number,
        'register_time': object.register_time
    }
    return json


class RecordList(Resource):
    def get(self):
        all_record = db.session.query(Record).order_by(Record.register_time.desc()).all()
        if all_record:
            record = []
            for r in all_record:
                record.append(convert_to_json(r))
            return jsonify(record)
        else:
            return {'message': 'Not yet a record.'}


class RecordNew(Resource):
    def post(self):
        record_json = json.loads(request.data.decode('utf-8'))
        record = Record(record_json)
        db.session.add(record)
        db.session.commit()
        return record_json


class RecordDetail(Resource):
    def get(self, id):
        record = db.session.query(Record).filter_by(id=id).first()
        if record:
            record_json = convert_to_json(record)
            return jsonify(record_json)
        else:
            return {'message': 'Record Not Found.'}, 404


class RecordEdit(Resource):
    def patch(self, id):
        data = json.loads(request.data.decode('utf-8'))
        record = db.session.query(Record).filter_by(id=id).first()
        if record:
            db.session.query(Record).filter_by(id=id).update({
                'name': data['name'],
                'surname': data['surname'],
                'phone_number': data['phone_number']
            })
            db.session.commit()
            return {'message': 'Success'}, 200
        else:
            return {'message': 'Record Not Found.'}, 404


class RecordDelete(Resource):
    def delete(self, id):
        record = db.session.query(Record).filter_by(id=id).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'message': 'Success'}, 200
        else:
            return {'message': 'Record Not Found.'}, 404

api.add_resource(RecordList, '/')
api.add_resource(RecordNew, '/record/new/')
api.add_resource(RecordDetail, '/record/<int:id>/detail/')
api.add_resource(RecordEdit, '/record/<int:id>/edit/')
api.add_resource(RecordDelete, '/record/<int:id>/delete/')
