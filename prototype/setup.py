# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 20:40:17 2020

@author: Michael
"""

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

#our own script
from utils import *
from register import *
from payment import *
import numpy as np
import cv2


# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

#make this global, so we can run in the terminal cmd
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def main():
    # Create an authenticated FaceClient.


    # Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
    # You can call list_person_groups to print a list of preexisting PersonGroups.
    # SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
    PERSON_GROUP_ID = 'prototype_group'

    # Used for the Snapshot and Delete Person Group examples.
    TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

    #delete_person_group(face_client,PERSON_GROUP_ID)
    
    create_person_group(face_client,PERSON_GROUP_ID)

    #register_person(face_client,"sample_man","sample_man","425224145215241525","5152","521")
    register_person(face_client,"sample_woman","sample_woman","425224145215241525","5152","521")

    list_out_person(face_client)
    #train_person_group(face_client)

    #verify_payment(face_client,verify_photo="verify_woman_1")
    #verify_payment(face_client,verify_photo="test-image-person-group")


def train_person_group(client,PERSON_GROUP_ID='prototype_group'):
    print()
    print('Training the person group...')
    # Train the person group
    train_start_time = time.time()
    client.person_group.train(PERSON_GROUP_ID)
    while (True):
        training_status = client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(1)
    train_end_time = time.time()
    print ("training take {}. ".format(train_end_time-train_start_time))

main()
