import tweepy
import pandas as pd
import datetime


# api_key = 'ndwYEnl0nMmyduUyIs5qJ034I'
# api_key_secret = 'GOh9zfXx1LTIGcdcydlzhft3YYlaCdvd8v54x3eHyGQO4OxxOP'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHJRVwEAAAAA9nuaI3nsag4vYnyLHxdVUrTUp00%3DVJFgN1W63jcBmSZauFAzaQDxjnztDAcQVWYcHPHmqDhA6a1nDH'
#
# consumer_key = api_key
# consumer_secret = api_key_secret
#
# access_token = '1460078982053965831-RKrtnV0M6FAZvHqNqIDeMI4Ub7qmp7'
# access_token_secret = 'I8CCASI82wOQtzzWSyc4P3U5JAW6J5QFTNTS5PcOtZ5uy'
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
# api = tweepy.API(auth, wait_on_rate_limit=True)

# Authentication set up
api_key = 'Yl0zZGJtPQp9mUksPG1ggQtV2'
api_key_secret = 'A2bPtU2sJ27QMlTOyFkuAwvuw0Hgtj9gN3KJu3UhmLzsB6HF2V'
broken_token = 'AAAAAAAAAAAAAAAAAAAAAEtNWwEAAAAAx3fe3oXWrqHZPbIiwfjf185ppSY%3D9yLBziKfCGU4H1nykhgzhiV3zxTnQHZIu1zW5P5htZFUavzkNZ'

access_token = '1469352604840960002-ip2YVBL0qHPnk92hqKKoHZmihIRVGP'
access_token_secret = 'XwSC0pWVo01LAaB8ge5px1gn01q8eMOPdAQFrSQvR1Yhp'

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


# consumer_KEY = 'SPAGrhKfG5286S8pEzIDCWFeO'
# consumer_SECRET = 'AMQG0210wdgYzbVFNV8lRPOzf6NV7XAllHhIDa4iAlou1nkaJR'
# access_TOKEN = '1463141094657445889-47PCVsTSvDbiYUdproVEuYQA3mwqoz'
# access_TOKEN_SECRET = 'DZ0gPbCwt0WvGd17ZHshbzA1tFtpSfgabwYkrqBM9836S'
#
#
# auth = tweepy.OAuthHandler(consumer_KEY, consumer_SECRET)
# auth.set_access_token(access_TOKEN, access_TOKEN_SECRET)
# api = tweepy.API(auth, wait_on_rate_limit=True)

startDate = datetime.datetime(2021, 12, 10, 0, 0, 0)
endDate =   datetime.datetime(2012, 12, 11, 0, 0, 0)

cursor = tweepy.Cursor(api.search_tweets, q="(covid) OR (canada covid) OR (Covid-19)", lang="en", tweet_mode='extended', since='2021-12-10', until='2021-12-11').items(1600)

i = 0
tweet = []

for this_tweet in cursor:
    i += 1
    print(i)
    try:
        status = api.get_status(this_tweet.id, tweet_mode="extended")
        tweet.append(status.retweeted_status.full_text)
    except AttributeError:
        tweet.append(this_tweet.full_text)



print("Number of tweets collected: ", i)

df = pd.DataFrame(tweet, columns = ["text"])
df.to_csv("covid_with_date.csv")



