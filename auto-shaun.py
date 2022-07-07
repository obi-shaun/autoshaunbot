from telethon import TelegramClient, events
import random
import boto3 
import json
import logging
import re
import requests

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_hash = '{secrets manager reference}'
bot_token = '{secrets manager reference}'
open_weather_api_key = '{secrets manager reference}'
api_id = 13563722
bot = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Salaam!')
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/talk'))
async def call_me_daddy(event):
    """Positive Vibes."""
    sender = await event.get_sender()
    first_name = sender.first_name
    talk_strings = [
        f'Hi, {first_name}. You\'re amazing!',
        f'What a great person you are, {first_name}!',
        'Yass, king?',
        f'How does it feel being so great, {first_name}?',
        f'You\'re such a wonderful friend, {first_name}!',
        f'You\'re my hero, {first_name}...',
        f'Your opinions matter, {first_name}!',
        'Change the world!',
        'Go get \'em, boss!',
        f'You got this, {first_name}...;D'
    ]
    await event.respond(random.choice(talk_strings))
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/weather'))
async def start(event):
    """Returns weather."""
    api_key = '{secrets manager reference}'

    parts = event.raw_text.split()
    arg = None

    if len(parts) > 1:
        arg = parts[1]
    else:
        return await event.respond(f'Send me a Zip Code using the command \"/weatherboy 22030\"')
 
    if re.match(r'.*(\d{5}(\-\d{4})?)$', arg):
        zcode = arg
        ccode = 'us'
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?zip={zcode},{ccode}&appid={api_key}&units=imperial')
        r = r.json()
        city = r['name']
        current_temp = r['main']['temp']
        min_temp = r['main']['temp_min']
        max_temp = r['main']['temp_max']
        description_short = r['weather'][0]['main']
        description_long = r['weather'][0]['description']
        await event.respond(f'Here\'s the weather for {city}. It\'s currently {current_temp} degrees, {description_long}. A high of {max_temp} and a low of {min_temp} are expected for today')
    else:
        return await event.respond(f'Send me Zip Code using the command \"/weatherboy 22030\"')

    raise events.StopPropagation

@bot.on(events.NewMessage)
async def detect_sentiment(event):
    """Detects the tone of your message"""
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    text = event.raw_text
    response = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
    print(type(response))
    response = json.loads(response)
    sentiment = response['Sentiment']
    sender = await event.get_sender()
    if sentiment == 'POSITIVE':
        await event.respond(f'Oooh yeah {sender.first_name}, feeling good?!')
    if sentiment == 'NEGATIVE':
        await event.respond(f'Hi, {sender.first_name}. I sense you\'re upset. Anything I can do to help?')

def main():
    """Start the bot."""
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
