import csv
import boto3
import base64
from botocore.exceptions import ClientError

#从本地joe.csv read aws key
#key 是存在csv里， 也可以写入flask环境变量
with open('C:/Users/z9132/Desktop/level-4\capstone/AWS/new_user_credentials.csv','r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]
client = boto3.client('rekognition', region_name='us-east-2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
'''
#简单识别sample
photo = 'C:/capstone/Facewallet_fork/AWS_Rekognition/???.jpg'
client = boto3.client('rekognition')
with open (photo,'rb') as source_image:
    source_bytes = source_image.read()
response = client.detect_faces(
    Image = {'Bytes': source_bytes}
    )
'''
def create_collection(collection_id):


    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

def list_collections():

    max_results=2
    


    #Display all the collections
    print('Displaying collections...')
    response=client.list_collections(MaxResults=max_results)
    collection_count=0
    done=False
    
    while done==False:
        collections=response['CollectionIds']

        for collection in collections:
            print (collection)
            collection_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_collections(NextToken=nextToken,MaxResults=max_results)
            
        else:
            done=True

    return collection_count   


def describe_collection(collection_id):

    print('Attempting to describe collection ' + collection_id)


    try:
        response=client.describe_collection(CollectionId=collection_id)
        print("Collection Arn: "  + response['CollectionARN'])
        print("Face Count: "  + str(response['FaceCount']))
        print("Face Model Version: "  + response['FaceModelVersion'])
        print("Timestamp: "  + str(response['CreationTimestamp']))

        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
    print('Done...')

def delete_collection(collection_id):


    print('Attempting to delete collection ' + collection_id)

    status_code=0
    try:
        response=client.delete_collection(CollectionId=collection_id)
        status_code=response['StatusCode']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        status_code=e.response['ResponseMetadata']['HTTPStatusCode']
    return(status_code)


def add_faces_to_collection(photo,photo_name,collection_id):


    with open (photo,'rb') as source_image:
        source_bytes = source_image.read()

    response=client.index_faces(CollectionId=collection_id,
                                Image={'Bytes': source_bytes},
                                ExternalImageId=photo_name,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo_name) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

def delete_faces_from_collection(collection_id, faces):



    response=client.delete_faces(CollectionId=collection_id,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)
    return len(response['DeletedFaces'])

def list_faces_in_collection(collection_id):


    maxResults=2
    faces_count=0
    tokens=True


    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    print('Faces in collection ' + collection_id)

 
    while tokens:

        faces=response['Faces']

        for face in faces:
            print (face)
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
    return faces_count 

def search_face_in_collection(photo,collection_id):

    collectionId=collection_id
    #test_byte =

    with open (photo,'rb') as source_image:
        source_bytes = source_image.read()
        '''
        source_bytes = base64.b64encode(source_bytes)
        print(source_bytes)
        source_bytes = base64.b64decode(source_bytes)
        print(source_bytes)
        '''
        #test_byte = base64.b64decode(test_byte)

    threshold = 70
    maxFaces=2


  
    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'Bytes': source_bytes},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    return response['FaceMatches']


def main():
    
    collection_id='Test_Collection'
    ###本地读取图片
    #photo = 'C:/capstone/Facewallet_fork/AWS_Rekognition/obama.jpg'

    '''
    ###
    create_collection(collection_id)
    collection_count=list_collections()
    print("collections: " + str(collection_count))
    '''

    '''
    ###display  collection info
    collection_id='Test_Collection'
    describe_collection(collection_id)
    '''

    '''
    ###delete collection
    status_code=delete_collection(collection_id)
    print('Status code: ' + str(status_code))
    '''

    '''
    ###add face to collection
    indexed_faces_count=add_faces_to_collection(photo,'trump',collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))
    '''
    
    '''
    ###count faces in the collection 
    faces_count=list_faces_in_collection(collection_id)
    print("faces count: " + str(faces_count))
    '''

    '''
    ### face search
    faceMatches=search_face_in_collection(photo,collection_id)
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print
    '''
    


if __name__ == "__main__":
    main()    


