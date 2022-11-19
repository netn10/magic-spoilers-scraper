from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv

import praw # For Reddit Scrapping
import time # For timing the Telegram messaging
import os
import requests
import sys

# Load from .env file
try:
    load_dotenv()
except Exception as e:
    print("Error loading environment variables: " + str(e))
    sys.exit(1)

# Init Telegram Vars
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')

# Init Reddit Vars
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

# Init current results of scraps
current_reddit_snapshot = []
current_mythic_spoiler_snapshot = []

def telegram_bot_sendtext(telegram_bot_token: str, telegram_group_id: str, bot_message: str):
    time.sleep(2)
    send_text = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_group_id}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    return response.json()

def scrape_reddit(is_first_scrap: bool, reddit_client_id: str, reddit_client_secret: str, reddit_user_agent: str):
    global current_reddit_snapshot
    reddit_read_only = praw.Reddit(client_id=reddit_client_id,         # your client id
                                client_secret=reddit_client_secret,      # your client secret
                                user_agent=reddit_user_agent)        # your user agent
    
    subreddit = reddit_read_only.subreddit("magicTCG")

    last_post = list(subreddit.new(limit=1))[0]
    last_post = "https://www.reddit.com/" + last_post.permalink
    if is_first_scrap == True:
        current_reddit_snapshot = last_post
        return last_post
    else:
        if last_post != current_reddit_snapshot:
            # That's a new leak!
            # Add to the list of cards
            current_reddit_snapshot = last_post
            # Send it to Telegram
            print(f"Sending... {current_reddit_snapshot}")
            #telegram_bot_sendtext(current_reddit_snapshot)
            return current_reddit_snapshot

def scrape_mythic_spoilers(is_first_scrap: bool):
    global current_mythic_spoiler_snapshot
    url = "https://mythicspoiler.com/newspoilers.html"
    # Uncomment to test
    #url = "http://127.0.0.1:8000/static_test"
  
    # initiating the webdriver. Parameter includes the path of the webdriver.
    response = requests.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    soup = BeautifulSoup(response.text, "html.parser")

    # All cards are tagged as img and have "cards" in their src attribute
    all_current_cards = soup.find_all('img', src=lambda h: h and "cards" in h)
    
    if is_first_scrap == True:
        current_mythic_spoiler_snapshot = all_current_cards
        return current_mythic_spoiler_snapshot
    else:
        for card in all_current_cards:
            if card not in current_mythic_spoiler_snapshot:
                # That's a new card!
                # Add to the list of cards
                current_mythic_spoiler_snapshot.append(card)
                img_src = card["src"].strip()
                img_src = f"https://mythicspoiler.com/{img_src}"
                # Send it to Telegram
                print(f"sending... {img_src}")
                #telegram_bot_sendtext(img_src)
                return current_mythic_spoiler_snapshot
