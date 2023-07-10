from config import token, ownerId, testerIds, prefix, prefixActive, botName
import websocket
import threading
import requests
import json
import time
import os

os.system("cls")


def directChannelMessage(url, message):
    payload2 = {
        "content": message
    }

    header = {
        "authorization": token
    }

    r = requests.post(url=url, data=payload2, headers=header)


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


def heartbeat(interval, ws):
    print(f'{botName}: Dinleme Başladı')

    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }

        send_json_request(ws, heartbeatJSON)
        print("Sairus: Dinleme Gönderildi")


def command(prompt, message, ownerOnly=0, testerOnly=0, url=""):
    prompt = str(prompt)
    message = str(message)

    if not prompt and message:
        print(f"{botName}: Lütfen Komut ve Karşılığını Giriniz.")
    elif not prompt:
        print(f"{botName}: Lütfen Komut Giriniz.")
    elif not message:
        print(f"{botName}: Lütfen Karşılığını Giriniz.")
    elif ownerOnly == 1 and testerOnly == 0:
        if id == ownerId:
            if content == prompt:
                message = message.replace("$userid", f"<@{id}>")
                directChannelMessage(url=url, message=message)
    elif testerOnly == 1 and ownerOnly == 0:
        if id in testerIds:
            if content == prompt:
                message = message.replace("$userid", f"<@{id}>")
                directChannelMessage(url=url, message=message)
    elif ownerOnly and testerOnly == 1:
        if id in testerIds or ownerId == id:
            if content == prompt:
                message = message.replace("$userid", f"<@{id}>")
                directChannelMessage(url=url, message=message)
    elif ownerOnly == 0 and testerOnly == 0:
        if content == prompt:
            message = message.replace("$userid", f"<@{id}>")
            directChannelMessage(url=url, message=message)


ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "edge",
            "$device": "pc"
        }
    }
}

send_json_request(ws, payload)

while True:
    event = recieve_json_response(ws)

    try:
        global content
        global id
        global channelId
        global username

        id = int(event['d']['author']['id'])
        username = str(event['d']['author']['username'])
        channelId = event['d']['channel_id']
        content = str(event['d']['content'])
        url = f"https://discord.com/api/v9/channels/{channelId}/messages"

        if ownerId == id:
            if content == "prefix":
                if prefixActive == 0:
                    prefixActive = 1
                elif prefixActive == 1:
                    prefixActive = 0

        # Kod Yazma Alanı

        # command("test1", "bu komut herkese açıktır!", url=url)
        # command("test2", "bu komut sahibe açıktır!", ownerOnly=1, url=url)
        # command("test3", "bu komut testerlara açıktır!", testerOnly=1, url=url)
        # command("test4", "bu komut sahibe ve testera açıktır!", ownerOnly=1, testerOnly=1, url=url)
        
        if prefixActive == 0:
            command("selam", f"{botName}: Merhaba, $userid nasılsın?", url=url)
        elif prefixActive == 1:
            command(prefix + " selam", f"{botName}: Merhaba, $userid nasılsın?", url=url)
    except:
        pass
