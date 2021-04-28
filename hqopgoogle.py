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

def connect_websocket(url : str,url2 : str,url3 : str,token : str,cbc = None,cbc2 = None,cbc3 = None):
	hook = Webhook(url)
	hook2 = Webhook(url2)
	hook3 = Webhook(url3)
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
				qno = data["questionNumber"]
				totalq = data["questionCount"]
				question = str(question).replace(" ","+")
				answers = [unidecode(ans["text"]) for ans in data["answers"]]
				option1 = f"{answers[0]}"
				option2 = f"{answers[1]}"
				option3 = f"{answers[2]}"
				url="https://www.google.com/search?q=" + question
				embed = discord.Embed(title=f"**Question {qno} out of {totalq}**,description="",color=000000)
				embed.add_field(name=f"**{question}**",value=f"**[Search with options]({url}+{option1}+{option2}+{option3})**")
				embed.add_field(name="**Option 1**",value=f"**{option1}**")
				embed.add_field(name="**Option 2**",value=f"**{option2}**")
				embed.add_field(name="**Option 3**",value=f"**{option3}**") 
				embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/827177417092366396/834782681648595005/a7372eaaeafa289f28534ad39d96d517.gif")
				search = requests.get(url=url)
				searchop = requests.get(url=url + "+" + option1 + "+" + option2 + "+" + option3)
				res = str(search.text)
				resop = str(searchop.text)
				count1 = res.count(option1)
				count2 = res.count(option2)
				count3 = res.count(option3)
				countop1 = resop.count(option1)
				countop2 = resop.count(option2)
				countop3 = resop.count(option3)
				find1 = res.find(option1)
				find2 = res.find(option2)
				find3 = res.find(option3)
				embed = discord.Embed(title="**Google Results!**",url=url,description="",color=000000)
				embed.add_field(name="**__Search without options__**",value=f"**Option 1 : {count1}\nOption 2 : {count2}\nOption 3 : {count3}**")
				embed.add_field(name="**__Search with options__**",value=f"**Option 1 : {countop1}\nOption 2 : {countop2}\nOption 3 : {countop3}**")
				embed.add_field(name="**__Special Search__**",value=f"**Option 1 : {find1}\nOption 2 : {find2}\nOption 3 : {find3}**")
				embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/827177417092366396/834782681648595005/a7372eaaeafa289f28534ad39d96d517.gif")
				embed.set_author(name="HQ DUCK 🦆",icon_url="https://cdn.discordapp.com/attachments/827177417092366396/834785442003812402/IMG_20201114_151546.jpg")
				embed.set_footer(text="</> by Kumar Dhruv",icon_url="https://cdn.discordapp.com/attachments/827177417092366396/834785101153566720/IMG_20210130_095034.jpg")
				hook.send(cbc)
				hook.send(embed=embed)
				hook2.send(cbc2)
				hook2.send(embed=embed)
				hook3.send(cbc3)
				hook3.send(embed=embed)
				

while True:
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI2ODg5NDU2LCJ1c2VybmFtZSI6ImNoYWRMYW0iLCJhdmF0YXJVcmwiOiJodHRwczovL2Nkbi5wcm9kLmh5cGUuc3BhY2UvZGEvZ29sZC5wbmciLCJ0b2tlbiI6bnVsbCwicm9sZXMiOltdLCJjbGllbnQiOiJpUGhvbmU4LDIiLCJndWVzdElkIjpudWxsLCJ2IjoxLCJpYXQiOjE2MTkxMTE0MTUsImV4cCI6MTYyNjg4NzQxNSwiaXNzIjoiaHlwZXF1aXovMSJ9.jmRVRfC3TFsNz8WgMdPPtWS0NBjdH_nTxVoqsBmwWBs"
	url = "https://discord.com/api/webhooks/835083147761811467/4ZVK4BxJ_zIxgtG2zUtWoCabc13tp4aP0KA-LMfeAzliTDesgQrgw6JMtxbdeC3fjY0G"
	url2 = "https://discord.com/api/webhooks/763403798999203880/z-gW0sSMuKwjXKS8SfX6Q3mDRhXFiVMZFVovd3E5L75Xri0aTu3sM8Q99GPFj0UJcFed"
	url3 = "https://discord.com/api/webhooks/835764960344670228/B4F2PTg5FCNzyMhwudqtC3Oz0-vbvY6AMToIPm987IkBTWpO9keQ0CZMR1oqulNUI4He"
	if show_active():
		connect_websocket(url,url2,url3,token,"!duck","@duck","+mt")
	else:
		show_not_on()
		time.sleep(30)
