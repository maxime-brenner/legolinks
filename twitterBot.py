from dotenv import dotenv_values
import tweepy

config=dotenv_values(".env")

auth=tweepy.OAuthHandler(consumer_key=config["API_KEY"], consumer_secret=config["API_KEY_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

api=tweepy.API(auth)

my_id="1517070229104476161"
recipient_id="70748326"

with open("test_message.txt", 'r', encoding='UTF-8') as m:
    message=m.read()

#api.send_direct_message(recipient_id, text=message)
followers=api.get_follower_ids(user_id=recipient_id, count=1000)

i=0

for f in followers:
    try:
        api.send_direct_message(f, text=message)
        print("message sent to {0}!".format(f,))
        i+=1
    except tweepy.errors.Forbidden:
        print("cannot deliver message to {0}!".format(f,))
        pass

print("Message deliver to {0}/{1}".format(i, len(followers),))


