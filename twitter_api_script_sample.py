"""

Script to collect the Twitter timelines of selected Twitter accounts.

"""

"""Import necessary packages"""
import configparser
import tweepy
import time
import csv
import datetime
from emoji_unicode_codes import emoji_unicode

def main():

    """Write emoji functions"""

    # Define emoji replacement function
    def replace_emoji(text, dic):
        for i, j in dic.items():
            text = text.replace(i, ' '+j+' ')
        return text

    # Define emoji counting function
    def count_emoji(text, dic):
        emoji_list = []
        emoji_count = 0
        for i, j in dic.items():
            emoji_list.append(i)        
        for word in emoji_list:
            emoji_count += text.count(word)
        return emoji_count

    # Switch keys and values in emoji dict
    emojidict = {y:x for x,y in emoji_unicode.items()}

    """Set up CSV file"""

    # Create date variable for naming csv files
    today_string = datetime.datetime.today().strftime('%Y%m%d')

    # Open csv file writer and write headers to first line
    outfile_path='YOUR FILENAME HERE'+today_string+'.csv'
    writer = csv.writer(open(outfile_path, 'w', newline='', encoding="UTF-8"))
    headers = ['screen_name', 'user_id', 'acct_created', 'followers_count', 'statuses_count', 
                'friends_count', 'tweet_id', 'date', 'tweet_text', 'retweet_count', 
                'favorited', 'url1', 'url2', 'url3', 'url4', 'url5', 'hashtag1', 'hashtag2', 'hashtag3', 
                'hashtag4', 'hashtag5', 'hashtag6', 'hashtag7', 'hashtag8', 'hashtag9', 'hashtag10', 
                'hashtag11', 'hashtag12', 'hashtag13', 'hashtag14', 'hashtag15', 'hashtag16', 
                'hashtag17', 'hashtag18', 'hashtag19', 'hashtag20', 'user_mention1', 'user_mention2', 
                'user_mention3', 'user_mention4', 'user_mention5', 'user_mention6', 'user_mention7', 
                'user_mention8', 'user_mention9', 'user_mention10', 'user_mention11', 
                'user_mention12', 'user_mention13', 'user_mention14', 'user_mention15', 
                'user_mention16', 'user_mention17', 'user_mention18', 'user_mention19', 
                'user_mention20', 'media_type', 'retweet', 'emoji_count', 'media_url']
    writer.writerow(headers)

    """Authenticate your app"""

    # Read the config file
    config = configparser.ConfigParser()
    config.read('YOUR FILENAME HERE')

    # Set all of the variables we need for Twitter
    consumer_key = config['Twitter']['consumer_key']
    consumer_secret = config['Twitter']['consumer_secret']
    access_token = config['Twitter']['access_token']
    access_token_secret = config['Twitter']['access_token_secret']

    # Authenticate with Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create an API object to use
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    """Determine the accounts you want to collect tweets from"""

    # Create list of Twitter accounts to collect
    account_names = ['LIST OF ACCOUNT HANDLES HERE']

    """Extract the information you want"""

    # Get the tweets
    for account in account_names:

        result = tweepy.Cursor(api.user_timeline, id=account, count=200, include_rts=1)

        # Write to csv file
        for page in result.pages():
            for tweet in page:
                row = []
                row.append(str(tweet.user.screen_name))
                row.append(str(tweet.user.id_str))
                row.append(str(tweet.user.created_at))
                row.append(int(tweet.user.followers_count))
                row.append(int(tweet.user.statuses_count))
                row.append(int(tweet.user.friends_count))
                row.append(str(tweet.id_str)+'x')
                row.append(str(tweet.created_at))
                if hasattr(tweet, 'retweeted_status'):
                    text = replace_emoji(tweet.retweeted_status.text, emojidict)
                    row.append(str(text.replace('\n', '').replace('\r', '')))
                else:
                    text = replace_emoji(tweet.text, emojidict)
                    row.append(str(text.replace('\n', '').replace('\r', '')))
                row.append(int(tweet.retweet_count))
                row.append(str(tweet.favorited))
                if tweet.entities['urls']:
                    for count, url in enumerate(tweet.entities['urls'], start=1):
                        row.append(str(url['expanded_url']))
                    if count < 5:
                        for i in range(5-count):
                            row.append('')
                else:
                    for i in range(5):
                        row.append('')
                if tweet.entities['hashtags']:
                    for count, hashtag in enumerate(tweet.entities['hashtags'], start=1):
                        row.append(str(hashtag['text']))
                    if count < 20:
                        for i in range(20-count):
                            row.append('')
                else:
                    for i in range(20):
                        row.append('')
                if tweet.entities['user_mentions']:
                    for count, mention in enumerate(tweet.entities['user_mentions'], start=1):
                        row.append(str(mention['screen_name']))
                    if count < 20:
                        for i in range(20-count):
                            row.append('')    
                else:
                    for i in range(20):
                        row.append('')
                if 'media' in tweet.entities:
                    row.append(str(tweet.entities['media'][0]['type']))
                else:
                    row.append('')
                if hasattr(tweet, 'retweeted_status'):
                    row.append(str('TRUE'))
                    emoji_count = count_emoji(tweet.retweeted_status.text, emojidict)
                    row.append(int(emoji_count))
                else:
                    row.append(str('FALSE'))
                    emoji_count = count_emoji(tweet.text, emojidict)
                    row.append(int(emoji_count))
                if 'media' in tweet.entities:
                    row.append(str(tweet.entities['media'][0]['media_url']))
                else:
                    row.append('')
                writer.writerow(row)

        """Respect the rate limit"""

        # Wait 60 seconds after each account to stay within rate limit
        print('Account {} done'.format(account))
        time.sleep(60)


if __name__ == '__main__':
    main()

