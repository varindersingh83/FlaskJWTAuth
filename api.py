from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwtAuth.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(500))
    password = db.Column(db.String(500))
    admin = db.Column(db.Boolean)


@app.route('/user', methods=['GET'])
def get_all_users():
    return ''


@app.route('/user/<user_id>', methods=['GET'])
def get_one_user():
    return ''

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print (data)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name = data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

@app.route('/user/<user_id>', methods=['PUT'])
def promote_user():
    return ''

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
    return ''


if __name__ == '__main__':
    app.run(debug=True)