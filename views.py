from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from forms import RecordForm
from models import Record
from key import get_secret_key

app = Flask(__name__)
app.secret_key = get_secret_key()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def RecordList():
    all_record = db.session.query(Record).order_by(Record.register_time.desc()).all()
    return render_template('recordList.html', records=all_record)


@app.route('/record/new/', methods=['GET', 'POST'])
def RecordNew():
    print(request.method)
    if request.method == 'POST':
        form = RecordForm(request.form)
        if form.validate():
            record = Record(request.form['name'], request.form['surname'], request.form['phone_number'])
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('recordDetail', id=record.id))
    else:
        form = RecordForm()
    return render_template('recordEdit.html', form=form)


@app.route('/record/<int:id>/detail/', methods=['GET'])
def recordDetail(id):
    record = db.session.query(Record).filter_by(id=id).first()
    return render_template('recordDetail.html', record=record)


@app.route('/record/<int:id>/edit/', methods=['GET', 'POST'])
def recordEdit(id):
    record = db.session.query(Record).filter_by(id=id).first()
    if request.method == 'POST':
        form = RecordForm(request.form)
        if form.validate():
            db.session.query(Record).filter_by(id=id).update({
                'name': request.form['name'],
                'surname': request.form['surname'],
                'phone_number': request.form['phone_number']
            })
            db.session.commit()
            return redirect(url_for('recordDetail', id=record.id))
    else:
        form = RecordForm(obj=record)
    return render_template('recordEdit.html', form=form)


@app.route('/record/<int:id>/delete/', methods=['POST'])
def recordDelete(id):
    record = db.session.query(Record).filter_by(id=id).first()
    if record:
        db.session.delete(record)
        db.session.commit()
        return redirect('/', code=200)
