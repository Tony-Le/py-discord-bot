# This example requires the 'message_content' intent.
from datetime import datetime

import discord
import constants
import os
import requests
import helpers
import validators
import pyrfc6266
from urlextract import URLExtract
import os
from urllib.parse import urlparse


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
            extractor = URLExtract()
            urls = extractor.find_urls(msg.content)
            if msg.attachments:
                for attachment in msg.attachments:
                    if attachment.url and attachment.filename:
                        url = attachment.url
                        response = requests.get(url)
                        if response.status_code == 200:
                            with open(constants.folder_path + "/" + attachment.filename, "wb") as f:
                                f.write(response.content)
            for url in urls:
                if validators.url(url):
                    if helpers.is_url_image(url):
                        response = requests.get(url)
                        if response.status_code == 200:
                            filename = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                            if response.headers and 'content-disposition' in response.headers:
                                filename = pyrfc6266.parse_filename(response.headers['content-disposition'])
                            elif len(os.path.basename(urlparse(url).path)) > 0:
                                filename = os.path.basename(urlparse(url).path)
                                filename = helpers.add_image_file_extension_if_none(filename, response.headers['content-type'])
                            with open(constants.folder_path + "/" + filename, "wb") as f:
                                f.write(response.content)

        return


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(constants.discord_token)
