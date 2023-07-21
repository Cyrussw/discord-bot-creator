import websocket
import threading
import requests
import sqlite3
import json
import time
import os
from config import botToken, botName, botPrefix, botPrefixActive, ownerId, testerIds


class DiscordBot:
    def __init__(self):
        self.botToken = botToken
        self.botName = botName
        self.botPrefix = botPrefix
        self.botPrefixActive = botPrefixActive
        self.ownerId = ownerId
        self.testerIds = testerIds

    def getBotSettings(self):
        connection = sqlite3.connect('bot.sql')
        cursor = connection.cursor()

        # Execute query to retrieve bot settings
        cursor.execute(
            'SELECT botToken, botName, botPrefix, botPrefixActive, ownerId FROM bot_settings')
        result = cursor.fetchone()  # Get the first row

        connection.close()

        return result

    def directChannelMessage(self, url, message):
        payload2 = {
            "content": message
        }

        header = {
            "authorization": self.botToken
        }

        r = requests.post(url=url, data=payload2, headers=header)

    def command(self, prompt, message, ownerOnly=0, testerOnly=0, url=""):
        prompt = str(prompt)
        message = str(message)

        if not prompt and message:
            print(f"{self.botName}: Please enter the command and its response.")
        elif not prompt:
            print(f"{self.botName}: Please enter the command.")
        elif not message:
            print(f"{self.botName}: Please enter the response.")
        elif ownerOnly == 1 and testerOnly == 0:
            if id == self.ownerId:
                if content == prompt:
                    message = message.replace("$userid", f"<@{id}>")
                    self.directChannelMessage(url=url, message=f"{self.botName}: {message}")
        elif testerOnly == 1 and ownerOnly == 0:
            if id in testerIds:
                if content == prompt:
                    message = message.replace("$userid", f"<@{id}>")
                    self.directChannelMessage(url=url, message=f"{self.botName}: {message}")
        elif ownerOnly and testerOnly == 1:
            if id in testerIds or self.ownerId == id:
                if content == prompt:
                    message = message.replace("$userid", f"<@{id}>")
                    self.directChannelMessage(url=url, message=f"{self.botName}: {message}")
        elif ownerOnly == 0 and testerOnly == 0:
            if content == prompt:
                message = message.replace("$userid", f"<@{id}>")
                self.directChannelMessage(url=url, message=f"{self.botName}: {message}")

    def startTerminal(self):
        # Create database connection
        print(f"{self.botName}: System is starting!")
        time.sleep(1)
        os.system("cls")

    # Sends a JSON-based request over WebSocket
    def sendJsonRequest(self, ws, request):
        ws.send(json.dumps(request))

    # Receives a JSON-based response over WebSocket
    def receiveJsonResponse(self, ws):
        response = ws.recv()
        if response:
            return json.loads(response)

    # Keeps the WebSocket connection alive by sending a "heartbeat" request at a specified interval
    def heartbeat(self, interval, ws):
        print(f'{self.botName}: Heartbeat started')

        while True:
            time.sleep(interval)

            # Create a "heartbeat" request as JSON
            heartbeatJson = {
                "op": 1,
                "d": "null"
            }

            # Send the "heartbeat" request
            self.sendJsonRequest(ws, heartbeatJson)
            print(f'{self.botName}: Heartbeat sent')

    def start(self):
        self.startTerminal()
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
        event = self.receiveJsonResponse(ws)

        heartbeat_interval = event['d']['heartbeat_interval'] / 1000
        threading._start_new_thread(self.heartbeat, (heartbeat_interval, ws))

        payload = {
            "op": 2,
            "d": {
                "token": self.botToken,
                "properties": {
                    "$os": "windows",
                    "$browser": "edge",
                    "$device": "pc"
                }
            }
        }

        self.sendJsonRequest(ws, payload)

        while True:
            event = self.receiveJsonResponse(ws)

            try:
                global content
                global id
                global url
                global channelId
                global username

                id = int(event['d']['author']['id'])
                username = str(event['d']['author']['username'])
                channelId = event['d']['channel_id']
                content = str(event['d']['content'])
                url = f"https://discord.com/api/v9/channels/{channelId}/messages"

                if self.ownerId == id:
                    if content == "prefix":
                        if self.botPrefixActive == 0:
                            self.botPrefixActive = 1
                        elif self.botPrefixActive == 1:
                            self.botPrefixActive = 0

                if self.botPrefixActive == 1:
                    self.command(self.botPrefix + " merhaba",
                                 "merhaba", url=url)
                else:
                    self.command("merhaba", "merhaba", url=url)
            except:
                pass


bot = DiscordBot()
bot.botToken, bot.botName, bot.botPrefix, bot.botPrefixActive, bot.ownerId = bot.getBotSettings()
bot.start()
