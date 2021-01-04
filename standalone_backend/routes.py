from flask import Flask, jsonify, request, json
import glob
import re
import cv2
import base64
from io import BytesIO,StringIO
from PIL import Image, ImageDraw, ImageFont
from main import app,face_client,db
from forms import *
from database import *
import sys
sys.path.append('.')
from azure.utils import *
from azure.register import *
from azure.payment import *


@app.route("/")

def homepage():
    return "Homepage for sanity"

@app.route("/list")
def list_person():
    list_out_person(face_client)
    return "list printed in terminal"

@app.route("/testing", methods=['POST'])
def testing():
    data = json.loads(request.data, strict=False)
    print (data)
    return data

@app.route("/register/info", methods=['POST'])
def post_info():
    register_info = json.loads(request.data, strict=False)
    data = register_info.get('registerInfo')
    print (data)
    print (type(data))
    #customer = Customer(
        #first_name=data['first_name'], 
        #last_name=data['last_name'], 
        #phone_number=data['phone_number'], 
        #card_number=data['account_number'], 
        #cvv=data['cvv'], 
        #email=data['email'],
        #expire_date=data['expire_date']) 
    #register = RegisterForm(data)

    if (check_form_not_none(data)): 
        person_name_at_bank_acc = data['first_name'] + "_" + data['last_name'] + "@" + data['card_number']
        print (person_name_at_bank_acc)
        if (check_person_exist(face_client,person_name_at_bank_acc)):
            print ("user exist")
            return jsonify({'message': 'user already exist','name@bank':person_name_at_bank_acc}),200
        else:
            person_id = create_person(face_client,person_name_at_bank_acc)
            if person_id is None:
                return jsonify({'message': 'AI model can not create a person'}),200
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
                    )
            db.session.add_all([customer_info])
            db.session.commit()

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
        print (image_type)
        if (image_type != "data:image/jpeg;base64"):
            return jsonify({'message': 'the image is not a jpeg type'}),200
        #print (type(image_content))
        #print (type(base64.b64decode(image_content)))
        nparr = np.fromstring(base64.b64decode(image_content), np.uint8)
        #print (type(nparr))
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #print (type(img))
        #cv2.imshow('img',img)
        cv2.imwrite('./img.jpg', img) 
        file_p = open('./img.jpg', 'r+b')
        #when we add face, we can also add the name@bank as the argument
        #face_client.person_group_person.add_face_from_url(constant.PERSON_GROUP_ID, person_id, image_content, name="ma@123")

        face_client.person_group_person.add_face_from_stream(constant.PERSON_GROUP_ID, person_id, file_p)#, name="ma@123")
        #person_id = create_person(face_client,person_name_at_bank_acc)

        return jsonify({'message': 'ok'}),200

    return jsonify({'message': 'reponse'}),200


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



def register_info(info_data):
    time.sleep(1)
    return info_data, 201


def register_photo(photo_data):
    time.sleep(5)
    return photo_data, 201

@app.route("/payment")
def payment():
    return "payment"
