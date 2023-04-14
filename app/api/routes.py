from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Notepad, contact_schema, contacts_schema



api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}
    
@api.route('/notepad', methods = ['POST'])
@token_required
def create_notepad(current_user_token):
    date = request.json['Date']
    note = request.json['Note']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    notepad = Notepad(date, note, user_token=user_token)

    db.session.add(notepad)
    db.session.commit()

    response = contact_schema.dump(notepad)
    return jsonify(response) 

@api.route('/notepad', methods = ['GET'])
@token_required
def get_notepad(current_user_token):
    a_user = current_user_token.token
    notepad = Notepad.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(notepad)
    return jsonify(response)

@api.route('/notepad/<id>', methods = ['GET'])
@token_required
def get_single_notepad(current_user_token, id):
    notepad = Notepad.query.get(id)
    response = contact_schema.dump(notepad)
    return jsonify(response)

@api.route('/notepad/<id>', methods = ['POST', 'PUT'])
@token_required
def update_notepad(current_user_token, id):
    notepad = Notepad.query.get(id)
    notepad.date = request.json['Date']
    notepad.note = request.json['Note']
    notepad.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(notepad)
    return jsonify(response)

@api.route('/notepad/<id>', methods = ['DELETE'])
@token_required
def delete_notepad(current_user_token, id):
    notepad = Notepad.query.get(id)
    db.session.delete(notepad)
    db.session.commit()
    response = contact_schema.dump(notepad)
    return jsonify(response)