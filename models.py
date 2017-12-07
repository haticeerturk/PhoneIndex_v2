import flask
import flask_sqlalchemy
import flask_restless
import datetime

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = flask_sqlalchemy.SQLAlchemy(app)

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    phone_number = db.Column(db.String(11))
    register_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, data):
        self.name = data['name']
        self.surname = data['surname']
        self.phone_number = data['phone_number']

db.create_all()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Record, methods=['GET', 'POST', 'DELETE', 'PATCH'])
