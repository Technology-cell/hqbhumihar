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

def connect_websocket(url : str,url2 : str,url3 : str,url4 : str,token : str):
	ancient = Webhook(url)
	fetch = Webhook(url2)
	challenge = Webhook(url3)
	wiki = Webhook(url4)
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
				answersid = [answer["answerId"] for answer in data["answers"]]
			if data["type"] == "answered":
				name = data["username"]
				answer = data["answerId"]
				bestie = ["QuincyNicolas","Liam9708","Dunbar151","Jack-hunter88"]
				if name == "Shimmer8":
					uname = "Only Fun"
				if name == "Jack-hunter88":
					uname = "Kuna"
				if name == "QuincyNicolas":
					uname = "Most Trusted Friend"
				if name == "Liam9708":
					uname = "Dev Friend"
				if name == "Dunbar151":
					uname = "Kalua Friend"
				if name == "larkinfeli":
					uname = "Friend"
				if answer == answersid[0]:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{uname} went option :one:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					embed = discord.Embed(title=f"**Ancient Friends**",description=f"**{name} went option :one:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					if name in bestie:
						ancient.send(embed=embed)
						wiki.send("1c")
					fetch.send("w1")
				if answer == answersid[1]:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{uname} went option :two:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					embed = discord.Embed(title=f"**Ancient Friends**",description=f"**{name} went option :two:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					if name in bestie:
						ancient.send(embed=embed)
						wiki.send("2c")
					fetch.send("w2")
				if answer == answersid[2]:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{uname} went option :three:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					embed = discord.Embed(title=f"**Ancient Friends**",description=f"**{name} went option :three:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					if name in bestie:
						ancient.send(embed=embed)
						wiki.send("3c")
					fetch.send("w3")
					
while True:
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI3MzExMDU1LCJ1c2VybmFtZSI6IlNhcmlmNmdhZDMwIiwiYXZhdGFyVXJsIjoiaHR0cHM6Ly9jZG4ucHJvZC5oeXBlLnNwYWNlL2RhL2dyZWVuLnBuZyIsInRva2VuIjoiRWEwTHFxIiwicm9sZXMiOltdLCJjbGllbnQiOiJBbmRyb2lkLzEuNTIuMyIsImd1ZXN0SWQiOm51bGwsInYiOjEsImlhdCI6MTYxNTAzNTU5NiwiZXhwIjoxNjIyODExNTk2LCJpc3MiOiJoeXBlcXVpei8xIn0.HQ32U49H_gzV-7-93XSwsJaj1qXaaAwUfkkHXnHHGPk"
	url = "https://discord.com/api/webhooks/841643870042849341/bjyT1dKqVchWdhay1G0hyVcUFr2YneFY3J7ydgOWDUHXLgVDjGkDLbNuoS9qVUFD5HEV"
	url2 = "https://discord.com/api/webhooks/838271937888780318/jUoH7tbiyE6PZS-FMj34EBJM7CjY0S1NDgiipf_xd36kkbTMoc3ouQyIAMU2EJV6gH01"
	url3 = "https://discord.com/api/webhooks/848013930252337183/9c33_Jpk3-suOWkJE-gJP46hxEEqVxmp4r5FsEMFOdSVPXXWGZfxQFIl5gd9t0zk28en"
	url4 = "https://discord.com/api/webhooks/847470950442205224/ZKbwurLcLQycy7r9ci_dpgs28yzuY2uOa1S75pH1BLcTjzwV4QYdqZ0ZAzkAeG5Ju9gN"
	if show_active():
		connect_websocket(url,url2,url3,url4,token)
	else:
		show_not_on()
		time.sleep(30)
