from bs4 import BeautifulSoup
import requests
import boto3

TABLE = "lululemon-stock-checker-items"
SNS_TOPIC = "arn:aws:sns:us-east-1:259356154792:lululemon-stock-checker-notification"

def run(event, context):
	dynamo_client = boto3.resource("dynamodb")
	table = dynamo_client.Table(TABLE)
	table_scan = table.scan()
	items = table_scan["Items"]

	for item in items:
		response = requests.get(item["url"])
		soup = BeautifulSoup(response.text, features="html.parser")

		if soup.find("div", string="Sold out online.") == None:
			sns_client = boto3.client("sns")
			sns_client.publish(
				TopicArn=SNS_TOPIC,
				Subject=f'{item["name"]} in stock!',
				Message=f'Link: {item["url"]}'
			)
			print(f'{item["name"]} in stock! :)')
		else:
			print(f'{item["name"]} not in stock :(')
