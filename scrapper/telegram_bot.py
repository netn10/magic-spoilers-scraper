from functions import *

#scrape_reddit(is_first_scrap=True, reddit_client_id=REDDIT_CLIENT_ID, reddit_client_secret = REDDIT_CLIENT_SECRET, reddit_user_agent = REDDIT_USER_AGENT)
scrape_mythic_spoilers(is_first_scrap=True)

while True:
    #scrape_reddit(is_first_scrap=False, reddit_client_id=REDDIT_CLIENT_ID, reddit_client_secret = REDDIT_CLIENT_SECRET, reddit_user_agent = REDDIT_USER_AGENT)
    scrape_mythic_spoilers(is_first_scrap=False)
