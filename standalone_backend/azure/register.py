import glob
import time
import numpy as np
import cv2
import constant


def check_person_exist(client,person_name_at_bank_acc,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    exist_person_list = client.person_group_person.list(PERSON_GROUP_ID)
    if (exist_person_list is not None):
        person_name_list = [x.name for x in exist_person_list]
        #print ("exist_person_list: " + str(person_name_list))
        if person_name_at_bank_acc not in person_name_list:
            return False
        else:
            #print ("Person " + str(person_name_at_bank_acc)+" already exists not need to create")
            return True
    else:
        return False

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
    

