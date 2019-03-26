
import GetOldTweets3 as got


# Get tweets by username(s):
tweetCriteria = got.manager.TweetCriteria().setUsername("ElFinanciero_Mx")\
                                           .setMaxTweets(1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)


tweetCriteria = got.manager.TweetCriteria().setQuerySearch('mexico')\
                                               .setUsername()\
                                               .setSince("2015-05-01")\
                                               .setUntil("2015-05-02")\
                                               .setMaxTweets(1)




#Get tweets by query search:

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('eleconomista')\
                                           .setSince("2015-05-01")\
                                           .setUntil("2015-09-30")\
                                           .setMaxTweets(1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)
data = tweet



# Get tweets by username and bound dates:

tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama")\
                                           .setSince("2015-09-10")\
                                           .setUntil("2016-01-01")\
                                           .setMaxTweets(1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)



# Get the last 10 top tweets by username:

tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama")\
                                           .setTopTweets(True)\
                                           .setMaxTweets(10)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)








