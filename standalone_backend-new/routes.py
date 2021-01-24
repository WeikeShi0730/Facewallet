from flask import Flask, jsonify, request, json
import glob
import re
import base64
from io import BytesIO, StringIO
from forms import *
from database import *
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
import hashlib
import uuid
import sys
sys.path.append('.')
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


@app.route("/testing", methods=['POST'])
def testing():
    data = json.loads(request.data, strict=False)
    print(data)
    return data

@app.route("/api/merchant/register", methods=['POST'])
def post_merchant_info():
    data = request.form
    if (check_merchant_form_not_none(data)):
        # MM_todo - check person whether exist in data base instead of AI model
        if (Merchant.query.filter(Merchant.email == data['email']).first()):
            print("user exist")
            return jsonify({'message': 'user already exist'}), 200
        else:
            merchant_id = uuid.uuid1()
            # access_token = create_access_token(identity=data['email'])
            # refresh_token = create_refresh_token(identity=data['email'])

            merchant_info = Merchant(
                id=merchant_id,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=hashlib.md5(data['password'].encode()).hexdigest(),
                #phone_number=data['phone_number'],
                shop_name=data['shop_name'],
            )
            db.session.add_all([merchant_info])
            db.session.commit()
            return jsonify({'message': 'ok, the text info is added into db', 'person_id': merchant_id}), 200

    else:
        print("form contains None")
        return jsonify({'message': 'require more info'}), 200


@app.route("/api/customer/register/info", methods=['POST'])
def post_customer_info():
    data = request.form
    #print(data)
    print(type(data))

    if (check_customer_form_not_none(data)):
        person_name_at_bank_acc = data['first_name'] + \
            "_" + data['last_name'] + "@" + data['card_number']
        print(person_name_at_bank_acc)
        # MM_todo - check person whether exist in data base instead of AI model
        if (check_person_existence(data)):
            print("user exist")
            return jsonify({'message': 'user already exist', 'name@bank': person_name_at_bank_acc}), 200
        else:
            person_id = data['first_name'] + "_" + data['last_name'] + "_" + data['phone_number']
            
            print('Person id created :',person_id,'\n')
            # because 2nd time called this, we dont have the id, we need to store it frist

            # access_token = create_access_token(identity=data['email'])
            # refresh_token = create_refresh_token(identity=data['email'])

            customer_info = Customer(
                id=person_id,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=hashlib.md5(data['password'].encode()).hexdigest(),
                phone_number=data['phone_number'],
                card_number=data['card_number'],
                cvv=data['cvv'],
                expire_date=data['expire_date']
                # MM_todo - register payment cnt intialize t0 0
            )
            db.session.add_all([customer_info])
            db.session.commit()

            return jsonify({'message': 'ok, the text info is added into db', 'person_id': person_id}), 200

    else:
        print("form contains None")
        return jsonify({'message': 'require more info'}), 200


@app.route("/register/photo/test", methods=['POST'])
def post_photo_test():
    data = json.loads(request.data, strict=False)
    # print (data)
    print(type(data))

    # im = Image.new("RGB", (300, 30), (220, 180, 180))
    # im.format'JPEG'
    # dr = ImageDraw.Draw(im)
    # font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 16)
    # text =time.strftime("%m/%d  %H:%M:%S") +u"这是一段测试文本。"
    # dr.text((10, 5), text, font=font, fill="#000000")

    return jsonify({'message': 'reponse'}), 200


@app.route("/api/customer/register/photo/<person_id>", methods=['POST'])
def post_photo(person_id=None):
    data = json.loads(request.data, strict=False)
    # print (data.get('photo'))
    print(type(data))
    if (person_id == None or data.get('photo') == None or person_id == "undefined"):
        return jsonify({'message': 'person_id not returned to the backend neither the photo'}), 200
    else:
        print("got person id" + person_id)
        [image_type, image_content] = re.split(",", data['photo'])
        print(image_type)
        if (image_type != "data:image/jpeg;base64"):
            return jsonify({'message': 'the image is not a jpeg type'}), 200

        try:
            aws_respose = add_faces_to_collection(image_content,person_id,Collection_id)
            user= Customer.query.get(person_id)
            print ('user info:',user,'\n')
            user.aws_id = aws_respose['FaceRecords'][0]['Face']['FaceId']
            db.session.commit()
            print (user.aws_id)
        except APIErrorException:
            print ("no face is detected")
            return jsonify({'message': "no face is detected"}),200
            
        return jsonify({'message': 'photo is added'}),200

def check_customer_form_not_none(data):
    if (
        data['first_name'] is not None and
        data['last_name'] is not None and
        data['phone_number'] is not None and
        data['email'] is not None and
        data['password'] is not None and
        data['card_number'] is not None and
        data['cvv'] is not None and
        data['expire_date'] is not None and
        True  # dummy value to keep format
    ):
        return True
    else:
        return False

