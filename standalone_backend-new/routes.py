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
        if (check_person_existence_M(data)):
            print("user exist")
            return jsonify({'message': 'user already exist','level':'error'}), 200
        else:
            merchant_id = generate_id()
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
                balance = 100
            )
            db.session.add_all([merchant_info])
            db.session.commit()
            return jsonify({'message': 'ok, the text info is added into db', 'person_id': merchant_id,'level':'info'}), 200

    else:
        print("form contains None")
        return jsonify({'message': 'Error: require more info','level':'error'}), 200


@app.route("/api/customer/register/info", methods=['POST'])
def post_customer_info():
    data = request.form
    #print(data)
    print(type(data))

    if (check_customer_form_not_none(data)):
        person_name_at_bank_acc = data['first_name'] + \
            "_" + data['last_name'] + "@" + data['card_number']
        print('person try to register:',person_name_at_bank_acc,'\n')
        # MM_todo - check person whether exist in data base instead of AI model
        if (check_person_existence_C(data)):
            print("user exist")
            return jsonify({'message': 'user already exist', 'level':'error'}), 200
        else:
            person_id = generate_id()
            
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
                expire_date=data['expire_date'],
                sec_verify = data['secondary']=='false',
                balance = 100
                # MM_todo - register payment cnt intialize t0 0
            )
            db.session.add_all([customer_info])
            db.session.commit()

            return jsonify({'message': 'ok, the text info is added into db', 'person_id': person_id,'level':'info'}), 200

    else:
        print("form contains None")
        return jsonify({'message': 'Error: require more info','level':'error'}), 200


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
    #print (data.get('photo'),'\n')
    print('data tpye of photo',type(data),'\n')
    print('id:',person_id,'\n')
    if (person_id == None or data['photo'] == None or person_id == "undefined"):
        return jsonify({'message': 'person_id not returned to the backend neither the photo','level':'error'}), 200
    else:
        print("got person id" + person_id)
        [image_type, image_content] = re.split(",", data['photo'])
        print(image_type)
        if (image_type != "data:image/jpeg;base64"):
            return jsonify({'message': 'the image is not a jpeg type','level':'warning'}), 200

        try:
            aws_respose = add_faces_to_collection(image_content,person_id,Collection_id)
            user= Customer.query.get(person_id)
            print ('user info:',user,'\n')
            user.aws_id = aws_respose['FaceRecords'][0]['Face']['FaceId']
            db.session.commit()
            print (user.aws_id)
        except IndexError:
            print ("Error: no face is detected in the image")
            return jsonify({'message': 'no face is detected','level':'error'}),200
            
        return jsonify({'message': 'photo is added','level': 'success'}),200

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
        return jsonify({'message': 'Error: the photo not returned to the backend ','level':'error'}), 200
    else:
        [image_type, image_content] = re.split(",", data['photo'])
        print(image_type)
        if (image_type != "data:image/jpeg;base64"):
            return jsonify({'message': 'Error: the image is not a jpeg type','level':'warning'}), 200
        try:
            faceMatches=search_face_in_collection(image_content,Collection_id)
            if not faceMatches:
                print ('no matched faces')
                return jsonify({'message': 'no record faces in the input image','level':'warning'}),200
            else:
                print ('Matching faces')
                
                for match in faceMatches:
                        print ('FaceId:' + match['Face']['FaceId'])
                        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                if len(faceMatches)>1:
                    print("Identical faces found")
                    return jsonify({'message':'Secondary verification needed','level':'warning'})
                else:
                    cus_id = Customer.query.filter(Customer.aws_id ==faceMatches[0]['Face']['FaceId'] ).first().id
                    mer_id = person_id
                    amount = float(data.get('amount'))
                    New_transaction = Transaction(
                        amount = amount,
                        customer_id = cus_id,
                        Merchant_id = mer_id
                        )
                    db.session.add_all([New_transaction])
                    customer_user = Customer.query.get(cus_id)
                    customer_user.balance += amount
                    merchant_user = Merchant.query.get(mer_id)
                    merchant_user.balance -= amount
                    db.session.commit()
                    
                    return jsonify({'message': 'succeed', 'person_id' : faceMatches[0]['Face']['FaceId'], 
                                    'require_phone_number' : 0, 'Similarity' : faceMatches[0]['Similarity'], 'level':'success'}),200
        except:
           print ("detect failure")
           return jsonify({'message': 'detect failure, unexpected error','level':'error'}),200


@app.route("/api/customer/signin", methods=['POST'])
def customer_signin():
    try:
        email = request.form["email"]
        password = request.form["password"]
        current_user = Customer.query.filter(Customer.email == email).first()
        if not current_user:
            return {'message': 'User not in DB. Register as a new user','level':'error'}

        password = hashlib.md5(password.encode()).hexdigest()    
        if current_user.password == password:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify({'message': 'ok, the text info is added into db', 'person_id': current_user.id,'level':'error'}), 200

        else:
            return jsonify({'message': 'Wrong credentials','level':'error'})
    except:
        raise Exception("Cannot login user")

@app.route("/api/customer/<person_id>/profile", methods=['POST'])
def customer_profile(person_id=None):

    record = Transaction.query.filter(Transaction.customer_id == person_id).first()
    print(record)
    return jsonify({'level':'success','transaction record': record})

@app.route("/api/customer/test/profile")
def test_profile(person_id=None):
    record = Transaction.query.all()
    print(record)
    return jsonify({'level':'success','transaction record': record})

@app.route("/api/merchant/signin", methods=['POST'])
def merchant_signin():
    try:
        email = request.form["email"]
        password = request.form["password"]
        current_user = Merchant.query.filter(Merchant.email == email).first()
        if not current_user:
            return {'message': 'User not in DB. Register as a new user','level':'error'}

        password = hashlib.md5(password.encode()).hexdigest()    
        if current_user.password == password:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify({'message': 'ok, the text info is added into db', 'person_id': current_user.id,'level':'info'}), 200

        else:
            return jsonify({'message': 'Wrong credentials','level':'error'})
    except:
        raise Exception("Cannot login user")

@app.route("/api/merchant/<person_id>/profile", methods=['POST'])
def merchant_profile(person_id=None):
    record = Transaction.query.filter(Transaction.merchant_id == person_id).first()
    print(record)
    return jsonify({'level':'success','transaction record': record})
