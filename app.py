from typing import Final
import os
import re
import discord

TOKEN: Final[str] = os.environ['DISCORD_API_KEY']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def is_webhook_url(url: str) -> bool:
            pattern = r'^https://discord\.com/api/webhooks/\d+/\S+$'
            return re.match(pattern, url) is not None


@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message) -> None:
    saved_user_id = None
    
    if message.author == client.user:
        return
    
    if message.content == '!webhook':
        saved_user_id = message.author.id
        await message.channel.send('Webhook用URLを入力してください')
        
        def check_id(message) -> bool:
            return message.author.id == saved_user_id
        
        webhook_url = await client.wait_for('message', check=check_id)
        
        if is_webhook_url(webhook_url.content):
            await message.channel.send('Webhookを設定しました')
        
        else:
            await message.channel.send('URLが不正です')
            return

client.run(TOKEN)