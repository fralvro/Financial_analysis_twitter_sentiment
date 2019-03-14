
from textblob import TextBlob
import GetOldTweets3 as got


# Old Tweets

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('obama')\
                                           .setSince("2015-05-01")\
                                           .setUntil("2015-09-30")\
                                           .setTopTweets(True)\
                                           .setMaxTweets(10)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

print(tweet.text)
analysis = TextBlob(tweet.text)
print(analysis.sentiment)
if analysis.sentiment[0]>0:
	print('Positive')
else:
	print('Negative')
print("")


# LOOP 
years = 2

for year in range(years):
    year_a = 2019-year
    months = 12 
    for month in range(months+1):
        if (month == 4) or (month == 6) or (month == 9) or (month == 11):
            days = 30
        if (month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12):
            days = 31
        else: 
            if year_a= 3:
                days = 29
            else:
                days=28
                for day in days:
                    print([year_a,month,days])

            
        for day in day:
        
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch('IPC')\
                                                       .setSince("2015-05-01")\
                                                       .setUntil("2015-09-30")\
                                                       .setMaxTweets(10)


