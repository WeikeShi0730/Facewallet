import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from main import app, db, db_url
import datetime
# 配置数据库地址
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
# 跟踪数据库修改，不建议开启，消耗性能
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 数据库模型需要继承db.Model

# Yunan: add aws_id for access aws use only

class Customer(db.Model):
    # 定以表名
    __tablename__ = 'Customers'
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
    sec_verify = db.Column(db.Boolean(), nullable=False, default=True)
    balance = db.Column(db.Float(),nullable=False)
    #transactions = db.relationship('Transaction')
    
class Merchant(db.Model):
    # 定以表名
    __tablename__ = 'Merchants'
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
    balance = db.Column(db.Float(),nullable=False)
    #transactions = db.relationship('Transaction')

class Transaction(db.Model):

   __tablename__ = 'Transaction'
   
   trans_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
   amount = db.Column(db.Float, nullable = False)
   customer_id = db.Column(db.String(50), db.ForeignKey('Customers.id'))
   merchant_id = db.Column(db.String(50), db.ForeignKey('Merchants.id'))
   customer = db.relationship(Customer)
   merchant = db.relationship(Merchant)

def reset_db_with_some_initials():
    if ("amazonaws" not in db_url):
        # 删除表
        db.drop_all()
        # 创建表
        db.create_all()
        customer1=Customer(
            id='1234567890',
            first_name='test',
            last_name='test',
            email='test@123.ca',
            password='123',
            phone_number='1234567890',
            card_number='1234123412341234',
            cvv='123',
            expire_date='0922',
            sec_verify=False,
            balance=100
            )
        merchant1 = Merchant(
            id='1234567890',
            first_name='test',
            last_name='test',
            email='test@123.ca',
            password='123',
            shop_name='cap',
            balance = 100
        )
        transaction1 = Transaction(
            # trans_id = 1,
            amount = 12,
            customer_id = '1234567890',
            merchant_id = '1234567890'
        )
        transaction2 = Transaction(
            # trans_id = 2,
            amount = 34,
            customer_id = '1234567890',
            merchant_id = '1234567890'
        )
        db.session.add_all([customer1,merchant1,transaction1,transaction2])
        # db.session.add_all([customer1,merchant1,transaction1])
        db.session.commit()
        print ("init db is okay")
        print ("dummy print to preserve if statement")