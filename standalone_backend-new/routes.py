from flask import Flask, jsonify, request, json
import glob
import re
import base64
import random
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
    return 'print on terminal'

@app.route("/test_db/transaction")
def test_db_transaction():
    record = Transaction.query.filter(Transaction.customer_id == '1234567890').first()
    # record = Transaction.query.all()
    print(record)
    print(record.trans_id)
    print(record.amount)
    print(record.customer_id)
    print(record.merchant_id)
    return 'Transaction table okay'

@app.route("/test_db/customer")
def test_db_customer():
    record = Customer.query.filter(Customer.id == '1234567890').first()
    # record = Transaction.query.all()
    print(record)
    print(record.card_number)
    print(record.balance)
    print(record.phone_number)
    print(record.sec_verify)
    return 'customer table okay'

@app.route("/test_db/merchant")
def test_db_merchant():
    record = Merchant.query.filter(Merchant.id == '1234567890').first()
    # record = Transaction.query.all()
    print(record)
    print(record.shop_name)
    print(record.balance)
    print(record.first_name)
    return 'merchant table okay'

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

        faceMatches=search_face_in_collection(image_content,Collection_id)
        if not faceMatches:
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
        else:
            cus = Customer.query.filter(Customer.aws_id ==faceMatches[0]['Face']['FaceId'] ).first()
            cus_id = cus.id
            cus_name = cus.first_name + cus.last_name
            print("user may had an acount already")
            Customer.query.filter(Customer.id == person_id).delete()
            db.session.commit()
            return jsonify({'message':'existing face found','level':'warning','Customer_id':cus_id,'Customer_name':cus_name}),200

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
        # if (True):
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
                # if False:
                    print("Identical faces found")
                    return jsonify({'message':'Secondary verification needed','level':'warning'})
                else:
                    print ("FaceId")
                    print (faceMatches[0]['Face']['FaceId'])
                    cus_id = Customer.query.filter(Customer.aws_id ==faceMatches[0]['Face']['FaceId'] ).first().id
                    print ("cus_id")
                    print (cus_id)
                    mer_id = person_id
                    amount = float(data.get('amount'))
                    New_transaction = Transaction(
                        trans_id = random.randint(0,100),
                        amount = amount,
                        customer_id = cus_id,
                        merchant_id = mer_id
                        )
                    db.session.add_all([New_transaction])
                    customer_user = Customer.query.filter(Customer.id == cus_id).first()
                    customer_user.balance -= amount
                    merchant_user = Merchant.query.filter(Merchant.id == mer_id).first()
                    merchant_user.balance += amount
                    db.session.commit()
                    print ("merchant_user:")
                    print (merchant_user.balance)
                    print ("cust_user:")
                    print (customer_user.balance)
                    
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

def pre_jsonify_transaction(db_obj):
    # output_dict = {
    #     "trans_id" : "null",
    #     "date_time" : "null",
    #     "amount" : "null",
    #     "customer_id" : "null",
    #     "merchant_id" : "null",
    #     # "customer" : "null",
    #     # "merchant" : "null",
    # }
    output_dict = dict()
    output_dict['trans_id'] = db_obj.trans_id
    output_dict['date_time'] = db_obj.date_time
    output_dict['amount'] = db_obj.amount
    output_dict['customer_id'] = db_obj.customer_id
    output_dict['merchant_id'] = db_obj.merchant_id
    return output_dict

def cust_handle_db_transaction(db_obj):

    multi_dict = dict()
    trans_dict = dict()
    cnt=1
    for instant in db_obj:
        dictionary = 'Transaction_instance_'+str(cnt)
        trans_dict[dictionary] = pre_jsonify_transaction(instant)

        #query shop name
        merchant_id = trans_dict[dictionary]['merchant_id']
        merchant_info = Merchant.query.filter(Merchant.id == merchant_id).first()
        mer_list =dict()
        mer_list['Merchant'] = pre_jsonify_merchant(merchant_info)
        # shop_name = Merchant.query.filter(Merchant.id == merchant_id).first().shop_name
        # shop_dict = {'shop_name' : shop_name}
        trans_dict[dictionary].update(mer_list)

        # print ('in func')
        # print (trans_dict[dictionary])
        multi_dict.update(trans_dict)
        # print (multi_dict)
        cnt += 1
    trans_dict = multi_dict

    return trans_dict

