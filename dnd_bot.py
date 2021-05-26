import discord
from discord.ext import commands,tasks
import os
from dotenv import dotenv_values
import random
import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md
import json
import pandas as pd

config = dotenv_values("bot.env")


def iterdict(dictionary): #recursively iter nested dicts
    string = ''
    try:
        for i in dictionary.values():
            if isinstance(i, dict):
                string += iterdict(i)
            elif isinstance(i, list) and len(i)!=0:
                if isinstance(i[0], str):
                    string += "**"+"".join(list(dictionary.keys())[list(dictionary.values()).index(i)]) + "**: "  +"".join([item + " " for item in i]) + "\n"
                else:
                    for item in i:
                        string += iterdict(item)
            else:
                if str(list(dictionary.keys())[list(dictionary.values()).index(i)]) not in ['index', 'url']:
                    string += "**"+"".join(list(dictionary.keys())[list(dictionary.values()).index(i)]) + '**: ' + str(i)+'\n'
        return string
    except:
        return "Something went wrong"


intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='#',intents=intents)

@bot.command(name='roll', aliases=['r', 'rol'], help='With this command you can roll dices. Just type `#roll 1d20`')
async def _roll(ctx, arg):
    m = arg.split('d')
    if int(m[1]) < 9999 and int(m[0]) < 9999:
        num = sum([random.randint(1, int(m[1])) for i in range(int(m[0]))])
        await ctx.send(num)
    else:
        await ctx.send("We can't throw number this big")
@bot.command(name='spell', aliases=['spel', 's', 'sepll'], help="With this command you can get information about any spell from DnD 5e. Just write `#spell Mage Hand`.")
async def _spell(ctx, *args):
    name = []
    for n in args:
        if args.index(n) == 0:
            name.append(n)
        else:
            name.append(' '+n)
    name = ''.join(name) # this scrapy code parses spell description from a webpage, please change it in next version
    name.strip()
    name.lower()
    name = name.replace(' ', '-')
    url = 'https://www.dnd-spells.com/spell/' + name
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features="html.parser")
    el = soup.find("div", {"class": "col-md-12"})
    el.find("div", {"class": "call-action"}).decompose()
    el.find("div", {"class": "margin-top"}).decompose()
    el.find("i", {"class": "fa"}).parent.decompose()
    el.find("a", {"href": "https://www.dnd-spells.com"}).decompose()
    el.find("h4").decompose()
    comments = el.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        c.extract()
    el = md(str(el)).split('\n')
    el = [l for l in el if l]
    el = [n + '\n' for n in el if n not in ['\r', '---']]
    new = []
    for n in el:
        if n.startswith(' Page:'):
            break
        else:
            new.append(n)
    content = ''.join(new)
    if len(content) > 2000:
        firstpart, secondpart = content[:int(len(content)/2)], content[int(len(content)/2):]
        await ctx.send(firstpart)
        await ctx.send(secondpart)
    await ctx.send(content)
@bot.command(name='equipment', aliases=['e', 'eq', 'eqipment'], help='With this command you can get description of any D&D equipment just type `#equipment shortsword`.')
async def _equipment(ctx, *args):
    name = []
    for n in args:
        if args.index(n) == 0:
            name.append(n)
        else:
            name.append(' '+n)
    name = ''.join(name)
    name.strip()
    name.lower()
    name = name.replace(' ', '-')
    url = 'http://www.dnd5eapi.co/api/equipment/' + name
    response = requests.get(url).json()
    await ctx.send(iterdict(response))

@bot.command(name='magicitem', aliases=['magic items', 'magic item', 'magic-items'], help='With this command you can get description of any D&D magic item  just type `#magicitem adamantite armor`')
async def _magicitem(ctx, *args):
    name = []
    for n in args:
        if args.index(n) == 0:
            name.append(n)
        else:
            name.append(' '+n)
    name = ''.join(name)
    name.strip()
    name.lower()
    name = name.replace(' ', '-')
    url = 'http://www.dnd5eapi.co/api/magic-items/' + name
    response = requests.get(url).json()
    content = iterdict(response)
    if len(content) > 2000:
        firstpart, secondpart = content[:int(len(content)/2)], content[int(len(content)/2):]
        await ctx.send(firstpart)
        await ctx.send(secondpart)
    else:
        await ctx.send(content)

@bot.command(name='monster', aliases=['monsters', 'm', 'monsers', 'monser'], help='With this you command can get information about any D&D monster you like. Just write `#monster Fire Elemental`')
async def _monster(ctx, *args):
    name = []
    for n in args:
        if args.index(n) == 0:
            name.append(n)
        else:
            name.append(' '+n)
    name = ''.join(name)
    name.strip()
    name.lower()
    name = name.replace(' ', '-')
    url = 'http://www.dnd5eapi.co/api/monsters/' + name
    response = requests.get(url).json()
    content = iterdict(response)
    if len(content) > 2000:
        firstpart, secondpart = content[:int(len(content)/2)], content[int(len(content)/2):]
        await ctx.send(firstpart)
        await ctx.send(secondpart)
    else:
        await ctx.send(content)

# @bot.command(name="condition", aliases=["con"])




bot.run(config['TOKEN'])

