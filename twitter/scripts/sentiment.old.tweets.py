from textblob import TextBlob
import GetOldTweets3 as got
import pandas as pd
from datetime import date, timedelta



# LOOP 
years = 1
daily_tweets = 50


d1 = date(2019-years, 3, 24)  # start date
d2 = date(2019, 3, 19)  # end date

delta = d2 - d1         # timedelta

dates=[]
for i in range(delta.days + 1):
    j = str(d1 + timedelta(i))
    dates.append(j)


           
# RETRIEVE AND OBTAIN SENTIMENT
  
sources = ['eleconomista', 'ElFinanciero_Mx']
    
keywords = ['america movil','banco de mexico', 'mexico', 'bmv', 'bolsa mexicana de valores', 'bolsa mexicana',
            'ipc', 'gobierno de mexico',
             'walmex','femsa','televisa', 'grupo mexico','banorte','cemex','grupo alfa', 
            'peñoles', 'inbursa', 'elektra', 'mexichem', 'bimbo', 'arca continental', 'kimberly-clark',
            'genomma lab', 'puerto de liverpool', 'grupo aeroportuario', 'banco compartamos', 'alpek', 'ica',
            'tv azteca', 'ohl', 'maseca', 'alsea', 'carso', 'lala', 'banregio', 'comercial mexicana',
            'ienova', 'pinfra', 'santander mexico', 'presidente de mexico','cetes']          

#random.choice(keywords)  47
#tweets = [] No necesito guardar los tweets, solo las calificaciones
a=0
df_list = []

for i in range(len(dates)):
    
    i=i+1
    data1 = pd.DataFrame({'Date':[dates[i]]*daily_tweets})
    
    for keyword in keywords:
        
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword)\
                                                       .setSince(dates[i-1])\
                                                       .setUntil(dates[i])\
                                                       .setMaxTweets(daily_tweets)
        
        pos_neg = []                                              
        for j in range(daily_tweets):
            lista_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            if len(lista_tweets)<=j:
                
                s = 'na'
                                   
                            
            else:
                
                tweet = lista_tweets[j]
                #print(tweet.text)
                analysis = TextBlob(tweet.text)
                #print(analysis.sentiment)
                if analysis.sentiment[0]>0:
                    s=1 #positive
                else:
                    s=0 #negative
                               
                
            print(s)
            a=a+1
            print(a)
            print(keyword)
            #tweets.append(tui) No necesito guardar los tweets, solo las calificaciones
            pos_neg.append(s)
           
            if len(pos_neg)==daily_tweets:
                data1[keyword]=pos_neg
    
    data1.to_csv('Documents/tweets/'+str(dates[i])+'_'+str(daily_tweets)+'tweets.csv')       
                

                

