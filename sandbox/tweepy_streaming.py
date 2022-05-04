import os
import datetime
import tweepy

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

# globals - should probably be in stream class as well as some other functionality -
timestamp = datetime.datetime.now()
tweet_filename = "{}-tweets.jsonl".format(timestamp)
media_filename = "{}-media.jsonl".format(timestamp)

tweet_file = open(tweet_filename, 'w')
media_file = open(media_filename, 'w')

class MyStream(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        # print(dir(tweet))
        print(tweet.data)
        print()
        tweet_file.write("{}\n".format(tweet.data))

    # looks like this is separate so assuming need to write to separate jsonl output and merge later
    def on_includes(self, includes):
        for media in includes.get('media', []):
            print(media.data)
            media_file.write("{}\n".format(media.data))
        print()

#streaming_client = tweepy.StreamingClient(bearer_token=bearer_token)
streaming_client = MyStream(
    bearer_token=bearer_token,
    return_type=dict,
)

# delete any existing rules and start over
rules = streaming_client.get_rules().get('data')
#rules = streaming_client.get_rules().data
if len(rules) > 0:
    print("Deleting existing rules before beginning")
for rule in rules:
    print("..deleting rule: id={}, value={}".format(rule.get('id'), rule.get('value')))
    #print("..deleting rule: id={}, value={}".format(rule.id, rule.value))
    streaming_client.delete_rules(rule.get('id'))
    #streaming_client.delete_rules(rule.id)

# get rule
rule_value = input("Enter rule: ")
stream_rule = tweepy.StreamRule(value=rule_value)  #TODO: is this what this is doing?...just searching for text?...diff b/t tags?
#streaming_client.add_rules(stream_rule, dry_run=True)
streaming_client.add_rules(stream_rule)

# start stream
try:
    print()
    print("starting stream")
    print("..press Ctrl-C to stop")
    streaming_client.filter(
        expansions="attachments.media_keys",
        media_fields=["media_key", "type", "url", "width", "height", "duration_ms", "preview_image_url", "public_metrics"],
    )
except KeyboardInterrupt:
    print("..ending script")
    streaming_client.disconnect()
tweet_file.close()
media_file.close()