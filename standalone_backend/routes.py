from flask import Flask, jsonify, request, json
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
def post():
    data = json.loads(request.data, strict=False)
    print (data)
    print (type(data))
    #customer = Customer(
        #first_name=data['first_name'], 
        #last_name=data['last_name'], 
        #phone_number=data['phone_number'], 
        #account_number=data['account_number'], 
        #account_cvv=data['account_cvv'], 
        #email=data['email'],
        #account_date=data['account_date']) 
    #register = RegisterForm(data)

    #if "photo" in data:
    #    register_photo(data)
    #else:
    #    register_info(data)
    if (check_form_not_none(data)): 
        person_name_at_bank_acc = data['first_name'] + "_" + data['last_name'] + "@" + data['account_number']
        print (person_name_at_bank_acc)
        if (check_person_exist(face_client,person_name_at_bank_acc)):
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
                    account_number=data.get('account_number'),
                    account_cvv=data.get('account_cvv'),
                    account_date=data.get('account_date'),
                    email=data.get('email')
                    )
            db.session.add_all([customer_info])
            db.session.commit()

            return jsonify({'message': 'ok, the text info is added into db'}),200

    else:
        return jsonify({'message': 'require more info'}),400
    
def check_form_not_none(data):
    if (
        data.get('first_name') is not None and
        data.get('last_name') is not None and
        data.get('phone_number') is not None and
        data.get('account_number') is not None and
        data.get('account_cvv') is not None and
        data.get('account_date') is not None and
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


@app.route("/register", methods=['GET'])
def register_message():
    info = True
    photo = True
    message = "ok" if (info and photo) else "nok"
    return jsonify({'message': message})


@app.route("/payment")
def payment():
    return "payment"
