Creating a serverless web application using AWS Lambda, DynamoDB, S3, and IAM (Identity and Access Management) involves several steps. Below is a high-level overview of the process:

# 1. **AWS-Account:**
   - Make sure you have an AWS account. If not, sign up for one at https://aws.amazon.com/.

## 2. **IAM Roles:**
   - Set up IAM roles to define permissions for your AWS Lambda functions to interact with other AWS services. Ensure that your roles have the necessary permissions to access DynamoDB, S3, and other resources.
  ![IAM role](IAM.png)

### 3. **AWS Lambda:**
   - Create Lambda functions to handle different parts of your application.
   - Define the function code (e.g., Node.js, Python, Java).
   - Configure Lambda triggers (e.g., API Gateway, S3 events) to invoke your functions.

```
```
```python
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
  

```
*Demo Picture:* ![demo picture](aws%20lambda.png)

#### 4. **DynamoDB:**
   - Create a DynamoDB table to store data for your application.
   - Define the table schema and primary key(s).

##### 5. **S3:**
   - Set up an S3 bucket to store static assets (HTML, CSS, JavaScript, etc.) and other files.
   - Configure permissions to allow public access to necessary files if your web application requires it.
  
  ~***Html code for S3 bucket***~
```html
 > ><!DOCTYPE html>

```<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post Box</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url("https://contactlamb.s3.eu-west-1.amazonaws.com/employe_communication.gif");
            background-size: cover; /* Adjust as needed */
            background-position: center center; /* Adjust as needed */
            background-repeat: no-repeat;
           
        }
        .post-box {
            width: 400px;
            margin: 20px auto;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        label {
            display: block;
            margin-bottom: 8px;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>    
</head>
<body>
    <header>
        <h1>Communication-Box</h1>
    </header>
    <main>  
        <h2>Welcome to Our Communication-Box</h2>
        <p>Unleash your thoughts, share your stories, and connect with the world.</p>
    </main>
    <div class="post-box">
        <h2>Create a New Contact</h2>
        <form id="post-box" method="POST">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>

            <label for="email">email:</label>
            <input type="email" id="email" name="email" required><br><br>

            <label for="postContent">postContent:</label>
            <textarea id="postContent" name="postContent" rows="4" cols="50" required></textarea><br><br>
 
            <input type="submit" value="Submit">
        </form>
    </div> 
    <script>
        document.getElementById("post-box").addEventListener("submit", function(event) {
         event.preventDefault(); // Prevent form submission
             
        // Serailize form data into JSON
         var formData = {
         name: document.getElementById("name").value,
         email: document.getElementById("email").value,
         postContent: document.getElementById("postContent").value
        };
        var jsonData = JSON.stringify (formData);
            
        // Send Json payload to the endpoint
        fetch( "https://w1lur9xwkk.execute-api.eu-west-1.amazonaws.com/default/contactfunction",{
        method: "POST",
        body: jsonData
        })
       .then(Response => {
           if (Response.ok) {
             alert("form submitted successfully");
        // Perform any desired actions upon successfull form submission
            } else {
               alert("Form subbmission failed");
        // Handle the failure scenario
            }
        })   
        .catch(Error => {
           console.error("An error occurred:", error);
        //Handle any error that occurred during the form submission
        });

        });
    </script> 
           
    <footer>
        &copy; 2023 Your Website. All rights reserved.
    </footer>
  
</body>
</html>
``` 

###### 6. **API Gateway:**
   - If your web application requires API endpoints, set up API Gateway to trigger your Lambda functions.

###### 7. **Connecting Components:**
   - Configure the necessary permissions in IAM to allow Lambda functions to interact with DynamoDB, S3, SNS and any other services you're using.

# 8. **Testing:**
   - Test your Lambda functions, DynamoDB, and S3 interactions locally before deploying.

# 9. **Deployment:**
   - Deploy your Lambda functions, DynamoDB table, and S3 bucket using AWS CloudFormation, Serverless Framework, or other deployment tools.

# 10. **Monitoring and Logging:**
    - Set up CloudWatch Alarms and Logging for monitoring and debugging purposes.

# 11.  **Scaling:**
    - Consider configuring auto-scaling options for your Lambda functions based on demand.

# 12. **Security:**
    - Ensure your web application follows security best practices. This includes securing your API Gateway, handling sensitive information securely, and using HTTPS.

# 13. **Custom Domain (Optional):**
    - If desired, set up a custom domain for your web application using AWS Route 53 or a third-party domain registrar.

# 14. **CDN (Optional):**
    - Consider using AWS CloudFront or another Content Delivery Network (CDN) for better performance and scalability.


Remember to refer to the official AWS documentation for each service to get detailed information and best practices. Additionally, consider using infrastructure-as-code tools like AWS CloudFormation or the Serverless Framework for easier management and deployment of your serverless application.

|  Result: ![result](demo.png)

|  website: [link](https://contactlamb.s3.eu-west-1.amazonaws.com/index.html)

# Context

[1-Aws Account](#1-aws-account)\
[2-IAM roles](#2-iam-roles)\
[3-Aws Lambda](#3-aws-lambda)\
[4-DynamoDB](#4-dynamodb)\
[5-S3](#5-s3)\
[6-API Gateway](#6-api-gateway)\
[7-Connecting Components](#7-connecting-components)\
[8-Testing](#8-testing)\
[9-Deployment](#9-deployment)\
[10-Monitoring and Logging](#10-monitoring-and-logging)\
[11-Scaling](#11-scaling)\
[12-Security](#12-security)\
[13-Custom Domain](#13-custom-domain-optional)
[14-CDN](#14-cdn-optional)

