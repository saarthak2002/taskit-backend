from app import app, db
from flask import jsonify, request
from app.models import UserInfo

@app.route('/', methods=['GET'])
def index():
    return "Hello, world!"

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        user_list = []
        users = UserInfo.query.all()
        for user in users:
            user_list.append(UserInfo.serialize(user))
        return jsonify(user_list)
    
    elif request.method == 'POST':
        data = request.get_json()
        user_uid = data.get('userUID')
        username = data.get('username')
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        existing_user = UserInfo.query.filter_by(userUID=user_uid).first()
        if existing_user:
            return jsonify({'error': 'User with the same userUID already exists'})
        
        existing_user = UserInfo.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'User with the same username already exists'})

        new_user = UserInfo(
            userUID=user_uid,
            username=username,
            firstName=first_name,
            lastname=last_name
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'New user created successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/users/<user_uid>', methods=['GET'])
def get_user_info_by_uid(user_uid):
    user = UserInfo.query.filter_by(userUID=user_uid).first()
    if user:
        return jsonify(UserInfo.serialize(user))
    else:
        return jsonify({'error': 'User not found'})
