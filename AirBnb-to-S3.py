import csv
import boto3
import datetime
import json
import pandas as pd


def lambda_handler(event, context):
    print(f"event--> {event}")
    records = event[0]['message']
    header_cols = ['bookingId' , 'userId','propertyId','location','startDate','endDate','price']

    d_date = datetime.datetime.today()
    d_date=d_date.strftime('%Y%m%d')
    print(d_date)
    bucket_name = "aws-de-1-airbnb-booking-records"
    key = f"{d_date}/airbnb_processed_date_{d_date}.csv"


    s3_client = boto3.client('s3')
    s3_trg = boto3.resource('s3')
    bucket_trg = s3_trg.Bucket(bucket_name)
    try:
        s3_read = s3_client.get_object(Bucket=bucket_name,Key=key)
        file_body = s3_read['Body']
        # read_file = s3_read['Body'].read().decode('utf-8')
        # print(f"fileread---->{read_file}")
        df = pd.read_csv(file_body)
        df.set_index('bookingId',inplace=True)
        # print(df)
        for row in records:
            df.loc[row['bookingId']] = [row['userId'],row['propertyId'],row['location'],row['startDate'],row['endDate'],row['price']]
        print("Creating /tmp/temp.csv...........")
        df.to_csv('/tmp/temp.csv')
        bucket_trg.upload_file('/tmp/temp.csv' , key)
    except s3_client.exceptions.NoSuchKey:
        print(f"{bucket_name}://{key} does not exist !!!!")
        df = pd.DataFrame(columns=header_cols)
        df.set_index('bookingId',inplace=True)
        for row in records:
            df.loc[row['bookingId']] = [row['userId'],row['propertyId'],row['location'],row['startDate'],row['endDate'],row['price']]
        print("Creating /tmp/temp.csv...........")
        df.to_csv('/tmp/temp.csv')
        bucket_trg.upload_file('/tmp/temp.csv' , key)



    return {
        'statusCode': 200,
        'body': json.dumps('File generation to s3 successful !!!!!!')
    }
