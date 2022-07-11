from bs4 import BeautifulSoup
import requests
import boto3

def run(event, context):
	dynamo_client = boto3.client("dynamodb")
	items = dynamo_client.scan(
		TableName="lulu_items"
	)

	for item in items["Items"]:
		response = requests.get(item["url"]["S"])
		soup = BeautifulSoup(response.text, features="html.parser")

		if soup.find("div", string="Sold out online.") == None:
			sns_client = boto3.client("sns")
			sns_client.publish(
				TopicArn="arn:aws:sns:us-east-1:259356154792:lululemon-in-stock-notification",
				Message=f'{item["item"]["S"]} in stock!',
				Subject=f'Link: {item["url"]["S"]}',
			)
			print(f'{item["item"]["S"]} in stock! :)')
		else:
			print(f'{item["item"]["S"]} not in stock :(')
