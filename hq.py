import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601
import aiohttp
import asyncio
otp1 = []
otp2 = []
otp3 = []
trickdata = []
prizdata = []

webhook_url="https://discord.com/api/webhooks/840991903162957864/w_poXWoDETQvt8c_nVoyIj_SW524h4iu9nZs1O0qe4mN8c-KxETLCAXX5ft9Ehf_gDDI"

try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")
    
async def google(question,o1,o2,o3):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    url = f"https://google.com/search?q={question}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url,headers=head) as r:
            bsd = BeautifulSoup(await r.text(),'html.parser')
            divs = bsd.find_all('div')
            span = bsd.find_all('span')
            anc = bsd.find_all('a')
            for data1 in divs:
                ddt1 = data1.get_text()
                a = ddt1.count(o1)
                otp1.append(int(a))
                b = ddt1.count(o2)
                otp2.append(int(b))
                c = ddt1.count(o3)
                otp3.append(int(c))
            for data2 in span:
                ddt2 = data2.get_text()
                a = ddt2.count(o1)
                otp1.append(int(a))
                b = ddt2.count(o2)
                otp2.append(int(b))
                c = ddt2.count(o3)
                otp3.append(int(c))
            for data3 in anc:
                ddt3 = data3.get_text()
                a = ddt3.count(o1)
                otp1.append(int(a))
                b = ddt3.count(o2)
                otp2.append(int(b))
                c = ddt3.count(o3)
                otp3.append(int(c))
    s1 = sum(otp1)
    s2 = sum(otp2)
    s3 = sum(otp3)
    embed=discord.Embed(title="**__Google Result__**",description=f"[{s1}, {s2}, {s3}]",color=0x00fbff)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/787386630885081118/787495811830513664/hq31.jpg?width=1025&height=450")
    hook.send(embed=embed)
                    
def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
        print(response_data)
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%d/%m/%Y")
            x_inn = x_ind.strftime("%H:%M")
    
            prize = (response_data["nextShowPrize"])
            if prize == "$5,000":
                prizdata.insert(0,int(5000))
            elif prize == "$2,500":
                prizdata.insert(0,int(2500))
            elif prize == "$10,000":
                prizdata.insert(0,int(10000))
            time.sleep(5)
            print(x_in)
            print(prize)
