import asyncio
import discord
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib import parse
import os

client = commands.Bot(command_prefix = '-')
pageurl = "https://lostark.game.onstove.com/Profile/Character/"

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.Game(name="커피 한잔"))
    
    print("Logged in as ") #봇의 아이디, 닉네임이 출력
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):

    if message.author.bot:
        return None    
    
    if message.content.startswith('!검색'):
        await id_search(message)

@client.event
async def id_search(message):
    id = message.author.id
    channel = message.channel   
    url = pageurl+parse.quote(message.content[4:]) 
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")


    inumber = 0
    ijobnumber = 0
    img_alt = []
    for chname in bsObject.find_all("div", {"class":"content content--profile"})[0].find_all("ul", {"class":"profile-character-list__char"}):        
        for name in chname.find_all("span"):            
            
            for img_tag in name.find_all('img'):
                img_alt.append(str(img_tag.get('alt')))               

            if inumber % 2 != 0:               
                thisurl = pageurl + parse.quote(re.sub( "\<span>|\</span>","", str(name)))                              
                thishtml = urlopen(thisurl)
                thisbsObject = BeautifulSoup(thishtml, "html.parser")
                
                lvstr = thisbsObject.find_all("div", {"class":"level-info2__item"})[0].find_all("span")[1]
                
                await channel.send( re.sub( "\<span>|\</span>|\<small>|\</small>","", str(name) + "/" + img_alt[ijobnumber] + "/" +str(lvstr)))
                ijobnumber+=1            

            inumber+=1

    return

client.run(os.environ['token'])