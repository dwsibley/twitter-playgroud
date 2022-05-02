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

user_name = input("Enter Twitter user: ")

response = client.get_user(username=user_name)
user_id = response.data.id

end_time = datetime.datetime.now()
time_delta = datetime.timedelta(days=100)
start_time = end_time - time_delta

tweet_cnt = 0
for tweet in tweepy.Paginator(
    client.get_users_tweets,
    id = user_id,
    start_time = start_time,
    end_time = end_time,
    #media_fields = [{"type":"video"}],
    expansions="attachments.media_keys",
    media_fields=["media_key", "type", "url", "height", "duration_ms", "preview_image_url"],
    max_results=100).flatten(limit=1000):
    tweet_cnt += 1
    print(tweet.id)

print("captured this many tweets: {}".format(tweet_cnt))