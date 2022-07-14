from bs4 import BeautifulSoup
import requests
import boto3

TABLE = "lululemon-stock-checker-items"
SNS_TOPIC = "arn:aws:sns:us-east-1:259356154792:lululemon-stock-checker-notification"

def run(event, context):
	dynamo_client = boto3.client("dynamodb")
	items = dynamo_client.scan(
		TableName=TABLE
	)

	for item in items["Items"]:
		response = requests.get(item["url"]["S"])
		soup = BeautifulSoup(response.text, features="html.parser")

		if soup.find("div", string="Sold out online.") == None:
			sns_client = boto3.client("sns")
			sns_client.publish(
				TopicArn=SNS_TOPIC,
				Subject=f'{item["name"]["S"]} in stock!',
				Message=f'Link: {item["url"]["S"]}'
			)
			print(f'{item["name"]["S"]} in stock! :)')
		else:
			print(f'{item["name"]["S"]} not in stock :(')
