import os
import datetime
import tweepy

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token)

# from https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9
# Replace the limit=1000 with the maximum number of Tweets you want
# for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
#                               tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000):
#     print(tweet.id)


# Enter text for basic search
search_text = input("Search text: ")

# run search
now = datetime.datetime.now()
time_delta = datetime.timedelta(days=1)
start_time = now - time_delta

search_response = client.search_recent_tweets(
    query=search_text,
    start_time=start_time,
    expansions="attachments.media_keys",
    media_fields=["media_key", "type", "url", "width", "height", "duration_ms", "preview_image_url", "public_metrics"],    
)

# find tweets with images and build slide show
media_objects = search_response.includes.get("media", [])
if search_response.data is not None:
    for tweet in search_response.data:
        # print(tweet)
        print(tweet.text)
        media_keys = tweet.data.get("attachments", {}).get("media_keys", [])
        for media_key in media_keys:
            for media_object in media_objects:
                if media_object.media_key == media_key:
                    if media_object.url is not None:
                        print("  ", media_object.url)

# TODO: am I missing tweets from retweets?
# TODO: confirm this works with animated gifs