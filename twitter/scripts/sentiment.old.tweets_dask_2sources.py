from textblob import TextBlob
import GetOldTweets3 as got
import pandas as pd
from datetime import date, timedelta

# DASK
import dask as dask
from dask.distributed import Client, progress
import dask.dataframe as dd

client = Client()
client

from dask import delayed
                


# LOOP 
years = 1
daily_tweets = 3


d1 = date(2019-years, 12, 28)  # start date
d2 = date(2019, 1, 1)  # end date

delta = d2 - d1         # timedelta

dates=[]
for i in range(delta.days + 1):
    j = str(d1 + timedelta(i))
    dates.append(j)


           
# RETRIEVE AND OBTAIN SENTIMENT
  
sources = ['eleconomista', 'ElFinanciero_Mx','El_Universal_Mx']
    
    
keywords = ['america movil','banco de mexico', 'mexico', 'bmv', 'bolsa mexicana de valores', 'bolsa mexicana',
            'ipc', 'gobierno de mexico',
             'walmex','femsa','televisa', 'grupo mexico','banorte','cemex','grupo alfa', 
            'peñoles', 'inbursa', 'elektra', 'mexichem', 'bimbo', 'arca continental', 'kimberly-clark',
            'genomma lab', 'puerto de liverpool', 'grupo aeroportuario', 'banco compartamos', 'alpek', 'ica',
            'tv azteca', 'ohl', 'maseca', 'alsea', 'carso', 'lala', 'banregio', 'comercial mexicana',
            'ienova', 'pinfra', 'santander mexico', 'presidente de mexico','cetes']          




@delayed
def daily_tweets_func(i, dates, keywords,sources, daily_tweets):       
    
    i=i+1
    globals()['data%s'%1]=pd.DataFrame({'Date':[dates[i]]*daily_tweets})
    
    for source in sources:
        
        for keyword in keywords:
            
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword)\
                                                           .setUsername(source)\
                                                           .setSince(dates[i-1])\
                                                           .setUntil(dates[i])\
                                                           .setMaxTweets(daily_tweets)
            
            pos_neg = []                                              
            for j in range(daily_tweets):
                lista_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                if len(lista_tweets)<=j:
                    
                    s = 0
                                       
                                
                else:
                    
                    tweet = lista_tweets[j]
                    #print(tweet.text)
                    analysis = TextBlob(tweet.text)
                    #print(analysis.sentiment)
                    if analysis.sentiment[0]>0:
                        s=1 #positive puse 1 
                    else:                   # Esto para generar distintas combinaciones al sumar
                        s=2 #negative puse 2 
                                   

                #tweets.append(tui) No necesito guardar los tweets, solo las calificaciones
                pos_neg.append(s)
               
                if len(pos_neg)==daily_tweets:
                    globals()['data%s'%1][source+'_'+keyword]=pos_neg
    
    globals()['data%s'%1].to_csv('tweets/1.5_years_26marzo/2016/'+str(dates[i])+'_'+str(daily_tweets)+'tweets.csv')     
    return globals()['data%s'%1]          


var_l=[]
dataframes = []
for i in range(len(dates)):
    
    if i+1 > len(dates):
        break
    else:
        globals()['data%s'%str(i+1)] = daily_tweets_func(i,dates,keywords,sources, daily_tweets)
        
        dataframes.append(globals()['data%s'%str(i+1)])
        
        nvar = 'data'+str(i+1)
        var_l.append(nvar)

var_l.pop()
dataframes.pop()


@delayed
def create_variables(dataframes):
    
    variables = pd.concat(dataframes, axis=0)
    return variables

"""
@delayed
def create_variables(data1,data2,data3):
    
    variables = pd.concat([data1,data2,data3], axis=0)
    return variables
"""

data_final = create_variables(dataframes)

data_final = data_final.compute()
