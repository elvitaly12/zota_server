
from flask import Flask, request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy.sql import functions


from config import bot_key ,postgres_connection_string

from flask import current_app, flash, jsonify, make_response, redirect, request, url_for

import rncryptor
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_connection_string
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True,)
# cors = CORS(app, resources={r"/api/*": {"Access-Control-Allow-Origin": "*"}})
cors = CORS()
cors.init_app(app)
ma = Marshmallow(app)

# FLASK_APP= 'app.py'
# db.create_all()




def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response





class NewOrder(db.Model):
    Key = db.Column(db.String(30), primary_key=True)
    FirstName = db.Column(db.String(30), primary_key=False)
    LastName = db.Column(db.String(30), primary_key=False)
    EmailAdress = db.Column(db.String(30), primary_key=False)
    HomeAdress = db.Column(db.String(30), primary_key=False)
    NumberOfPizzas = db.Column(db.Integer, nullable=False)
    approved = db.Column(db.Boolean, nullable=False)

    def __init__(self, first, last, email,home,number,isapproved):
        self.FirstName = first
        self.LastName = last
        self.EmailAdress = email
        self.HomeAdress = home
        self.NumberOfPizzas = number
        self.approved = isapproved

    def __repr__(self):
        # return '<User %r>' % self.username
        return "<Users(FirstName='{}', LastName={}, EmailAdress={},HomeAdress={},NumberOfPizzas={},approved={})>" \
            .format(self.FirstName, self.LastName, self.EmailAdress,self.HomeAdress,self.NumberOfPizzas,self.NumberOfPizzas,self.approved)

    def add_neworder(first, last,email,home,num,isapproved ,db_input):
        new_order = NewOrder(first, last,email,home,num,isapproved)
        db_input.session.add(new_order)
        db_input.session.commit()



@app.errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404


@app.errorhandler(500)
def internal_error(e):
    print(e)
    return "500 Internal Server Error"

@app.route('/total_income', methods=['GET'])  # from ui recieve question_name and poll_name return all answers
def total_income():
    try:
        cursor = db.session.query(
            functions.sum(NewOrder.NumberOfPizzas).filter_by(
            isapproved=True))
        total_pizzas = cursor.scalar()
        return total_pizzas
    except:
        return Response('Internal Server Error', status=500)

@app.route('/not_approved', methods=['GET'])  # from ui recieve question_name and poll_name return all answers
def not_approved():
    try:
        cursor = db.session.query(
            functions.count(NewOrder.NumberOfPizzas).filter_by(
            isapproved=False))
        total_pizzas = cursor.scalar()
        return total_pizzas
    except:
        return Response('Internal Server Error', status=500)

@app.route('/approved_orders', methods=['GET'])  # from ui recieve question_name and poll_name return all answers
def aprrvoed():
    try:
        cursor = db.session.query(
            functions.count(NewOrder.NumberOfPizzas).filter_by(
            isapproved=True))
        total_pizzas = cursor.scalar()
        return total_pizzas
    except:
        return Response('Internal Server Error', status=500)


@app.route('/add_order', methods=['GET','POST'])  # from ui recieve question_name and poll_name return all answers
def add_order():

    try:
        print("fdfdsfdsfdsfds")
        FirstName = request.headers.get('FirstName')
        # print('admin_user_name', admin_user_name)
        LastName = request.headers.get('LastName')
        EmailAdress = request.headers.get('EmailAdress')
        HomeAdress = request.headers.get('HomeAdress')
        NumOfPizzas = request.headers.get('NumOfPizzas')
        # NewOrder.add_neworder(FirstName, LastName,EmailAdress,HomeAdress,NumOfPizzas, db)
        return Response('OK', status=200)
    except:
        return Response('Internal Server Error', status=500)

















