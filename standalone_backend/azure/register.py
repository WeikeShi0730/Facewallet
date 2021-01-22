import glob
import time
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

def remove_person(client,person_id,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    new_person = client.person_group_person.delete(PERSON_GROUP_ID, person_id=person_id)


