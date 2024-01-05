from typing import Final
import os
import re
import discord
import aiohttp

TOKEN: Final[str] = os.environ['DISCORD_API_KEY']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def is_webhook_url(url: str) -> bool:
    pattern = r'^https://discord\.com/api/webhooks/\d+/\S+$'
    return re.match(pattern, url) is not None

async def send_message_with_webhook(url: str, message: str) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(url, session=session)
        await webhook.send(message)


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
        await message.channel.send('Webhook用URLを入力してください。')
        
        def check_id(message) -> bool:
            return message.author.id == saved_user_id
        
        webhook_url = await client.wait_for('message', check=check_id)
        
        if is_webhook_url(webhook_url.content):
            await message.channel.send('Webhook用URLが登録されました。')
            await message.channel.send('送信するメッセージを入力してください。')
            send_message = await client.wait_for('message', check=check_id)
            await message.channel.send('送信回数を半角数字で入力してください。')
            send_time = await client.wait_for('message', check=check_id)
            if send_time.content.isdigit():
                for i in range(int(send_time.content)):
                    await send_message_with_webhook(webhook_url.content, send_message.content)
        else:
            await message.channel.send('URLが不正です。')
            return

client.run(TOKEN)
