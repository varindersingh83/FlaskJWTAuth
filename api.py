from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


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



@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'user not found'})

    user.admin = True
    db.session.commit()
    return jsonify({'message': 'user has been promoted'})

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user():
    return ''


if __name__ == '__main__':
    app.run(debug=True)