import discord
from discord.ext import commands
import requests
import numpy as np
from news import everything_news
import datetime
from cricket_score import score
from pycoingecko import CoinGeckoAPI
from wiki import wiki_info
from toss import coinFlip, method
from weather import weather_res
from score_scrapper import fbscore
from nickname import nickn
from barney import Barney
from chandler import Chandler
from animequote import Animequote
from gif import Gif
import discord,asyncio,youtube_dl
import os
import json
from dotenv import load_dotenv
from creepy import story
from dictionary import Dictionary
from movies import mov
from crypto_logo_img import logo
from animerec import synopsis

cg = CoinGeckoAPI()



client  = commands.Bot(command_prefix = 'kb$')
client.remove_command('help')

@client.event
async def on_ready():
    print("Bot is ready")


from dotenv import load_dotenv

load_dotenv()

exts=['music'] 


@client.event
async def on_ready():
    song_name='with All For One' 
    activity_type=discord.ActivityType.playing
    await client.change_presence(activity=discord.Activity(type=activity_type,name=song_name))
    print(client.user.name)

for i in exts:
    client.load_extension(i)

    
newUserMessage = ['Omae wa mo shindeiru','to the big leagues kid!', 'Starting today you are a HERO!', 'SASAGEYO!!!','May the Force be with you','The World is here where were you?','Give up on your Dreams and Die!','There you are you little shit!','The King in the North','How ya doin?','With great penis comes great responsibilities!','Hope you quarantined yourself for 2 weeks before coming here...','eat my hair and gain my power!','you might be the one for me','starting today you are a Rental Girlfirend!','To Indu IT School']

@client.event
async def on_member_join(member: discord.Member):
    p = numpy.random.randint(16,size=1)
    q = p[0]
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send('Welcome '+str(member.mention)+' '+str(newUserMessage[q]))

@client.event
async def on_command_error(ctx,error):
        await ctx.send("No such command x_x")


@client.event
async def on_member_join(member: discord.Member):
    def get_name():
        n_name = nickn()
        name_list = []
        name_list.append(n_name)
        return name_list
    x = get_name()
    a_set = set(x)
    contains_duplicates = len(x) != len(x)
    if (contains_duplicates == True):
        x.pop((-1))
        x = get_name()

    await member.edit(nick=x[-1])
    

@client.command()
async def words(ctx):
    embed = discord.Embed(title = 'WORDS OF WISDOM', color = discord.Colour.magenta())
    p = np.random.randint(3,size=1)
    q = p[0]

    if q==0:
        name = " - Barney Stinson"
        z = str(Barney()+name)
    elif q==1:
        name = " - chandler Bing"
        z = str(Chandler()+name)
    elif q==2:
        z = Animequote()

    embed.add_field(name = "Quote", value = z , inline=True)
    await ctx.send(embed = embed)

