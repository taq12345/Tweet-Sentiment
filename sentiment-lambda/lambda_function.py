import tweepy
from textblob import TextBlob
import time
import re
import json


def lambda_handler(event, context):
    # Go to http://apps.twitter.com and create an app.
    # The consumer key and secret will be generated for you after
    consumer_key = "--------"
    consumer_secret = "--------"

    # After the step above, you will be redirected to your app's page.
    # Create an access token under the the "Your access token" section
    access_token = "--------"
    access_token_secret = "--------"

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    count = 0
    data = {'dates': [], 'polarities': []}
    start = time.time()
    query = event['queryStringParameters']['query']
    print("query: ", query)
    #query = 'love'
    for status in tweepy.Cursor(api.search, lang='en', q=query, type='recent', count=100,
                                tweet_mode='extended').items():
        # process status here
        # print(status.created_at)
        text = status.full_text
        date = str(status.created_at)
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub('rt @[A-Za-z0-9]+', '', text)
        text = re.sub('@[A-Za-z0-9]+', '', text)
        # print(text)
        for letter in text:
            if (letter < chr(97) or letter > chr(122)) and letter is not chr(32):
                if letter is not chr(10):
                    text = text.replace(letter, '')
        text = text.strip()

        # print('\n')
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        count += 1
        data['dates'].append(date)
        data['polarities'].append(polarity)

        if time.time() - start > 25 or count >= 1500:
            print(count)
            break
 
    avgs = []
    mid_dates = []
    sum = 0
    batch_size = 25
    for i in range(len(data['polarities'])):
        if i % batch_size == 0 and i != 0:
            avgs.append(sum / batch_size)
            mid_dates.append(data['dates'][i])
            sum = 0

        sum = sum + data['polarities'][i]

    data['dates'] = mid_dates
    data['polarities'] = avgs
    # print(avgs)
    # print(mid_dates)
    # print(len(avgs))
    # print(len(mid_dates))
    # print(query)
    # print(count)
    # print(event)
    #print(data)

    pointData = [];
    for i in range(len(data["dates"])):
        pointData.append({
            'x': i,
            'y': data['polarities'][i]
        })

    #print(pointData)

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(pointData)
    }
    print(response)
    return response