def mer_handle_db_transaction(db_obj):

    multi_dict = dict()
    trans_dict = dict()
    cnt=1
    for instant in db_obj:
        dictionary = 'Transaction_instance_'+str(cnt)
        trans_dict[dictionary] = pre_jsonify_transaction(instant)

        #query customer
        customer_id = trans_dict[dictionary]['customer_id']
        customer_info = Customer.query.filter(Customer.id == customer_id).first()
        cust_list =dict()
        cust_list['Customer'] = pre_jsonify_customer(customer_info)
        trans_dict[dictionary].update(cust_list)

        # print ('in func')
        # print (trans_dict[dictionary])
        multi_dict.update(trans_dict)
        # print (multi_dict)
        cnt += 1
    trans_dict = multi_dict

    return trans_dict

def pre_jsonify_customer(db_obj):
    output_dict = dict()
    output_dict['id'] = db_obj.id
    output_dict['aws_id'] = db_obj.aws_id
    output_dict['first_name'] = db_obj.first_name
    output_dict['last_name'] = db_obj.last_name
    # output_dict['phone_number'] = db_obj.phone_number
    # output_dict['email'] = db_obj.email
    # output_dict['password'] = db_obj.phone_numbpassworder
    output_dict['card_number'] = db_obj.card_number
    # output_dict['cvv'] = db_obj.cvv
    # output_dict['expire_date'] = db_obj.expire_date
    # output_dict['payment_cnt'] = db_obj.payment_cnt
    # output_dict['reg_image_cnt'] = db_obj.reg_image_cnt
    # output_dict['sec_verify'] = db_obj.sec_verify
    output_dict['balance'] = db_obj.balance
    return output_dict

def pre_jsonify_merchant(db_obj):
    output_dict = dict()
    output_dict['id'] = db_obj.id
    output_dict['aws_id'] = db_obj.aws_id
    output_dict['first_name'] = db_obj.first_name
    output_dict['last_name'] = db_obj.last_name
    # output_dict['phone_number'] = db_obj.phone_number
    # output_dict['email'] = db_obj.email
    # output_dict['password'] = db_obj.phone_numbpassworder
    output_dict['shop_name'] = db_obj.shop_name
    output_dict['balance'] = db_obj.balance
    return output_dict

# @app.route("/api/customer/<person_id>/profile", methods=['POST'])
@app.route("/api/customer/<person_id>/profile", methods=['GET'])
def customer_profile(person_id=None):

    record = Transaction.query.filter(Transaction.customer_id == person_id).all()
    print(type(record))
    print(len(record))
    # print(record[0].amount)
    # print(record[1].amount)
    # for col in record:
    #     print(col)
    trans_list = dict()
    trans_list['Transaction'] = cust_handle_db_transaction(record)
    # print(trans_list)

    cust_list = dict()
    customer_info = Customer.query.filter(Customer.id == person_id).first()
    cust_list['Customer'] = pre_jsonify_customer(customer_info)
    # print(cust_list)

    full_json = dict()
    full_json.update(trans_list)
    full_json.update(cust_list)
    # print(full_json)

    return jsonify(full_json)
    # return jsonify({'level':'success','transaction record': record})

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

@app.route("/api/merchant/<person_id>/profile", methods=['GET'])
def merchant_profile(person_id=None):
    
    record = Transaction.query.filter(Transaction.merchant_id == person_id).all()
    print(type(record))
    print(len(record))
    # print(record[0].amount)
    # print(record[1].amount)
    # for col in record:
    #     print(col)
    trans_list = dict()
    trans_list['Transaction'] = mer_handle_db_transaction(record)
    # print(trans_list)

    mer_list = dict()
    merchant_info = Merchant.query.filter(Merchant.id == person_id).first()
    mer_list['Merchant'] = pre_jsonify_merchant(merchant_info)
    # print(mer_list)

    full_json = dict()
    full_json.update(trans_list)
    full_json.update(mer_list)
    # print(full_json)

    return jsonify(full_json)
