import csv
import boto3
import base64
from botocore.exceptions import ClientError

#从本地joe.csv read aws key
#key 是存在csv里， 也可以写入flask环境变量
with open('joe.csv','r') as input:
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
    test_byte =b'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'

    with open (photo,'rb') as source_image:
        source_bytes = source_image.read()
        source_bytes = base64.b64encode(source_bytes)
        print(source_bytes)
        source_bytes = base64.b64decode(source_bytes)
        print(source_bytes)
        test_byte = base64.b64decode(test_byte)

    threshold = 70
    maxFaces=2


  
    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'Bytes': source_bytes},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    return response['FaceMatches']


def main():
    #本地读取图片
    collection_id='Test_Collection'
    photo = 'C:/capstone/Facewallet_fork/AWS_Rekognition/obama.jpg'
    '''
    collection_id='Test_Collection'
    create_collection(collection_id)
    collection_count=list_collections()
    print("collections: " + str(collection_count))
    '''
    '''
    collection_id='Test_Collection'
    describe_collection(collection_id)
    '''
    '''
    status_code=delete_collection(collection_id)
    print('Status code: ' + str(status_code))'''

    collection_id='Test_Collection'
    photo = 'C:/capstone/Facewallet_fork/AWS_Rekognition/yunan_test3.jpg'


    '''
    indexed_faces_count=add_faces_to_collection(photo,'trump',collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))
    '''

    faces_count=list_faces_in_collection(collection_id)
    print("faces count: " + str(faces_count))


    '''
    faceMatches=search_face_in_collection(photo,collection_id)
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print
    '''
    


if __name__ == "__main__":
    main()    


