import glob
import numpy as np
import cv2


def verify_payment(client,verify_photo="verify",PERSON_GROUP_ID='prototype_group'):
    #only take single photo for now
    new_person_images = glob.glob('./validation_set\\'+str(verify_photo)+'.jpg')
    print (str(len(new_person_images)) + " images_file: ")
    print ("images_file: " +str(new_person_images))
    for image in new_person_images:
        w = open(image, 'r+b')

        #openCV
        # Load an color image in grayscale
        #img = cv2.imread(image,0)
        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        # Detect faces
        face_ids = []
        faces = client.face.detect_with_stream(w,recognition_model='recognition_03')
        for face in faces:
            face_ids.append(face.face_id)
            print('face ID in faces {}.\n'.format(face.face_id)) 
        if (len(face_ids) == 0):
            print ("No face detected in this verify image")
        elif (len(faces) > 1):
            print ("More than 1 faces detected in this verify image. Please retake the photo")
        else:
            results = client.face.identify(face_ids,PERSON_GROUP_ID)
            if not results:
                print('No person in this database matched with this verification')
            else:
                for each_verify_face in results:
                    #print (each_verify_face)
                    if (len(each_verify_face.candidates) == 0):
                        print('No candidates person in this database matched with this verification')
                    else :
                        for possible in each_verify_face.candidates:
                            print (possible)
                            possible_person_name = client.person_group_person.get(PERSON_GROUP_ID,possible.person_id).name
                            print('Person name {} with person_id {} matched with this cerification with a confidence of {}.'.format(possible_person_name, possible.person_id, possible.confidence)) 
