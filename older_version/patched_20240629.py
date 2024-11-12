import discord
from discord.ext import commands
import json
import asyncio
import random
from wxauto import WeChat
from typing import Optional
from discord import Intents
from discord import app_commands

# Load settings from the JSON file
with open('settings.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

channel_id = int(jdata["channel_id"])
bot_token = jdata["TOKEN"]

# Initialize intents for the Discord bot
intents = Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, proxy="http://127.0.0.1:10809")
EMBED_COLOR = discord.Color.blue()

# Initialize the WeChat client
wx = WeChat()

# Function to read the last messages from the JSON file
def read_last_messages():
    try:
        with open('last_messages.json', 'r', encoding='utf8') as f:
            data = json.load(f)
            return data.get('last_messages', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save the last messages to the JSON file
def save_last_messages(last_messages):
    with open('last_messages.json', 'w', encoding='utf8') as f:
        json.dump({'last_messages': last_messages}, f)

# Function to print all WeChat messages
async def print_all_messages():
    msgs = wx.GetAllMessage()
    channel = bot.get_channel(channel_id)
    color = EMBED_COLOR
    if channel:
        for msg in msgs:
            sender = msg[0]
            message = msg[1]
            if sender == "Self":
                color = discord.Color.green()
                sender = sender.replace("Self", "Me")
            if sender == "SYS" and ("下午" in message or "上午" in message):
                sender = "Time"
            else:
                sender = sender.replace("SYS", "System")

            embed = discord.Embed(title=f'{sender}', description=f'{message}', color=color)
            await channel.send(embed=embed)
            color = EMBED_COLOR
    return [{'sender': msg[0], 'message': msg[1]} for msg in msgs[-3:]] if msgs else []

# Function to check for new WeChat messages
async def check_new_messages(last_msgs):
    while True:
        msgs = wx.GetAllMessage()
        channel = bot.get_channel(channel_id)
        color = EMBED_COLOR
        if msgs:
            latest_msgs = [{'sender': msg[0], 'message': msg[1]} for msg in msgs[-3:]]
            new_msgs = [msg for msg in latest_msgs if msg['message'] not in [last_msg['message'] for last_msg in last_msgs]]
            last_msgs = latest_msgs  # Update last_msgs to the latest three messages
            save_last_messages(last_msgs)  # Save the latest messages to the JSON file
            for latest_msg in new_msgs:
                sender = latest_msg['sender']
                message = latest_msg['message']
                if sender == "Self":
                    color = discord.Color.green()
                    sender = sender.replace("Self", "Me")
                if sender == "SYS" and ("下午" in message or "上午" in message):
                    sender = "Time"
                else:
                    sender = sender.replace("SYS", "System")

                embed = discord.Embed(title=f'{sender}', description=f'{message}', color=color)
                await channel.send(embed=embed)

        await asyncio.sleep(0.05)  # Add a sleep to prevent a tight loop

# Event: on_message
@bot.event
async def on_message(msg):
    designated_person_id = 857808844439945276
    designated_person_name = "little_blue0527"

    # 碰氣專用(10%)
    if msg.author.id == designated_person_id or msg.author.name == designated_person_name:
        tmp_num = random.randint(1, 5)
        if tmp_num == 5:
            await msg.reply("出門右轉")

    # 除了碰氣以外的其他人(0.02%)
    if msg.author.id != designated_person_id:
        tmp_num = random.randint(1, 10000)
        if tmp_num == 1 or tmp_num == 2:
            await msg.reply("出門右轉")

    # 點點點
    if msg.content.endswith("點點點") and msg.author != bot.user:
        await msg.reply("出門右轉")

    # Process commands
    await bot.process_commands(msg)

# Event: Bot is online
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(">>Bot is online<<")
    last_messages = read_last_messages()  # Read the last messages from the JSON file
    last_messages = last_messages if last_messages else await print_all_messages()
    bot.loop.create_task(check_new_messages(last_messages))

# Command: 覆述
@bot.tree.command(name="say", description="替你說話")
async def say(interaction: discord.Interaction, text: Optional[str] = None):
    if text is None:
        text = "點點點"
    await interaction.response.send_message(text, ephemeral=False)

# Command: Hello
@bot.tree.command(name="hello", description="Hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello")

# Command: 拍一拍
@bot.tree.command(name="pat", description="拍一拍指定的使用者")
@app_commands.describe(user="选择一个用户")
async def pat(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"{interaction.user.display_name} 拍了拍 {user.mention}")


# Command: Shutdown the bot
@bot.tree.command(name='shutdown', description="關機")
async def shutdown(interaction: discord.Interaction):
    role_id = 1093829644219842612  # 替换为你的角色 ID
    if any(role.id == role_id for role in interaction.user.roles):
        await interaction.response.send_message(">>Bot is now offline<<")
        await bot.close()
    else:
        await interaction.response.send_message("出門右轉", ephemeral=True)


# Main execution
if __name__ == "__main__":
    bot.run(bot_token)
