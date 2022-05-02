import os
import datetime
import tweepy

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token)

user_name = input("Enter Twitter user: ")

response = client.get_user(username=user_name)
# print(type(response))
# print(response)
# print(dir(response))
# print(response.data.id)
user_id = response.data.id

end_time = datetime.datetime.now()
time_delta = datetime.timedelta(days=1)
start_time = end_time - time_delta

tweets_response = client.get_users_tweets(
    id = user_id,
    start_time = start_time,
    end_time = end_time,
    #media_fields = [{"type":"video"}],
    expansions="attachments.media_keys",
    media_fields=["media_key", "type", "url", "height", "duration_ms", "preview_image_url"],
    max_results = 15,
)
tweets = tweets_response.data
tweet_includes = tweets_response.includes
media_objects = tweet_includes.get("media", [])
# print(type(tweets))
# print(dir(tweets))
# print(tweets)
# print(type(tweets.data))
# print(tweets.data)
print(tweet_includes)
print()
for tweet in tweets:
    #print(type(tweet))
    #print(dir(tweet))
    #print(tweet)
    print(tweet.id)
    print(tweet.text)
    #print(tweet.data)
    media_keys = tweet.data.get("attachments", {}).get("media_keys", [])
    print(media_keys)
    for media_key in media_keys:
        for media in media_objects:
            # print(type(media))
            #print(dir(media))
            if media.media_key == media_key:
                #print(media.type)
                #print(media.data)
                if media.preview_image_url is not None:
                    print(media.preview_image_url)
    #print(tweet.includes)
    #print(tweet.meta)
    #print(tweet._fields)
    print()
