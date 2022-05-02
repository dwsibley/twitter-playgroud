import os
import datetime
import tweepy

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token)

user_name = input("Enter Twitter user: ")

response = client.get_user(username=user_name)
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

print(tweet_includes)
print()
for tweet in tweets:
    print(tweet.id)
    print(tweet.text)
    media_keys = tweet.data.get("attachments", {}).get("media_keys", [])
    print(media_keys)
    for media_key in media_keys:
        for media in media_objects:
            if media.media_key == media_key:
                #print(media.type)
                #print(media.data)
                if media.preview_image_url is not None:
                    print(media.preview_image_url)
    print()
