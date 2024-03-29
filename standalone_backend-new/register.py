from wtforms.validators import Email
from database import Customer,Merchant
import glob
import time
import constant
import uuid

#modified for AWS
def check_person_existence_C(data):
    existing = Customer.query.filter(Customer.first_name ==data['first_name'], 
    Customer.last_name==data['last_name'],
    Customer.card_number==data['card_number'],
    Customer.phone_number==data['phone_number'],
    Customer.email==data['email']).first()

    phone = Customer.query.filter(Customer.phone_number==data['phone_number']).first()
    email = Customer.query.filter(Customer.email==data['email']).first()

    if existing != None:
        print(existing.id)
        return 1
    elif email != None:
        return 2
    elif phone != None:
        return 3
    else:
        return False

def check_person_existence_M(data):
    existing = Merchant.query.filter(Merchant.first_name ==data['first_name'], 
    Merchant.last_name==data['last_name'],
    Merchant.email==data['email'],
    Merchant.shop_name==data['shop_name']).first()
    email = Merchant.query.filter(Merchant.email==data['email']).first()

    # print("debug!!!!",existing.id)
    if existing != None:
        print(existing.id)
        return 1
    elif email != None:
        print(email.id)
        return 2
    else:
        return False
def generate_id():
    id = str(uuid.uuid4())
    existing_C = Customer.query.filter(Customer.id == id ).first()
    existing_M = Merchant.query.filter(Customer.id == id ).first()

    return id if (existing_C == None or existing_M == None) else generate_id()

#not used for AWS
def create_person(client,person_name_at_bank_acc,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    new_person = client.person_group_person.create(PERSON_GROUP_ID, name=person_name_at_bank_acc)
    return new_person.person_id

def register_person(client,person_photo,person_name,bank_acc,bank_pin,bank_cvv,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    exist_person_list = client.person_group_person.list(PERSON_GROUP_ID)
    if (exist_person_list is not None):
        person_name_list = [x.name for x in exist_person_list]
        #print ("exist_person_list: " + str(person_name_list))
        if person_name not in person_name_list:
            add_new_person(client,person_photo,person_name,bank_acc,bank_pin,bank_cvv,PERSON_GROUP_ID=constant.PERSON_GROUP_ID)
        else:
            print ("Person " + str(person_name)+" already exists not need to create")

    #empty list
    else:
        add_new_person(client,person_photo,person_name,bank_acc,bank_pin,bank_cvv,PERSON_GROUP_ID=constant.PERSON_GROUP_ID)

def remove_person(client,person_id,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    new_person = client.person_group_person.delete(PERSON_GROUP_ID, person_id=person_id)

def person_id_map_name():
    return True

def update_person():
    return True

def add_new_person_photo(client,person_photo,person_name,bank_acc,bank_pin,bank_cvv,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    return True


def add_new_person(client,person_photo,person_name,bank_acc,bank_pin,bank_cvv,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    new_person = client.person_group_person.create(PERSON_GROUP_ID, name=person_name)

    new_person_images = [file for file in glob.glob('./register_photo/*.jpg') if file.startswith('./register_photo\\' + str(person_name))] #TODO consider person with same name
    #print (str(len(new_person_images)) + " images_file: ")
    #print ("images_file: " +str(new_person_images))
    for image in new_person_images:
        w = open(image, 'r+b')

        client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, new_person.person_id, w, name=person_name, user_data = bank_acc)
        #openCV
        # Load an color image in grayscale
        #img = cv2.imread(image,0)
        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    

