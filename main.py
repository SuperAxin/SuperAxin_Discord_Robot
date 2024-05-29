import requests
import json
import asyncio
import pandas as pd
from table2ascii import table2ascii as t2a, PresetStyle
from io import BytesIO

# 導入Discord.py模組
import discord

# 導入commands指令模組
from discord.ext import commands

from fredapi import Fred

api_key = '' #　自行輸入 Fredapi Key
fred = Fred(api_key=api_key)

# Plot
import matplotlib.pyplot as plt

# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

@bot.command()
# 輸入%Hello呼叫指令
async def FRED(ctx, database):
    data = fred.get_series(database).tail(10)
    # 作圖
    plt.plot(data)
    plt.grid()
    plt.title(database)
    plt.xlabel('Date')
    plt.ylabel('Value')
    # 將圖片保存到 BytesIO 對象中
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    # 將 BytesIO 對象轉換為 discord.File 對象並發送到 Discord
    file = discord.File(img, filename='img.png')
    await ctx.send(file=file)
    # 釋放資源
    plt.close()

    # 做表格
    series_data = pd.Series(data)
    df = pd.DataFrame({'Date': series_data.index, 'Value': series_data.values})
    print(df['Date'][0].date())

    change = data.pct_change() * 100 # 變動率計算
    change = change.round(2)

    output = t2a(
        header=['Date', 'Value', 'Change'],
        body=[
            [df['Date'][0].date(), df['Value'][0], change[0]],
            [df['Date'][1].date(), df['Value'][1], change[1]],
            [df['Date'][2].date(), df['Value'][2], change[2]],
            [df['Date'][3].date(), df['Value'][3], change[3]],
            [df['Date'][4].date(), df['Value'][4], change[4]],
            [df['Date'][5].date(), df['Value'][5], change[5]],
            [df['Date'][6].date(), df['Value'][6], change[6]],
            [df['Date'][7].date(), df['Value'][7], change[7]],
            [df['Date'][8].date(), df['Value'][8], change[8]],
            [df['Date'][9].date(), df['Value'][9], change[9]],
              ],
        first_col_heading=True
    )
    await ctx.send(f"```\n{output}\n```")


@bot.command()
async def SFRED(ctx, search):
    df = fred.search_by_category(int(search), limit=10, order_by='popularity', sort_order='desc')
    await ctx.send(df['title'])

@bot.command()
async def GPT(ctx, arg):
    api_key = '' #　自行輸入GPT Token

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json = {
    'model': 'gpt-3.5-turbo',  # 一定要用chat可以用的模型
    'messages':
        [
            {"role": "user", "content": arg},
        ]
})
    response = response.json()
    message = response['choices'][0]['message']['content']
    await ctx.send(message)

Token = '' #　自行輸入Token
asyncio.run(bot.run(Token))