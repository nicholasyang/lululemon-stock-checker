from bs4 import BeautifulSoup
import requests
import boto3

def run(event, context):
	response = requests.get("https://shop.lululemon.com/p/mens-trousers/ABC-Pant-Slim-30/_/prod9610173?color=0001&sz=28")
	soup = BeautifulSoup(response.text, features="html.parser")
	sns_client = boto3.client("sns")

	if soup.find("div", string="Sold out online.") == None:
		sns_client.publish(
			TopicArn="arn:aws:sns:us-east-1:259356154792:lululemon-in-stock-notification",
			Message="It's in stock!",
			Subject="Lululemon in stock alert!"
		)
		print("It's in stock!")
	else:
		print("Not in stock.")
