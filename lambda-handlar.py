  import json
  import boto3
 from datetime import datetime 

def lambda_handler(event, context):
    # TODO implement
    db = boto3.resource('dynamodb')
    table = db.Table('contactinfo')
    ses = boto3.client('ses')
    print(f"Event: {event}")


```   payload = json.loads(event['body'])
    
    timestamp = datetime.now().strftime("%Y-%m-%d- %H:%M:%S")
    name = payload['name']
    email = payload['email']
    postContent = payload['postContent']
    print(f"name: {name}, email: {email}, postContent: {postContent}")
   
    #Prepare email
    body = f"""
        Contact Information:
        Name: {name}
        email: {email}
        postContent: {postContent}
        """
    try:
        table.put_item(
              Item={
                   'timestamp': timestamp,
                   'name': name,
                   'email': email,
                   'postContent': postContent
                }
        )
        
        ses.send_email(
            Source = 'amna.sohail.25@gmail.com',
            Destination = {
              'ToAddresses': [
                  'amnasohail25@yahoo.com'
                ]
            },
            Message = {
              'Subject': {
                'Data': 'Contact Information',
                'Charset': 'UTF-8'
               },
                'Body': {
                   'Text':{
                      'Data': body,
                      'Charset': 'UTF-8'
                    }
               }
             }        
        )      

        return {
           'statusCode': 200,
           'body': json.dumps('Successfully data stored in DB'),
           'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            }
        }
    except:
        return {
           'statusCode': 400,
           'body': json.dumps('Error occur in data stored'),
           'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            }
        }
  
