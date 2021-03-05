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

os.environ["FACE_SUBSCRIPTION_KEY"] = "97ed7848c921405a80168adfbe8e2039"
os.environ["FACE_ENDPOINT"] = "https://aslfjkl1245132q.cognitiveservices.azure.com/"

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'my-unique-person-group'

# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

#face_client.person_group.delete(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
'''
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
#face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

## Define woman friend
woman = face_client.person_group_person.create(PERSON_GROUP_ID, "Woman")
## Define man friend
man = face_client.person_group_person.create(PERSON_GROUP_ID, "Man")
## Define child friend
child = face_client.person_group_person.create(PERSON_GROUP_ID, "Child")

'''
Detect faces and register to correct person
'''
## Find all jpeg images of friends in working directory
woman_images = [file for file in glob.glob('*.jpg') if file.startswith("woman")]
man_images = [file for file in glob.glob('*.jpg') if file.startswith("man")]
child_images = [file for file in glob.glob('*.jpg') if file.startswith("child")]

# Add to a woman person
for image in woman_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, woman.person_id, w)

# Add to a man person
for image in man_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, man.person_id, m)

# Add to a child person
for image in child_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, child.person_id, ch)


person_group_list = face_client.person_group.list()
person_group_person_list = face_client.person_group_person.list(PERSON_GROUP_ID)
for x in person_group_list:
    print (x)
print ("\n\n")
for y in person_group_person_list:
    print (y)
    print ("\n")
    print('PersonGroup person_id {}.\n'.format(y.person_id))
    #print ((y['persisted_face_id']))
#print (person_group_person_list[1])

'''
Train PersonGroup
'''
print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)

'''
Identify a face against a defined PersonGroup
'''
# Group image for testing against
group_photo = 'test-image-person-group.jpg'
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
# Get test image
test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
image = open(test_image_array[0], 'r+b')

# Detect faces
face_ids = []
faces = face_client.face.detect_with_stream(image)
for face in faces:
    face_ids.append(face.face_id)
    print('face ID in faces {}.\n'.format(face.face_id)) 

# Identify faces
results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
print('Identifying faces in {}'.format(os.path.basename(image.name)))
if not results:
    print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
for person in results:
    print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) 
    for possible in person.candidates:
        print ("test\n")
        print('Person for face ID {} is identified in person_id {} with a confidence of {}.'.format(person.face_id, possible.person_id, possible.confidence)) 
    #print ("test\n")
    #verify_results = face_client.face.verify_face_to_person(person.face_id,'d21b8e11-4fa6-47f8-8c26-93274c25ef9c',PERSON_GROUP_ID)
    #print (verify_results.is_identical)
    #print ("\n")
    #print (verify_results.confidence)


## Base url for the Verify and Facelist/Large Facelist operations
#IMAGE_BASE_URL = 'https://csdx.blob.core.windows.net/resources/Face/Images/'
#
## Create a list to hold the target photos of the same person
#target_image_file_names = ['Family1-Dad1.jpg', 'Family1-Dad2.jpg']
## The source photos contain this person
#source_image_file_name1 = 'Family1-Dad3.jpg'
#source_image_file_name2 = 'Family1-Son1.jpg'
#
## Detect face(s) from source image 1, returns a list[DetectedFaces]
#detected_faces1 = face_client.face.detect_with_url(IMAGE_BASE_URL + source_image_file_name1)
## Add the returned face's face ID
#source_image1_id = detected_faces1[0].face_id
#print('{} face(s) detected from image {}.'.format(len(detected_faces1), source_image_file_name1))
#
## Detect face(s) from source image 2, returns a list[DetectedFaces]
#detected_faces2 = face_client.face.detect_with_url(IMAGE_BASE_URL + source_image_file_name2)
## Add the returned face's face ID
#source_image2_id = detected_faces2[0].face_id
#print('{} face(s) detected from image {}.'.format(len(detected_faces2), source_image_file_name2))
#
## List for the target face IDs (uuids)
#detected_faces_ids = []
## Detect faces from target image url list, returns a list[DetectedFaces]
#for image_file_name in target_image_file_names:
    #detected_faces = face_client.face.detect_with_url(IMAGE_BASE_URL + image_file_name)
    ## Add the returned face's face ID
    #detected_faces_ids.append(detected_faces[0].face_id)
    #print('{} face(s) detected from image {}.'.format(len(detected_faces), image_file_name))
#
## Verification example for faces of the same person. The higher the confidence, the more identical the faces in the images are.
## Since target faces are the same person, in this example, we can use the 1st ID in the detected_faces_ids list to compare.
#verify_result_same = face_client.face.verify_face_to_face(source_image1_id, detected_faces_ids[0])
#print('Faces from {} & {} are of the same person, with confidence: {}'
    #.format(source_image_file_name1, target_image_file_names[0], verify_result_same.confidence)
    #if verify_result_same.is_identical
    #else 'Faces from {} & {} are of a different person, with confidence: {}'
        #.format(source_image_file_name1, target_image_file_names[0], verify_result_same.confidence))
#
## Verification example for faces of different persons.
## Since target faces are same person, in this example, we can use the 1st ID in the detected_faces_ids list to compare.
#verify_result_diff = face_client.face.verify_face_to_face(source_image2_id, detected_faces_ids[0])
#print('Faces from {} & {} are of the same person, with confidence: {}'
    #.format(source_image_file_name2, target_image_file_names[0], verify_result_diff.confidence)
    #if verify_result_diff.is_identical
    #else 'Faces from {} & {} are of a different person, with confidence: {}'
        #.format(source_image_file_name2, target_image_file_names[0], verify_result_diff.confidence))


