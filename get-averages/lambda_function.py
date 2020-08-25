import requests
import json
from datetime import datetime
import boto3

def lambda_handler(event, context):
	x = requests.get('https://n831z3jc8h.execute-api.us-east-1.amazonaws.com/dev/get-sentiment?query=imran khan')
	result = x.text
	print(result)
	data = json.loads(result)
	
	sum = 0
	for item in data:
	    sum = sum + item["y"]
	
	
	avg = sum/len(data)
	
	print(str(datetime.now()) + ',' + str(avg))
	
	client = boto3.client('s3')
	obj = client.get_object(Bucket='tweet-averages-bucket',Key='imran khan.csv')
	old = obj['Body'].read().decode("utf-8")
	#print(old)
	entry = old + '\n' + str(datetime.now()) + ',' + str(avg)
	print(entry)
	client.put_object(Bucket='tweet-averages-bucket', Key='imran khan.csv', Body=entry)