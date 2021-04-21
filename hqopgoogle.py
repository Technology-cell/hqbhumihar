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

def connect_websocket(url : str,token : str,cbc = None):
	hook = Webhook(url)
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
				question = str(question).replace(" ","+")
				answers = [unidecode(ans["text"]) for ans in data["answers"]]
				option1 = f"{answers[0]}"
				option2 = f"{answers[1]}"
				option3 = f"{answers[2]}"
				url="https://www.google.com/search?q=" + question
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
				embed = discord.Embed(title="**Google Results!**",description="",color=000000)
				embed.add_field(name="**__Search without options__**",value=f"**Option 1 : {count1}\nOption 2 : {count2}\nOption 3 : {count3}**")
				embed.add_field(name="**__Search with options__**",value=f"**Option 1 : {countop1}\nOption 2 : {countop2}\nOption 3 : {countop3}**")
				embed.add_field(name="**__Special Search__**",value=f"**Option 1 : {find1}\nOption 2 : {find2}\nOption 3 : {find3}**")
				hook.send(embed=embed)
				if cbc == None:
					print("No Crowd Command Found")
				else:
					hook.send(cbc)

while True:
	token = ""
	url = ""
	if show_active(token):
		connect_websocket(url,token,"duck")
	else:
		show_not_on()
		time.sleep(30)