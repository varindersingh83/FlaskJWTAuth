from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwtAuth.db'

db = SQLAlchemy(app)

#create db schema
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(500))
    password = db.Column(db.String(500))
    admin = db.Column(db.Boolean)



#API route to get all users. 
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data={}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})




#API route to get one users by public_id. 
@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'user not found'})

    user_data={}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({ 'user': user_data})




#API route to create a user by JSON. 
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print (data)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), name = data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


#route to update user info - change admin role
@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'user not found'})

    user.admin = True
    db.session.commit()
    return jsonify({'message': 'user has been promoted'})



#route to delete a user from table
@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'user not found'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user has been deleted!!!!'})

#add authentication
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify1', 401, {'WWW-Authenticate' : 'Basic realm="Login required!1"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify username', 401, {'WWW-Authenticate' : 'Basic realm="Login username required!"'})

    print(user.password)
    print(user.name)
    print(auth.password)
    print(check_password_hash(user.password, auth.password))

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    #{
    #   "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxOTZjMzRmNi00Yjc4LTRmMjAtODQxZC1iZDcxMzcyYjZjNTIiLCJleHAiOjE1NzQzODE1MDN9.1XnGYknYd2wlFKsn2PaZ_n7ltE8szog-FUgTddtYiwY"
    # }
    return make_response('Could not verify3', 401, {'WWW-Authenticate' : 'Basic realm="Login required!3"'})

if __name__ == '__main__':
    app.run(debug=True)