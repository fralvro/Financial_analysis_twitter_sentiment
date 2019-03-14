By Arun Kurian

Sentiment Analysis, also called opinion mining or emotion AI, is the process of determining whether a piece of writing is positive, negative, or neutral. A common use case for this technology is to discover how people feel about a particular topic. Sentiment analysis is widely applied to reviews and social media for a variety of applications.

Sentiment analysis can be performed in many different ways. Many brands and marketers use keyword-based tools that classify data (i.e. social, news, review, blog, etc.) as positive/negative/neutral.

Automated sentiment tagging is usually achieved through word lists. For example, mentions of ‘hate’ would be tagged negatively.

There can be two approaches to sentiment analysis.

1. Lexicon-based methods
2. Machine Learning-based methods.

In this problem, we will be using a Lexicon-based method.

Lexicon based methods define a list of positive and negative words, with a valence — (eg ‘nice’: +2, ‘good’: +1, ‘terrible’: -1.5 etc). The algorithm looks up a text to find all known words. It then combines their individual results by summing or averaging. Some extensions can check some grammatical rules, like negation or sentiment modifier (like the word “but”, which weights sentiment values in text differently, to emphasize the end of text).

Let’s build the analyzer now.

Twitter API
Before we start coding, we need to register for the Twitter API https://apps.twitter.com/. Here we need to register an app to generate various keys associated with our API. The Twitter API can be used to perform many actions like create and search.

Now after creating the app we can start coding.

We need to install two packages:

pip install tweepy
This package will be used for handling the Twitter API.

pip install textblob
This package will be used for the sentiment analysis.

sentiment_analyzer.py

import tweepy
from textblob import TextBlob
We need to declare the variables to store the various keys associated with the Twitter API.

consumer_key = ‘[consumer_key]’
consumer_key_secret = ‘[consumer_key_secret]’
access_token = ‘[access_token]’
access_token_secret = ‘[access_token_secret]’
The next step is to create a connection with the Twitter API using tweepy with these tokens.

Tweepy
Tweepy supports OAuth authentication. Authentication is handled by the tweepy.OAuthHandler class.

An OAuthHandler instance must be created by passing a consumer token and secret.

On this auth instance, we will call a function set_access_token by passing the access_token and access_token_secret.

Finally, we create our tweepy API instance by passing this auth instance into the API function of tweepy.

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
We can now search Twitter for any topic using the search method of the API.

public_tweets = api.search(‘Dogs’)
Now we will be getting all the tweets related to the topic ‘Dogs’. We can perform sentiment analysis using the library textblob.

TextBlob
TextBlob is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.

A textblob can be created in the following way (example, and not part of the original code):

example = TextBlob("Python is a high-level, general-purpose programming language.")
And tokenization can be performed by the following methods:

words: returns the words of text

usage:

example.words
sentences: returns the sentences of text

usage:

example.sentences
Part-of-speech Tagging
Part-of-speech tags can be accessed through the tags property.

wiki.tags
[('Python', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('high-level', 'JJ'), ('general-purpose', 'JJ'), ('programming', 'NN'), ('language', 'NN')]
Sentiment Analysis
The sentiment property returns a named tuple of the form Sentiment (polarity, subjectivity). The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.


We can iterate the publice_tweets array, and check the sentiment of the text of each tweet based on the polarity.


Execute: python3 analyzer.py
