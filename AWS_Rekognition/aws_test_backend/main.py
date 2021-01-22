
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
from PIL import Image, ImageDraw
#from azure.cognitiveservices.vision.face import FaceClient
#from msrest.authentication import CognitiveServicesCredentials
#from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
sys.path.append('.')
import boto3

import constant

app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


#AZURE_KEY = os.environ['FACE_SUBSCRIPTION_KEY']
#AZURE_ENDPOINT = os.environ['FACE_ENDPOINT']
Region = os.environ['REGION_NAME']
Aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
Aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
Collection_id = os.environ['COLLECTION_ID']

client = boto3.client('rekognition', region_name=Region, aws_access_key_id=Aws_access_key_id, aws_secret_access_key=Aws_secret_access_key)

#face_client = FaceClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

#PERSON_GROUP_ID = constant.PERSON_GROUP_ID
#TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)
#delete_person_group(face_client,PERSON_GROUP_ID)
#create_person_group(face_client,PERSON_GROUP_ID)

from routes import *
from database import *
# 删除表
db.drop_all()
# 创建表
db.create_all()
# 添加用户
customer1=Customer(id='400065323',first_name='Bohui',last_name='Yu',phone_number='6479365120',card_number='1234123412341234',cvv='123',expire_date='0922')
customer2=Customer(id='400050636',first_name='Weike',last_name='Shi',phone_number='647936666',card_number='1234123412341234',cvv='456',expire_date='0922')
customer3=Customer(id='400099173',first_name='Haolin',last_name='Ma',phone_number='6479365555',card_number='1234123412341234',cvv='123',expire_date='0922')
customer4=Customer(id='400104626',first_name='Yunan',last_name='Zhou',phone_number='6479365111',card_number='1234123412341234',cvv='123',expire_date='0922')
db.session.add_all([customer1,customer2,customer3,customer4])
db.session.commit()