#             embed = Embed(title="HQ Trivia", description="Next Hq Trivia Date **{}**".format(x_in))
#             embed.add_field(name="Next Hq Trivia Time", value="**{}**".format(x_inn),inline=False)
#             embed.add_field(name="Prize Money", value="**{}🎉**".format(prize),inline=False)
#             embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/662974806550904853/726402727214710814/hq2.jpg")
#             hook.send(embed=embed)



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            if message_data['type'] == 'interaction':
                pass
            elif message_data['type'] == 'broadcastEnded':
                pass
            else:
                print(message_data)
        
            if message_data['type'] == 'question':
                question = message_data['question']
                global qcnt
                qcnt = message_data['questionNumber']
                global Fullcnt
                Fullcnt = message_data['questionCount']
                id1 = message_data["answers"][0]["answerId"]
                id2 = message_data["answers"][1]["answerId"]
                id3 = message_data["answers"][2]["answerId"]
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                global o1
                o1 = answers[0]
                global o2
                o2 = answers[1]
                global o3
                o3 = answers[2]
                real_question = str(question).replace(" ","+")
                opt1 = str(answers[0]).replace(" ","+")
                opt2 = str(answers[1]).replace(" ","+")
                opt3 = str(answers[2]).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question
                q_op1 = "https://google.com/search?q="+real_question+opt1   
                q_op2 = "https://google.com/search?q="+real_question+opt2
                q_op3 = "https://google.com/search?q="+real_question+opt3
                embed = discord.Embed(title=f"Question {qcnt}/{Fullcnt}",description=f"[{question}]({google_query})",color=0x0800f0)
                embed.add_field(name="Option 1",value=f"[{answers[0]}]({q_op1})")
                embed.add_field(name="Option 2",value=F"[{answers[1]}]({q_op2})")
                embed.add_field(name="Option 3",value=f"[{answers[2]}]({q_op3})")
                embed.add_field(name="All Options",value=f"[Click Here]({google_query}+{opt1}+{opt2}+{opt3})")
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/787386630885081118/787495811830513664/hq31.jpg?width=1025&height=450")
                hook.send(embed=embed)
                hook.send("Hq")
                hook.send("+mt")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(google(question,o1,o2,o3))
            elif message_data["type"] == "answered":
				name = message_data["username"][0:3]
				answer = message_data["answerId"]
				if answer == id1:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{name} went option :one:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					#fetch.send("w1")
				if answer == id2:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{name} went option :two:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					#fetch.send("w2")
				if answer == id3:
					embed = discord.Embed(title=f"**Challenge Friends**",description=f"**{name} went option :three:**",color=000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835091231301304340/838295779461431326/IMG_20210330_002943.jpg")
					challenge.send(embed=embed)
					#fetch.send("w3")
            elif message_data["type"] == "questionClosed":
                embed=discord.Embed(title=":alarm_clock: Time,s UP",description="",color=0x0800f0)
                hook.send(embed=embed)
                time.sleep(5)
                otp1.clear()
                otp2.clear()
                otp3.clear()

            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                rlanswer = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']
                totalp = int(advancing)+int(eliminated)
                advp = round(int(advancing)/int(totalp)*100,2)
                elip = round(int(eliminated)/int(totalp)*100,2)
                cpr = round(int(prizdata[0])/int(advancing),2)
                nextcheck = message_data['nextCheckpointIn']
                ques = message_data['question']
                lol1 = message_data['answerCounts'][0]['answer']
                lol2 = message_data['answerCounts'][1]['answer']
                lol3 = message_data['answerCounts'][2]['answer']
                pol1 = message_data['answerCounts'][0]['count']
                pol2 = message_data['answerCounts'][1]['count']
                pol3 = message_data['answerCounts'][2]['count']
                qcnt = message_data['questionNumber']
                if str(correct) == str(o1):
                    rlanswer = f"Option :one:.{correct}"
                    trickdata.append(int(1))
                elif str(correct) == str(o2):
                    rlanswer = f"Option :two:.{correct}"
                    trickdata.append(int(2))
                else:
                    rlanswer = f"Option :three:.{correct}"
                    trickdata.append(int(3))

                embed = discord.Embed(title=f"Answer Stats({qcnt}/{Fullcnt})",description=f"**Correct Answer:-\n{rlanswer}\n• Advancing Players : {str(advancing)}({str(advp)}%)\n• Eliminated Players : {str(eliminated)}({str(elip)}%)\n• Current Payout : ${str(cpr)}**",color=0x0800f0)
                embed.add_field(name="Current Pattern",value=str(trickdata))
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/787386630885081118/787495811830513664/hq31.jpg?width=1025&height=450")
                hook.send(embed=embed)
            # elif message_data["type"] == "giftDrop":
            #     embed=discord.Embed(title="Tap On The ``Open It`` To Open The Chest",description="",color=0x0f03fc)
            #     hook.send(embed=embed)

            elif message_data["type"] == "gameSummary":
                winn = message_data['numWinners']
                priz = str(message_data["winners"][0]["prize"]) 
                print(winn)
                print(priz)
                embed = discord.Embed(title="Game Stats", description=f"• Winners : {winn}\n• Payout : {priz}\n• Prize Money : ${str(prizdata[0])}",color=0x0800f0)
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/787386630885081118/787495811830513664/hq31.jpg?width=1025&height=450")
                hook.send(embed=embed)

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

while True:
    if show_active():
        url = get_socket_url()
        token = get_auth_token()
        if token == 'NONE':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)

    else:
        show_not_on()
        time.sleep(30)
