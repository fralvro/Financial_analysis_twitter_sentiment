from textblob import TextBlob
import GetOldTweets3 as got

# Usados en este programa
import pandas as pd
from datetime import date, timedelta
import glob 
# Usados en este programa


# DASK
import dask as dask
from dask.distributed import Client, progress
import dask.dataframe as dd

client = Client()
client

from dask import delayed

# Información inicial

datos2 = pd.read_csv('tweets/1.5_years_26marzo/2019/2018-01-07_3tweets.csv',index_col=0)

sources = ['eleconomista', 'ElFinanciero_Mx','El_Universal_Mx']
    
    
keywords = ['america movil','banco de mexico', 'mexico', 'bmv', 'bolsa mexicana de valores', 'bolsa mexicana',
            'ipc', 'gobierno de mexico',
             'walmex','femsa','televisa', 'grupo mexico','banorte','cemex','grupo alfa', 
            'peñoles', 'inbursa', 'elektra', 'mexichem', 'bimbo', 'arca continental', 'kimberly-clark',
            'genomma lab', 'puerto de liverpool', 'grupo aeroportuario', 'banco compartamos', 'alpek', 'ica',
            'tv azteca', 'ohl', 'maseca', 'alsea', 'carso', 'lala', 'banregio', 'comercial mexicana',
            'ienova', 'pinfra', 'santander mexico', 'presidente de mexico','cetes']          


# - De entrada junto todos los .csv dentro de la carpeta 2019 en frame

path = 'tweets/1.5_years_26marzo/2019' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, )
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)




# - Listo todas las fechas de las que supuestamente he obtenido tweets y comparo
# con lo que realmente descargué para obtener las fechas faltantes 


d1 = date(2017, 1, 1)  # start date
d2 = date(2019, 3, 26)  # end date

delta = d2 - d1         # timedelta

dates=[]
for i in range(delta.days + 1):
    j = str(d1 + timedelta(i))
    dates.append(j)


fechas_real = list(set(frame['Date']))

fechas_faltantes = list(set(dates) - set(fechas_real))

# Transformo los DataFrames para recolectar la inforamción que necesito

## Intento 1: Cuento los tweets negativos/positivos por fuente (3)

por_fuente = pd.DataFrame()
for fuente in sources:
    
    filter_col = [col for col in frame if col.startswith(fuente)]
    filter_col.append('Date')
    fr_int1 = frame[filter_col]
    
    globals()['pos_%s' % fuente] = []
    globals()['neg_%s' % fuente] = []
    globals()['neu_%s' % fuente] = []
    

    for fecha in fechas_real:
    
        dframe = fr_int1.loc[fr_int1['Date'] == fecha]
        positivo = dframe[dframe[filter_col] == 1].count().sum()
        negativo = dframe[dframe[filter_col] == 2].count().sum()
        neutro = dframe[dframe[filter_col] == 0].count().sum()

        globals()['pos_%s' % fuente].append(positivo)
        globals()['neg_%s' % fuente].append(negativo)
        globals()['neu_%s' % fuente].append(neutro)

    
    por_fuente[str(fuente+'_positivos')] = globals()['pos_%s' % fuente]
    por_fuente[str(fuente+'_negativos')] = globals()['neg_%s' % fuente]
    por_fuente[str(fuente+'_neutros')] = globals()['neu_%s' % fuente]
por_fuente['Date'] = fechas_real
    
    
## Intento 2: Cuento los tweets negativos/positivos por tema (41)

## Intento 3: Combino la información de intento 1 y 2 

## Intento 4: Cuento los totales negativos/positivos por tema_fuente (124)

## Intento 5: Mezclo todo (168)

