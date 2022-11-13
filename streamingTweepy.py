from dotenv import dotenv_values
import tweepy
import sys
from time import sleep

config=dotenv_values(".env")

auth=tweepy.OAuthHandler(consumer_key=config["API_KEY"], consumer_secret=config["API_KEY_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

api=tweepy.API(auth, wait_on_rate_limit=True)

client=tweepy.Client(config['BEARER_TOKEN'], config["API_KEY"], config["API_KEY_SECRET"], config['ACCESS_TOKEN'], config['ACCESS_TOKEN_SECRET'])
search_terms=["tesla", "spaceX"]

class Listener(tweepy.StreamingClient):

    def on_connect(self):
        print("Connected")

    def on_tweet(self, tweet):
        if tweet.referenced_tweets==None :
            try:
                 tweet.entities['mentions'][0]['username']='elonmusk'
                 print(tweet.text)
                 sleep(0.2)
            except KeyError:
                pass


            

    def on_error(self, status_code):
        print(status_code)
        return False



stream=Listener(bearer_token=config["BEARER_TOKEN"])


for term in search_terms:
    print(stream.get_rules())
    stream.add_rules(tweepy.StreamRule(term))

#stream.filter(tweet_fields=["referenced_tweets",], expansions='entities.mentions.username')