def check_merchant_form_not_none(data):
    if (
        data['first_name'] is not None and
        data['last_name'] is not None and
        data['email'] is not None and
        data['password'] is not None and
        data['shop_name'] is not None and
        True  # dummy value to keep format
    ):
        return True
    else:
        return False


@app.route("/api/merchant/<person_id>/facepay", methods=['POST'])
def payment_photo(person_id=None):
    data = json.loads(request.data, strict=False)
    # print (data.get('photo'))
    print(type(data))
    if (data.get('photo') == None):
        return jsonify({'message': 'the photo not returned to the backend '}), 200
    else:
        [image_type, image_content] = re.split(",", data['photo'])
        print(image_type)
        if (image_type != "data:image/jpeg;base64"):
            return jsonify({'message': 'the image is not a jpeg type'}), 200
        nparr = np.fromstring(base64.b64decode(image_content), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite(constant.PAY_PHOTO_FOLDER +
                    '{person_id_name}.jpg'.format(person_id_name="temp"), img)
        file_p = open(constant.PAY_PHOTO_FOLDER +
                      '{person_id_name}.jpg'.format(person_id_name="temp"), 'r+b')
        # Detect faces
        face_ids = []
        try:
            faces = face_client.face.detect_with_stream(
                file_p, recognition_model=constant.RECOGNITION_MODEL)
        except APIErrorException:
            print("detect failure")
            return jsonify({'message': "detect failure"}), 200

        for face in faces:
            face_ids.append(face.face_id)
            print('face ID in faces {}.\n'.format(face.face_id))
        if (len(face_ids) == 0):
            print("No face detected in this verify image")
            return jsonify({'message': "No face detected in this verify image"}), 200
        elif (len(faces) > 1):
            print(
                "More than 1 faces detected in this verify image. Please retake the photo")
            return jsonify({'message': "More than 1 faces detected in this verify image. Please retake the photo"}), 200
        else:
            try:
                results = face_client.face.identify(
                    face_ids, constant.PERSON_GROUP_ID)
            except APIErrorException:
                print("identify failure, possibly person group not train")
                return jsonify({'message': "identify failure, possibly person group not train"}), 200

            if not results:
                print('No person in AI database matched with this verification')
                return jsonify({'message': "No person in AI database matched with this verification"}), 200
            else:
                # should be only 1 face
                first_face = results[0]
                first_candidates = first_face.candidates[0]
                print("test")
                print(first_face)
                print(type(first_face))
                print(first_candidates)
                print(type(first_candidates))
                if (len(first_face.candidates) == 0):
                    print(
                        'No candidates person in this database matched with this verification')
                    return jsonify({'message': "No candidates person in this database matched with this verification"}), 200
                else:
                    first_person_id = first_candidates.person_id
                    first_person_confidence = first_candidates.confidence
                    first_person_name = face_client.person_group_person.get(
                        constant.PERSON_GROUP_ID, first_candidates.person_id).name
                    print('Person name {} with person_id {} matched with this cerification with a confidence of {}.'.format(
                        first_person_name, first_person_id, first_person_confidence))

                    # MM_todo query database, return user all info
                    # MM_todo set confidence threholds, check payment_cnt
                    return jsonify({'message': 'succeed', 'person_id': first_person_id, 'person_name': first_person_name, 'require_phone_number': 0, 'confidence': first_person_confidence}), 200
    return jsonify({'message': 'reponse'}), 200


@app.route("/api/customer/signin", methods=['POST'])
def customer_signin():
    try:
        email = request.form["email"]
        password = request.form["password"]
        current_user = Customer.query.filter(Customer.email == email).first()
        if not current_user:
            return {"error": "User not in DB. Register as a new user"}

        password = hashlib.md5(password.encode()).hexdigest()    
        if current_user.password == password:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify({'message': 'ok, the text info is added into db', 'person_id': current_user.id}), 200

        else:
            return {'error': 'Wrong credentials'}
    except:
        raise Exception("Cannot login user")


@app.route("/api/merchant/signin", methods=['POST'])
def merchant_signin():
    try:
        email = request.form["email"]
        password = request.form["password"]
        current_user = Merchant.query.filter(Merchant.email == email).first()
        if not current_user:
            return {"error": "User not in DB. Register as a new user"}

        password = hashlib.md5(password.encode()).hexdigest()    
        if current_user.password == password:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify({'message': 'ok, the text info is added into db', 'person_id': current_user.id}), 200

        else:
            return {'error': 'Wrong credentials'}
    except:
        raise Exception("Cannot login user")
