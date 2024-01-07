# This example requires the 'message_content' intent.

import discord
import constants
import os
import requests


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await  self.get_attachments_in_channel()

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def get_attachments_in_channel(self):
        if not os.path.exists(constants.folder_path):
            os.makedirs(constants.folder_path)

        channel = discord.utils.get(self.get_all_channels(), name=constants.discord_channel_name)
        # This was a synchronous way to access messages in a channel history below,
        # channel.history provides an async iterator
        # messages = [message async for message in channel.history(limit=constants.message_search_limit)]
        async for msg in channel.history(limit=constants.message_search_limit):
            print(msg.content)
            if msg.attachments:
                for attachment in msg.attachments:
                    if attachment.url and attachment.filename:
                        url = attachment.url
                        response = requests.get(url)
                        with open(constants.folder_path + "/" + attachment.filename, "wb") as f:
                            f.write(response.content)
        return


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(constants.discord_token)
