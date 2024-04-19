import json
import datetime

def lambda_handler(event, context):
    print(f"enrichment started ................")
    print(event)
    print(f"Messages received in this queue batch is : {len(event)}")
    new_event=[]
    try:
        for record in event:
            # print((record['body']))
            row =  json.loads(record['body'])
            print(row)
            # checking if the duration of the booking is more than a day , if yes the record is discarded !!!!
            start_date = datetime.datetime.strptime(row['startDate'],'%Y-%m-%d')
            end_date = row['endDate']+' 23:59:59'
            end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
            # print(f"start date - {start_date} , end date - {end_date}")
            if (end_date-start_date).total_seconds() > 86400:
                print("The duration of booking is more than  1 day , so record will be processed......")
                new_event.append(row)

            else:
                print(f"The record with booking id {row['bookingId']} is discarded as booking is less than or equal to 1 day..........")
        return {
            'message':new_event
        }
    except Exception as e:
        return {'message' : str(e)}
