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
Identical_face_register_enable = True
client = boto3.client('rekognition', region_name=Region, aws_access_key_id=Aws_access_key_id, aws_secret_access_key=Aws_secret_access_key)

if ("amazonaws" in db_url and Collection_id == 'Deploy_Collection'):
    print ("using online db and deploy face collection")
elif ("amazonaws" not in db_url and Collection_id == 'Deploy_Collection'):
    print ("Should not do this !!!!!\n  using local db and deploy face collection")
elif ("amazonaws" in db_url and Collection_id == 'Test_Collection'):
    print ("Should not do this !!!!!\n  using online db and local face collection")
elif ("amazonaws" not in db_url and Collection_id == 'Test_Collection'):
    print ("using local db and local face collection")

from routes import *
from database import *

reset_db_with_some_initials()
print ("dummy print to check compilation")

# 添加用户
#customer1=Customer(id='400065323',first_name='Bohui',last_name='Yu',phone_number='6479365120',card_number='1234123412341234',cvv='123',expire_date='0922')
# customer2=Customer(id='400050636',first_name='Weike',last_name='Shi',phone_number='647936666',card_number='1234123412341234',cvv='456',expire_date='0922')
# customer3=Customer(id='400099173',first_name='Haolin',last_name='Ma',phone_number='6479365555',card_number='1234123412341234',cvv='123',expire_date='0922')
# customer4=Customer(id='400104626',first_name='Yunan',last_name='Zhou',phone_number='6479365111',card_number='1234123412341234',cvv='123',expire_date='0922')
# db.session.add_all([customer1,customer2,customer3,customer4])
#db.session.commit()