@client.command()
async def news(ctx,arg):
    embed = discord.Embed(title = "HEADLINES" , color = discord.Colour.green())
    arg = str(arg)
    x = everything_news(arg)
    upper_case = arg.upper()
    embed.add_field(name = upper_case, value = x, inline = True )
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)

    
@client.command()
async def cprice(ctx, *, crypto):
    crypto = crypto.upper()
    embed = discord.Embed(title = crypto , color = discord.Colour.dark_blue())
    crypto = crypto.lower()
    l = logo(crypto)
    x = cg.get_price(ids= crypto, vs_currencies='usd,eur,inr', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
    usd = str(x[crypto]['usd'])+' USD'
    eur = str(x[crypto]['eur'])+' EUR'
    inr = str(x[crypto]['inr'])+' INR'

    usd_market_cap = str(x[crypto]['usd_market_cap'])+' USD'
    usd_24h_vol = str(x[crypto]['usd_24h_vol'])+' USD'
    usd_24h_change = str(x[crypto]['usd_24h_change'])+' USD'
    z = ctx.author.name
    # g = crypto_g(crypto,z)

    embed.set_thumbnail(url = l)
    embed.add_field(name = "USD", value = usd, inline = False )
    embed.add_field(name = "EUR", value= eur, inline = False)
    embed.add_field(name = "INR", value= inr, inline = False)
    embed.add_field(name = "MARKET CAP", value= usd_market_cap, inline = False)
    embed.add_field(name = "24H VOL", value= usd_24h_vol, inline = False)
    embed.add_field(name = "24H CHANGE", value= usd_24h_change, inline = False)
  
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

    
@client.command()
async def wiki(ctx,*, subject):
    subject = subject.upper()
    em = discord.Embed(title = subject , color = discord.Colour.red())
    subject = subject.lower()
    await ctx.send(embed = em)

    y = wiki_info(subject)

    str_count = 0
    end_count=1999
    for i in range(int((len(y)/1999)+1)):
        if end_count > len(y):
            await ctx.send(y[str_count :])
            break
        await ctx.send(y[str_count : end_count]+'-')
        if end_count == len(y):
            break
        str_count +=1999
        end_count += 1999

    embed = discord.Embed(title = " " , color = discord.Colour.red())
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")

    await ctx.send(embed = embed)
    
    
@client.command()
async def toss(ctx, member: discord.Member):
    d = {}
    probability = .5
    side = np.random.binomial(1,probability)
    if (side == 1):
        x = 0
    else:
        x = 1

    d.update({ctx.author.name:1,member.name:0})
    t =coinFlip()
    w = method(d,t)
    res = f"{w} is the winner"
    embed = discord.Embed(title = "TOSS" , color = discord.Colour.dark_orange())
    embed.add_field(name = 'RESULT' , value = res , inline = False)
    await ctx.send(embed=embed)


@client.command()
async def weather(ctx,city, *, country):

    city = str(city)
    country = str(country)
    json_data_2 = weather_res(city, country)

    icon = json_data_2['weather'][0]['icon']
    icon_link = "http://openweathermap.org/img/wn/" + icon + "@2x.png"

    weather_type = str(json_data_2['weather'][0]['main'])
    temperature = str(json_data_2['main']['temp']) + ' °C'
    feel_like = str(json_data_2['main']['feels_like']) + ' °C'
    min_temp = str(json_data_2['main']['temp_min']) + ' °C'
    max_temp = str(json_data_2['main']['temp_max']) + ' °C'
    humidity = str(json_data_2['main']['humidity']) + ' %'
    city = city.upper() + "'S"
    embed = discord.Embed(title = city + " WEATHER", color = discord.Colour.dark_green())
    embed.set_thumbnail(url = icon_link)
    embed.add_field(name = "CATEGORY", value = weather_type, inline = False )
    embed.add_field(name = "TEMP", value = temperature, inline = True)
    embed.add_field(name = "FEELS LIKE", value = feel_like, inline = True )
    embed.add_field(name = "MIN_TEMP", value = min_temp, inline = False)
    embed.add_field(name = "MAX_TEMP", value = max_temp, inline = True)
    embed.add_field(name = "HUMIDITY", value = humidity, inline = True)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)

@client.command()
async def g(ctx, x, r = None):
    
    x = x.upper()
    embed = discord.Embed(title = x, color = discord.Colour.teal())
    x= x.lower()

    y = ctx.author.mention
    c = Gif(y, x)
    # file = discord.File(y+'.gif')
    # b = 'attachment://'+y+'.gif'
    # embed.set_image(url = b)
    if r == None:
        embed.add_field(name = "\u200b", value = y+" "+x, inline=True)
    else:
        embed.add_field(name = "\u200b", value = y+" "+x+" "+r, inline = True)
        

    embed.set_image(url = c)
    await ctx.send(embed = embed)




@client.command()
async def fblive(ctx):
    embed = discord.Embed(title = 'INFO', color = discord.Colour.from_rgb(0, 255, 255))

    result = football_live()
    x = len(result)
    for i in result:
        embed.add_field(name = "Match", value = i, inline = False)

    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)
 

@client.command()
async def creepy(ctx):
    s = story()
    story_title = str(s[0])
    story_content = str(s[1])
    embed = discord.Embed(title  = story_title, color = discord.Colour.dark_red())
    await ctx.send(embed = embed)
    
    str_count = 0
    end_count=1999
    for i in range(int((len(story_content)/1999)+1)):
        if end_count > len(story_content):
            await ctx.send(story_content[str_count :])
            break
        await ctx.send(story_content[str_count : end_count]+'-')
        if end_count == len(story_content):
            break
        str_count +=1999
        end_count += 1999


