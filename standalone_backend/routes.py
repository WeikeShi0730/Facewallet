from flask import Flask, jsonify, request, json
from main import app
from forms import *
from database import *


@app.route("/")

def homepage():
    return "Homepage for sanity"

@app.route("/testing", methods=['POST'])
def testing():
    data = json.loads(request.data, strict=False)
    print (data)
    return data

@app.route("/register", methods=['POST'])
#def get():
    #info = True
    #photo = True
    #message = "ok" if (info and photo) else "nok"
    #return jsonify({'message': message})
def post():
    data = json.loads(request.data, strict=False)
    print (data)
    print (type(data))
    #id='400065323',first_name='Bohui',last_name='Yu',phone_number='6479365120',account_number='1234123412341234',account_cvv='123',account_date='0922',email='yub14@mcmaster.ca'
    #customer = Customer(
        #first_name=data['first_name'], 
        #last_name=data['last_name'], 
        #phone_number=data['phone_number'], 
        #account_number=data['account_number'], 
        #account_cvv=data['account_cvv'], 
        #email=data['email'],
        #account_date=data['account_date']) 
    #register = RegisterForm(data)
    if (
        data.get('first_name') is not None and
        data.get('last_name') is not None and
        data.get('account_number') is not None and
        True #dummy value to keep format
        ): 
        person_name_at_bank_acc = data['first_name'] + "_" + data['last_name'] + "@" + data['account_number']
        print (person_name_at_bank_acc)
        #if "photo" in data:
        #    register_photo(data)
        #else:
        #    register_info(data)
        return jsonify({'message': 'ok'}),200
    else:
        return jsonify({'message': 'require more info'}),400
    
    #if "photo" in data:
        #register_photo(data)
    #else:
        #register_info(data)
   


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
