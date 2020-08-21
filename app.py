import os
from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
#from functools import wraps
#from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask_jwt_extended import JWTManager
from werkzeug.security import safe_str_cmp

import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'assembler'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

app.config['JWT_SECRET_KEY'] = 'jose'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)

########### MODELS ##########


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50),  nullable=False)
    password = db.Column(db.Text, nullable=False)
    expense = db.relationship(
        'Expense', backref='user', lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f" Name is : {self.name}"


class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)


### API's ###
class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        user = User(
            name=data['name'], username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username = data['username']).first()
        print(user.password)
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, expires_delta = datetime.timedelta(minutes=30))
            #refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'id':user.id
            }, 200
        return {"message": 'Invalid credentials'}, 401

class UserExpense(Resource):

    @jwt_required
    def post(self, user_id):
        data = request.get_json()
        expense = Expense(user_id=user_id,
                          description=data['description'], amount=data['amount'], type=data['type'])
        db.session.add(expense)
        db.session.commit()

        return {'message': 'Expense added successfully'}

    @jwt_required
    def get(self, user_id):
        expense = Expense.query.filter_by(user_id=user_id).all()
        expense_data = []
        print(expense)
        if not (expense):
            return {"message": 'What are you doing?'}

        for i in range(len(expense)):
            expense_data.append({'description': expense[i].description,
                                 'amount': expense[i].amount,
                                 'type': expense[i].type})

        return {'data': expense_data}

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.append(jti)
        return {"message": "Successfully logged out"}, 200

class GetAllExpenses(Resource):

    @jwt_required
    def get(self):
        expense_list = Expense.query.all()
        expense_data = []
        print(expense_list)
        if not (expense_list):
            return {"message": 'What are you doing?'}

        for i in range(len(expense_list)):
            expense_data.append({'description': expense_list[i].description,
                                 'amount': expense_list[i].amount,
                                 'type': expense_list[i].type})

        return {'data': expense_data}



@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


# @jwt.needs_fresh_token_loader
# def token_not_fresh_callback():
#     return jsonify({
#         "description": "The token is not fresh.",
#         'error': 'fresh_token_required'
#     }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


BLACKLIST = []

@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)
api.add_resource(UserExpense, "/<int:user_id>")
api.add_resource(GetAllExpenses, "/getAll")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    app.run(debug=True)
