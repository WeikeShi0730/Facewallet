from flask import Flask, jsonify, request, json
import os
#Azure
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

sys.path.append('.')
import boto3
import constant

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'boost-is-the-secret-of-our-app'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
db_url = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt=JWTManager(app)
db=SQLAlchemy(app)

Region = os.environ['REGION_NAME']
Aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
Aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
Collection_id = os.environ['COLLECTION_ID']

client = boto3.client('rekognition', region_name=Region, aws_access_key_id=Aws_access_key_id, aws_secret_access_key=Aws_secret_access_key)



from routes import *
from database import *
if ("amazonaws" not in db_url):
    # # 删除表
    # db.drop_all()
    # # 创建表
    # db.create_all()
    # customer1=Customer(
    #     id='1234567890',
    #     first_name='test',
    #     last_name='test',
    #     email='123@123.ca',
    #     password='123',
    #     phone_number='1234567890',
    #     card_number='1234123412341234',
    #     cvv='123',
    #     expire_date='0922',
    #     sec_verify=False,
    #     balance=100
    #     )
    # merchant1 = Merchant(
    #     id='1234567890',
    #     first_name='test',
    #     last_name='test',
    #     email='123@123.ca',
    #     password='123',
    #     shop_name='cap',
    #     balance = 100
    # )
    # transaction1 = Transaction(
    #     # trans_id = 1,
    #     amount = 12,
    #     customer_id = '1234567890',
    #     merchant_id = '1234567890'
    # )
    # transaction2 = Transaction(
    #     # trans_id = 2,
    #     amount = 34,
    #     customer_id = '1234567890',
    #     merchant_id = '1234567890'
    # )
    # db.session.add_all([customer1,merchant1,transaction1,transaction2])
    # # db.session.add_all([customer1,merchant1,transaction1])
    # db.session.commit()
    # print ("init db is okay")
    print ("dummy print to preserve if statement")
    


# 添加用户
#customer1=Customer(id='400065323',first_name='Bohui',last_name='Yu',phone_number='6479365120',card_number='1234123412341234',cvv='123',expire_date='0922')
# customer2=Customer(id='400050636',first_name='Weike',last_name='Shi',phone_number='647936666',card_number='1234123412341234',cvv='456',expire_date='0922')
# customer3=Customer(id='400099173',first_name='Haolin',last_name='Ma',phone_number='6479365555',card_number='1234123412341234',cvv='123',expire_date='0922')
# customer4=Customer(id='400104626',first_name='Yunan',last_name='Zhou',phone_number='6479365111',card_number='1234123412341234',cvv='123',expire_date='0922')
# db.session.add_all([customer1,customer2,customer3,customer4])
#db.session.commit()



