from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from .models import Parking
from .models import Note
from .models import Arrival
#from flask_login import login_user, login_required, logout_user, current_user

from . import db
import json
import sqlite3 as sql
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short 😗!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/parking-registered', methods=['GET', 'POST'])
@login_required
def parking():
    if request.method == 'POST':
        name = request.form.get('name')
        name2 = request.form.get('name2')
        cp = request.form.get('cp')
        ttt = request.form.get('tel')
        cap = request.form.get('capacity')

        #user = User.query.filter_by(email=email).first()
        parking = Parking.query.filter_by(name=name).first()
        if parking:
            flash('Name already exists.', category='error')
        elif len(name) < 4:
            flash('Name must be greater than 3 characters.', category='error')
        elif len(cp) < 5:
            flash('C.P name must be greater than 5 character.', category='error')
        elif name != name2:
            flash('Name\'s don\'t match.', category='error')
        elif len(ttt) < 10:
            flash('Phone must be greater than 10 characters.', category='error')
        elif len(cap) < 0:
            flash('Capacity must be at least 0 characters.', category='error')
        else:
            new_parking = Parking(name=name, cp=cp, tel=ttt, cap=cap, user_id=current_user.id)
            db.session.add(new_parking)
            db.session.commit()
            flash('Parking created! 👌🏻', category='success')
            # return redirect(url_for('views.home'))

    return render_template("parking_registered.html", user=current_user)

@views.route('/arrival', methods=['GET', 'POST'])
@login_required
def arrival():
    if request.method == 'POST':
        name = request.form.get('name')
        name2 = request.form.get('name2')
        date = request.form.get('datein')
        time = request.form.get('timein')

        #user = User.query.filter_by(email=email).first()
        arrival = Arrival.query.filter_by(name=name).first()
        if arrival:
            flash('Name already exists.', category='error')
        elif len(name) < 4:
            flash('Name must be greater than 3 characters.', category='error')
        elif name != name2:
            flash('Name\'s don\'t match.', category='error')
        elif len(date) < 5:
            flash('Date name must be greater than 5 character.', category='error')
        elif len(time) < 4:
            flash('Time must be greater than 4 characters.', category='error')
        else:
            new_arrival = Arrival(name=name, date=date, time=time, user_id=current_user.id)
            db.session.add(new_arrival)
            db.session.commit()
            flash('Arrival registered! 👌🏻', category='success')

    return render_template("arrival.html", user=current_user)

@views.route('/exit', methods=['GET', 'POST'])
@login_required
def exit():
    return render_template("exit.html", user=current_user)

@views.route('/list-records', methods=['GET', 'POST'])
@login_required
def list():
    con =sql.connect("DB_SmartParking.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('SELECT * FROM Arrival')

    row = cur.fetchall();
    return render_template("list_records.html", rows=rows, user=current_user)