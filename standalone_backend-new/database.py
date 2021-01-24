import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from main import app, db

# 配置数据库地址
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
# 跟踪数据库修改，不建议开启，消耗性能
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 数据库模型需要继承db.Model

# Yunan: add aws_id for access aws use only

class Customer(db.Model):
    # 定以表名
    __tablename__ = 'customer'
    # 定以字段
    # db.Column表示一个字段

    id = db.Column(db.String(50), primary_key=True)
    aws_id = db.Column(db.String(50),nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    expire_date = db.Column(db.String(10), nullable=False)
    payment_cnt = db.Column(db.Integer(), nullable=True)
    reg_image_cnt = db.Column(db.Integer(), nullable=True)

class Merchant(db.Model):
    # 定以表名
    __tablename__ = 'merchant'
    # 定以字段
    # db.Column表示一个字段

    id = db.Column(db.String(50), primary_key=True)
    aws_id = db.Column(db.String(50),nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    #phone_number = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    shop_name = db.Column(db.String(50), unique=False, nullable=False)

class Transaction(db.Model):

   __tablename__ = 'Transaction'
   
   trans_id = db.Column(db.String(50),primary_key=True)
   date_time = db.Column(db.DateTime, nullable = False)
   amount = db.Column(db.Float, nullable = False)
   customer_id = db.Column(db.String(50), db.ForeignKey('Customers.id'))
   Merchant_id = db.Column(db.String(50), db.ForeignKey('Merchants.id'))
   customer = db.relationship(Customer)
   merchant = db.relationship(Merchant)