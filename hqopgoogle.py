from dhooks import Webhook
from lomond import WebSocket
import time
import json
from unidecode import unidecode
import discord
import requests

def show_not_on():
	url = "https://api-quiz.hype.space/shows/now"
	response = requests.get(url=url).json()
	if "broadcast" not in response or response["broadcast"] is None:
		if "error" in response and response["error"] == "Auth not valid":
			raise RuntimeError("Invalid Bearer")
		else:
			print("Game is not live")

def show_active():
	url = "https://api-quiz.hype.space/shows/now"
	response = requests.get(url=url).json()
	return response["active"]

def connect_websocket(url : str,url2 : str,token : str):
	challenge = Webhook(url)
	fetch = Webhook(url2)
	headers = {"Authorization": f"Bearer {token}"}
	url = requests.get(url="https://api-quiz.hype.space/shows/now").json()["broadcast"]["socketUrl"].replace("https","wss")
	websocket = WebSocket(url)
	for header, value in headers.items():
		websocket.add_header(str.encode(header), str.encode(value))
	for msg in websocket.connect(ping_rate=5):
		if msg.name == "text":
			message = msg.text
			data = json.loads(message)
			if data["type"] == "question":
				question = data["question"]
				answersid = [answer["answerId"] for answer in data["answers"]]
			if data["type"] == "answered":
				name = data["username"][0:5]
				answer = data["answerId"]
				if answer == answersid[0]:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{name} went option :one:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					fetch.send("w1")
				if answer == answersid[1]:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{name} went option :two:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					fetch.send("w2")
				if answer == answersid[2]:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{name} went option :three:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					fetch.send("w3")
					
while True:
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI3Mzk3NDI3LCJ1c2VybmFtZSI6InNoYWhpZGFtdSIsImF2YXRhclVybCI6Imh0dHBzOi8vY2RuLnByb2QuaHlwZS5zcGFjZS9kYS9nb2xkLnBuZyIsInRva2VuIjoibXJkRDQyIiwicm9sZXMiOltdLCJjbGllbnQiOiJpT1MvMS43LjQgYjAiLCJndWVzdElkIjpudWxsLCJ2IjoxLCJpYXQiOjE2MTczNzY1OTAsImV4cCI6MTYyNTE1MjU5MCwiaXNzIjoiaHlwZXF1aXovMSJ9.L0bNNH0gbAWT4h43XlI2P-0HVBg1xVG77NZ6auq3wkY"
	url = "https://discord.com/api/webhooks/834267847701954560/waz7W0RaKkIJzF5sEJDAd3mtE5YmmbAO1hTlRq_AiaD_pqJ31aucEFl18npKeA5L5fzy"
	url2 = "https://discord.com/api/webhooks/838271937888780318/jUoH7tbiyE6PZS-FMj34EBJM7CjY0S1NDgiipf_xd36kkbTMoc3ouQyIAMU2EJV6gH01"
	if show_active():
		connect_websocket(url,url2,token)
	else:
		show_not_on()
		time.sleep(30)
