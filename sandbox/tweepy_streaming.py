import os
import datetime
import tweepy

class MyStream(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        print(tweet.id, tweet)

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

#streaming_client = tweepy.StreamingClient(bearer_token=bearer_token)
streaming_client = MyStream(
    bearer_token=bearer_token,
    return_type=dict,
)

# delete any existing rules and start over
rules = streaming_client.get_rules().get('data')
if len(rules) > 0:
    print("Deleting existing rules before beginning")
for rule in rules:
    print("..deleting rule: id={}, value={}".format(rule.get('id'), rule.get('value')))
    streaming_client.delete_rules(rule.get('id'))

# get rule
rule_value = input("Enter rule: ")
stream_rule = tweepy.StreamRule(value=rule_value)  #TODO: is this what this is doing?...just searching for text?...diff b/t tags?
#streaming_client.add_rules(stream_rule, dry_run=True)
streaming_client.add_rules(stream_rule)

# start stream
print("Starting stream")
streaming_client.filter()
