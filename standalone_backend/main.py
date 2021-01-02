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
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

sys.path.append('.')
from azure.utils import *
from azure.register import *
from azure.payment import *

app = Flask("__main__")

AZURE_KEY = os.environ['FACE_SUBSCRIPTION_KEY']
AZURE_ENDPOINT = os.environ['FACE_ENDPOINT']

face_client = FaceClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

PERSON_GROUP_ID = 'prototype_group'
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)
#delete_person_group(face_client,PERSON_GROUP_ID)
create_person_group(face_client,PERSON_GROUP_ID)

@app.route("/")
def homepage():
    
    return "Homepage for sanity"

@app.route("/testing", methods=['POST'])
def testing():
    data = json.loads(request.data, strict=False)
    print (data)
    return data

@app.route("/register", methods=['POST'])
def register():
    data = json.loads(request.data, strict=False)
    if "photo" in data:
        register_photo(data)
    else:
        register_info(data)
    return data


def register_info(info_data):
    time.sleep(1)
    return info_data, 201


def register_photo(photo_data):
    time.sleep(5)
    return photo_data, 201


@app.route("/register", methods=['GET'])
def register_message():
    info = True
    photo = True
    message = "ok" if (info and photo) else "nok"
    return jsonify({'message': message})


@app.route("/payment")
def payment():
    return "payment"
