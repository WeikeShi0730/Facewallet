from flask import Flask, jsonify, request, json
import glob
import re
import base64
from io import BytesIO,StringIO
from PIL import Image, ImageDraw, ImageFont
from main import *
from forms import *
from database import *
#from azure.cognitiveservices.vision.face.models import APIErrorException
import sys
sys.path.append('.')
#from azure.utils import *
from register import *
from Aws_functions import *
from main import app,db, Collection_id, client

@app.route("/")

def homepage():
    return "Homepage for sanity"

@app.route("/list")
def list_person():
    faces_count=list_faces_in_collection(Collection_id)
    print("faces count: " + str(faces_count))

    return "list printed in terminal"

@app.route("/testing", methods=['POST'])
def testing():
    data = json.loads(request.data, strict=False)
    print (data)
    return data

@app.route("/register/info", methods=['POST'])
def post_info():
    data = json.loads(request.data, strict=False)
    #print (data)
    print (type(data))
    if (check_form_not_none(data)): 
        person_name_at_bank_acc = data['first_name'] + "_" + data['last_name'] + "@" + data['card_number']
        print (person_name_at_bank_acc)
        #MM_todo - check person whether exist in data base instead of AI model
        if (check_person_existence(data)):
            print ("user exist")
            return jsonify({'message': 'user already exist','name@bank':person_name_at_bank_acc}),200
        else:
            #Yunan: use name_phone as id
            # so 'id' and 'aws_id' are different items
            
            person_id = data['first_name'] + "_" + data['last_name'] + "_" + data['phone_number']
            print (person_id)
            #because 2nd time called this, we dont have the id, we need to store it frist 

            customer_info = Customer(
                    id=person_id,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    phone_number=data.get('phone_number'),
                    card_number=data.get('card_number'),
                    cvv=data.get('cvv'),
                    expire_date=data.get('expire_date')
                    #MM_todo - register payment cnt intialize t0 0

                    )
            db.session.add_all([customer_info])
            db.session.commit()
            print ("user added !!!!!!!!!!!!!!!!\n")

            return jsonify({'message': 'ok, the text info is added into db', 'person_id': person_id}),200

    else:
        print ("form contains None")
        return jsonify({'message': 'require more info'}),200
    
@app.route("/register/photo/test", methods=['POST'])
def post_photo_test():
    data = json.loads(request.data, strict=False)
    #print (data)
    print (type(data))

    #im = Image.new("RGB", (300, 30), (220, 180, 180))
    ##im.format'JPEG'
    #dr = ImageDraw.Draw(im)
    #font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 16)
    #text =time.strftime("%m/%d  %H:%M:%S") +u"这是一段测试文本。"
    #dr.text((10, 5), text, font=font, fill="#000000")

    return jsonify({'message': 'reponse'}),200

@app.route("/register/photo/<person_id>", methods=['POST'])
def post_photo(person_id = None):
    data = json.loads(request.data, strict=False)
    #print (data.get('photo'))
    print (type(data))
    if (person_id == None or data.get('photo') == None or person_id == "undefined"):
        return jsonify({'message': 'person_id not returned to the backend neither the photo'}),200
    else:
        print ("got person id" + person_id)
        [image_type,image_content] = re.split(",",data['photo'])
        if (image_type != "data:image/jpeg;base64"):
            return jsonify({'message': 'the image is not a jpeg type'}),200


        try:
            aws_respose = add_faces_to_collection(image_content,person_id,Collection_id)
            user= Customer.query.get(person_id)
            print (user)
            user.aws_id = aws_respose['FaceRecords'][0]['Face']['FaceId']
            db.session.commit()
            print (user.aws_id)
        except APIErrorException:
            print ("no face is detected")
            return jsonify({'message': "no face is detected"}),200
            
        return jsonify({'message': 'photo is added'}),200



def check_form_not_none(data):
    if (
        data.get('first_name') is not None and
        data.get('last_name') is not None and
        data.get('phone_number') is not None and
        data.get('card_number') is not None and
        data.get('cvv') is not None and
        data.get('expire_date') is not None and
        True #dummy value to keep format
        ): 
        return True
    else:
        return False

@app.route("/payment", methods=['POST'])
def payment_photo():
    data = json.loads(request.data, strict=False)
    #print (data.get('photo'))
    print (type(data))
    if (data.get('photo') == None):
        return jsonify({'message': 'the photo not returned to the backend '}),200
    else:
        [image_type,image_content] = re.split(",",data['photo'])
        print (image_type)
        if (image_type != "data:image/jpeg;base64"):
           return jsonify({'message': 'the image is not a jpeg type'}),200
        try:
            faceMatches=search_face_in_collection(image_content,Collection_id)
            if not faceMatches:
                print ('no matched faces')
                return jsonify({'message': "no matched faces"}),200
            else:
                print ('Matching faces')
                for match in faceMatches:
                        print ('FaceId:' + match['Face']['FaceId'])
                        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                return jsonify({'message': 'succeed', 'person_id' : faceMatches[0]['Face']['FaceId'], 'require_phone_number' : 0, 'Similarity' : faceMatches[0]['Similarity']}),200
        except APIErrorException:
           print ("detect failure")
           return jsonify({'message': "detect failure"}),200

        
