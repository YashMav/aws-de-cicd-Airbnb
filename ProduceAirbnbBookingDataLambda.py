import json
import random
import string
import boto3


def get_airbnb_data():
    return {
        "bookingId":''.join(random.choices(string.ascii_letters,k=6)).capitalize()+str(random.randint(100000,999999)),
        "userId":"ID"+str(random.randint(100000,999999)),
        "propertyId":"PRPID"+str(random.randint(100000,999999)),
        "location":random.choice(["CA,USA","BOM,IND","DEL,IND","BRU,BEL","PAR,FR","HUN,BUD"]),
        "startDate":random.choice(["2024-01-03","2024-01-04","2024-01-05","2024-01-07","2024-01-08","2024-01-06"]),
        "endDate":random.choice(["2024-01-03","2024-01-04","2024-01-05","2024-01-07","2024-01-08","2024-01-06"]),
        "price":random.randint(1,999999999)
    }


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    sqs_url = "https://sqs.ap-south-1.amazonaws.com/891376943331/AirbnbBookingQueue"
    for i in range(1,11):
        booking_data = get_airbnb_data()
        print(json.dumps(booking_data))
        sqs_client.send_message(QueueUrl=sqs_url,MessageBody=json.dumps(booking_data))
    return {
        'statusCode': 200,
        'body': json.dumps('Mock Airbnb booking data generated to sqs successfully.................')
    }
