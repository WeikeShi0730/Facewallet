import constant
import time
from main import TrainingStatusType
def list_out_person_group(client):
    person_group_list = client.person_group.list()
    print ("existing person group: \n")
    for x in person_group_list:
        print (x)
    print ("\n\n")

def get_person_group(client,person_group_name):
    get_result = client.person_group.get(person_group_id=person_group_name, name=person_group_name)
    return get_result
        

def delete_person_group(client,person_group_name):
    client.person_group.delete(person_group_id=person_group_name, name=person_group_name)

def create_person_group(client,person_group_name):
    list_existing_person_group = client.person_group.list()
    if (list_existing_person_group is not None):
        person_groups = [x.person_group_id for x in list_existing_person_group]
        print ("exist_person_groups: " + str(person_groups))
        if person_group_name not in person_groups:
            client.person_group.create(person_group_id=person_group_name, name=person_group_name,recognition_model='recognition_03')
        else:
            print ("Group " + str(person_group_name)+" already exists not need to create")
    #empty list
    else:
        client.person_group.create(person_group_id=person_group_name, name=person_group_name,recognition_model='recognition_03')
    
def list_out_person(client,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    person_list = client.person_group_person.list(PERSON_GROUP_ID)
    print ("existing person: \n")
    for x in person_list:
        print (x)
    print ("\n\n")

def train_person_group(client,PERSON_GROUP_ID=constant.PERSON_GROUP_ID):
    print('Training the person group...')
    # Train the person group
    train_start_time = time.time()
    client.person_group.train(PERSON_GROUP_ID)
    while (True):
        training_status = client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(1)
    train_end_time = time.time()
    print ("training take {}. ".format(train_end_time-train_start_time))