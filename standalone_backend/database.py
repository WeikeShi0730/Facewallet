import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from main import app,db

# 配置数据库地址
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
# 跟踪数据库修改，不建议开启，消耗性能 
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 数据库模型需要继承db.Model
class Customer(db.Model):
   # 定以表名
   __tablename__= 'customers'
   # 定以字段
   # db.Column表示一个字段
   id = db.Column(db.String(50),primary_key=True)
   first_name = db.Column(db.String(50),nullable=False)
   last_name=db.Column(db.String(50),nullable=False)
   phone_number=db.Column(db.String(15),nullable=False,unique=True)
   account_number=db.Column(db.String(16),nullable=False)
   account_cvv=db.Column(db.String(3),nullable=False)
   account_date=db.Column(db.String(4),nullable=False)
   email=db.Column(db.String(50),unique=True,nullable=True)
   payment_cnt=db.Column(db.Integer(),nullable=True)
   reg_image_cnt=db.Column(db.Integer(),nullable=True)

