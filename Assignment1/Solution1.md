## ASSIGNMENT 1 - CloudFront CDN and S3 Bucket
##### AUTHOR - TANUJ ARORA
##### DATE - 19 July 2024
----
### Create a Bucket for Root Object
1. Upload the index.html in the root directory
![alt text](image-3.png)
![alt text](image-8.png)
### Create a second bucket for Devops-Folder
1. Create a devops-folder
2. Upload the index.html inside the devops-folder.
3. Make sure you have the public access disabled for security reasons.
![alt text](image-4.png)
![alt text](image-6.png)
![alt text](image-7.png)
4. Create a CloudFront Distribution
![alt text](image-9.png)
5. Add the root object for the distribution.
![alt text](image-10.png)
6. Add the origin for both S3 Buckets. 
![alt text](image-11.png)
7. Create an Origin access identity for the distribution
![alt text](image-12.png)
8. Add Behaviours for both the S3 Buckets.
![alt text](image-13.png)
![alt text](image-14.png)
9. For /devops-folder/ to direct to index.html file we need to create a lambda@edge function to update the request url.
```python
def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    uri = request['uri']
    if uri.endswith('/devops-folder/'):
        request['uri'] = uri + 'index.html'
    return request
test_event = {
    'Records': [{
        'cf': {
            'request': {
                'uri': '/devops-folder/'
            }
        }
    }]
}


# print(lambda_handler(test_event, None))

```
10. Create a new version for the edge function to be used.
![alt text](image-16.png)

11. Add the custom policy for the lambda function.
![alt text](image-17.png)
12. Update the Trust Relationships for the edge function.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com",
                    "edgelambda.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

## FINAL RESULT
#### BROWSER OUTPUT
##### Root object
![alt text](image-2.png)
##### Devops-Folder
![alt text](image-1.png)
#### CURL COMMAND
![alt text](image.png)