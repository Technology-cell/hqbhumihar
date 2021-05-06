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

def connect_websocket(url : str,url2 : str,url3 : str,token : str,cbc = None):
	marvel = Webhook(url)
	fetch = Webhook(url2)
	mafia = Webhook(url3)
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
				questio = data["question"]
				qno = data["questionNumber"]
				totalq = data["questionCount"]
				question = str(questio).replace(" ","+")
				answers = [unidecode(ans["text"]) for ans in data["answers"]]
				answersid = [answer["answerId"] for answer in data["answers"]]
				option1 = f"{answers[0]}"
				option2 = f"{answers[1]}"
				option3 = f"{answers[2]}"
				op1 = option1.replace(" ","+")
				op2 = option2.replace(" ","+")
				op3 = option3.replace(" ","+")
				url="https://www.google.com/search?q=" + question
				embed = discord.Embed(title=f"**Question {qno} out of {totalq}**",description=f"**[{questio}]({url})\n\n[Search with options]({url}+{op1}+{op2}+{op3})**",color=000000)
				embed.add_field(name="**Option 1**",value=f"**[{option1}]({url}+{op1})**")
				embed.add_field(name="**Option 2**",value=f"**[{option2}]({url}+{op2})**")
				embed.add_field(name="**Option 3**",value=f"**[{option3}]({url}+{op3})**")
				embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
				marvel.send(embed=embed)
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
				embed.set_author(name="HQ Trivia",icon_url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
				embed.set_footer(text="</> by Kumar Dhruv",icon_url="https://cdn.discordapp.com/attachments/827177417092366396/834785101153566720/IMG_20210130_095034.jpg")
				marvel.send(cbc)
				marvel.send(embed=embed)
				mafia.send(cbc)
				mafia.send(embed=embed)
			if data["type"] == "answered":
				name = data["username"]
				answer = data["answerId"]
				if name == "rosemiya":
					uname = "Marvel Owner"
				if name == "Lucas8002":
					uname = "Kumar Dhruv"
				if name == "elisabenson35":
					uname = "Don Uday Bhai"
				if name == "lunisiko":
					uname = "VermA"
				if name == "vitkar2":
					uname = "K.D."
				if name == "tesla1999":
					uname = "Spiderman 1"
				if name == "teslahero04":
					uname = "Spiderman 2"
				if name == "darrymask":
					uname = "Spiderman 3"
				if name == "GretlLeda65":
					uname = "Legend"
				if name == "Itzmeloll":
					uname = "Finishhh"
				if name == "maxvinila":
					uname = "R K"
				if answer == answersid[0]:
					embed = discord.Embed(title=f"**Marvel Friends**",description=f"**{uname} went option :one:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					marvel.send(embed=embed)
					fetch.send("w1")
				if answer == answersid[1]:
					embed = discord.Embed(title=f"**Marvel Friends**",description=f"**{uname} went option :two:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					marvel.send(embed=embed)
					fetch.send("w2")
				if answer == answersid[2]:
					embed = discord.Embed(title=f"**Marvel Friends**",description=f"**{uname} went option :three:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					marvel.send(embed=embed)
					fetch.send("w3")
			if data["type"] == "questionSummary":
				correct = ""
				opno = ""
				if option1 == correct:
					opno = "Option :one:"
				if option2 == correct:
					opno = "Option :two:"
				if option3 == correct:
					opno = "Option :three:"
				for answer in data["answerCounts"]:
					ans_str = unidecode(answer["answer"])
					if answer["correct"]:
						correct = ans_str
				advancing = data["advancingPlayersCount"]
				eliminated = data["eliminatedPlayersCount"]
				paysum = (5000)/(int(advancing))
				payout = float("{:.2f}".format(paysum))
				embed = discord.Embed(title="**Question Summary**",description="",color=000000)
				embed.add_field(name="**Correct Answer :-**",value=f"**{opno}.{correct}**")
				embed.add_field(name="**Stats :-**",value=f"**• Advancing Players : {advancing}\n• Eliminated Players : {eliminated}\• Current Payout : ${payout}**")
				hook.send(embed=embed)

			if data["type"] == "gameSummary":
				winners = data["numWinners"]
				payout = str(data["winners"][0]["prize"])
				print(f"Winners : {winners}\nPayout : {payout}")

while True:
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI2ODg5NDU2LCJ1c2VybmFtZSI6ImNoYWRMYW0iLCJhdmF0YXJVcmwiOiJodHRwczovL2Nkbi5wcm9kLmh5cGUuc3BhY2UvZGEvZ29sZC5wbmciLCJ0b2tlbiI6bnVsbCwicm9sZXMiOltdLCJjbGllbnQiOiJpUGhvbmU4LDIiLCJndWVzdElkIjpudWxsLCJ2IjoxLCJpYXQiOjE2MTkxMTE0MTUsImV4cCI6MTYyNjg4NzQxNSwiaXNzIjoiaHlwZXF1aXovMSJ9.jmRVRfC3TFsNz8WgMdPPtWS0NBjdH_nTxVoqsBmwWBs"
	url = "https://discord.com/api/webhooks/835764960344670228/B4F2PTg5FCNzyMhwudqtC3Oz0-vbvY6AMToIPm987IkBTWpO9keQ0CZMR1oqulNUI4He"
	url2 = "https://discord.com/api/webhooks/838271937888780318/jUoH7tbiyE6PZS-FMj34EBJM7CjY0S1NDgiipf_xd36kkbTMoc3ouQyIAMU2EJV6gH01"
	url3 = "https://discord.com/api/webhooks/835083147761811467/4ZVK4BxJ_zIxgtG2zUtWoCabc13tp4aP0KA-LMfeAzliTDesgQrgw6JMtxbdeC3fjY0G"
	if show_active():
		connect_websocket(url,url2,url3,token,"+mt")
	else:
		show_not_on()
		time.sleep(30)
