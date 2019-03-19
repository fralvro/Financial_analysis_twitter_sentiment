
from textblob import TextBlob
import GetOldTweets3 as got
import pandas as pd




# LOOP 
years = 2
daily_tweets = 25

dates=[]
for year in range(years):
    year_a = 2019-year
    months = 12 
    for month in range(months):
        month = month+1

        if month == 6 or month == 4 or month == 9 or month == 11:
            days = 30
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            days = 31
        else: 
            if year_a == 2016 or year_a == 2004 or year_a == 2008 or year_a == 2012 or year_a == 2016:
                days = 29
            else:
                days=28      
    
        for day in range(days):
            yyyy = str(year_a)
            mm = str(month).zfill(2)
            dd = str(day+1).zfill(2)
            #print(yyyy+'-'+mm+'-'+dd)
            dateymd= str(yyyy+'-'+mm+'-'+dd)
            dates.append(dateymd)

            
# RETRIEVE AND OBTAIN SENTIMENT
  
keywords = ['america movil','banco de mexico', 'mexico', 'bmv', 'bolsa mexicana de valores', 'mexbol', 'bolsa mexicana', 'el economista',
            'el financiero', 'mexico stock', 'ipc', 'gobierno de mexico',
             'walmex','femsa','televisa', 'grupo mexico','banorte','cemex','grupo alfa', 
            'peñoles', 'inbursa', 'elektra', 'mexichem', 'bimbo', 'arca continental', 'kimberly-clark',
            'genomma lab', 'puerto de liverpool', 'grupo aeroportuario', 'banco compartamos', 'alpek', 'ica',
            'tv azteca', 'ohl', 'maseca', 'alsea', 'carso', 'lala', 'banregio', 'comercial mexicana',
            'ienova', 'pinfra', 'santander mexico', 'presidente de mexico', 'mexican government', 'president of mexico','cetes']          

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
    #df_list.append(data1)
                
                
              

                
#data_twitter= pd.concat(df_list, ignore_index=True)
            
            
                
                