@client.command()
async def meaning(ctx, word):
    try:
        word = word.upper()
        embed = discord.Embed(title = word, color = discord.Colour.gold())
        word = word.lower()

        val = Dictionary(word)
        definition = val['list'][0]['definition']
        example = val['list'][0]['example']
        embed.add_field(name = "Meaning", value = definition, inline= False)
        embed.add_field(name = "Example", value = example, inline = True)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")

        await ctx.send(embed = embed)
    except:
        embed = discord.Embed(title = "Error 404", color = discord.Colour.gold())
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")        

        await ctx.send(embed=embed)

@client.command()
async def roll(ctx):
    p = np.random.randint(low = 1, high = 6,size=1)
    embed = discord.Embed(title = " ", color = discord.Colour.gold())
    embed.add_field(name = "Dice",
                    value = f"The number is **{p}**")
    
    await ctx.send(embed = embed)


@client.command()
async def movie(ctx, *, name):
    z = mov(name)
    release_date = z[0]
    image = z[1]
    summary = z[2]
    rating = z[3] + '/10'
    cast = str(z[4]) + ', ' + str(z[5]) + ', ' + str(z[6]) + ', ' + str(z[7])
    name = name.upper()
    embed = discord.Embed(title = name, color = discord.Color.from_rgb(254, 226, 216))
    embed.set_image(url = image)
    embed.add_field(name = "Summary", value = summary, inline=False)
    embed.add_field(name = "IMDb", value = rating, inline=False)
    embed.add_field(name = "Release Date", value = release_date, inline=False)
    embed.add_field(name = 'Cast', value = cast, inline = False)
    
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)
    
   
@client.command(name="remhr",help="Insert the text you want to be reminded of and the time in minutes")
async def remhhr(ctx,time=None,*, amount: str):
    if time==None:
        await ctx.send("Please insert all the arguements.e.g kb$rem time(in hours) text")
    else:
        await asyncio.sleep(int(time)*60*60)
        embed = discord.Embed(title = 'Reminder!', color = discord.Colour.magenta())
        embed.add_field(name = f"Requested by {ctx.author.name}", value = amount , inline=True)
        await ctx.send(embed = embed)
        asyncio.get_event_loop()

@client.command(name="remmin",help="Insert the text you want to be reminded of and the time in minutes")
async def remmin(ctx,time=None,*, amount: str):
    if time==None:
        await ctx.send("Please insert all the arguements.e.g kb$rem time(in minutes) text")
    else:
        await asyncio.sleep(int(time)*60)
        embed = discord.Embed(title = 'Reminder!', color = discord.Colour.magenta())
        embed.add_field(name = f"Requested by {ctx.author.name}", value = amount , inline=True)
        await ctx.send(embed = embed)
        asyncio.get_event_loop()

@client.command(name="animerecommend")
async def anime(ctx):
    fin = synopsis()
    
    embed = discord.Embed(title = "Anime of the Day!", color = discord.Color.from_rgb(254, 226, 216))
    embed.set_image(url = fin[0])
    embed.add_field(name = "Anime", value = fin[1], inline=False)
 
    await ctx.send(embed = embed)
    await ctx.send(fin[2]) 
    em = discord.Embed(title = " ", color = discord.Color.from_rgb(254, 226, 216))
    em.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = em)        


@client.command()
async def criclive(ctx):
    z = cricket_live()
    embed = discord.Embed(title = " ", color = discord.Colour.green())
    embed.add_field(name = "Overview", value=z)

    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)
    
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colur = discord.Colour.orange())
    embed.set_author(name='Available Commands')
    embed.add_field(name='Music',value='• pub/join\n• pub/play\n• pub/queue\n• pub/song-info\n• pub/stop\n• pub/pause\n• pub/resume\n• pub/prev\n• pub/repeat\n• pub/channel\n• pub/move-bot',inline=True)
    
    embed.add_field(name='Endpoints',value='• pub/news\n• pub/weather\n• pub/roll\n• pub/toss\n• pub/remmin\n• pub/remhr\n• pub/cprice\n• pub/g (member is optional)\n• pub/meaning\n• pub/words\n• pub/movie <movie name>\n• pub/delete\n• pub/wiki\n• pub/fb <team 1> <team 2>\n• pub/cric <team 1> <team 2> (optional)\n• pub/creepy\n• pub/animetoday\n\n\n',inline=True)
    embed.set_footer(text='Check out our readme for further queries \nhttps://github.com/AkshatJoshi2000/P.U.B---Plus-Ultra-Bot', icon_url = ctx.author.avatar_url)
    
    await ctx.send(embed=embed)
    
    
@client.command()
async def delete(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

 
client.run('BOTTOKEN')
