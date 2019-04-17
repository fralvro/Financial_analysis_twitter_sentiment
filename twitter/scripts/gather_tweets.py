from textblob import TextBlob
import GetOldTweets3 as got

# Usados en este programa
import pandas as pd
from datetime import date, timedelta
import glob 
from yahoo_historical import Fetcher
import numpy as np
# Usados en este programa


# DASK
import dask as dask
from dask.distributed import Client, progress
import dask.dataframe as dd

client = Client()
client

from dask import delayed

"""
#1
                        ----- Información inicial-----
"""

#datos2 = pd.read_csv('tweets/1.5_years_26marzo/2019/2018-01-07_3tweets.csv',index_col=0)

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


d1 = date(2017, 1, 1)  # start date, revisar que cuadre con quandl abajo
d2 = date(2019, 3, 26)  # end date, revisar que cuadre con quandl abajo

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
por_fuente = por_fuente.set_index('Date')
    
## Intento 2: Cuento los tweets negativos/positivos por tema (41)

por_tema = pd.DataFrame()
for fuente in keywords:
    
    filter_col = [col for col in frame.columns if str(fuente) in col]
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

    
    por_tema[str(fuente+'_positivos')] = globals()['pos_%s' % fuente]
    por_tema[str(fuente+'_negativos')] = globals()['neg_%s' % fuente]
    por_tema[str(fuente+'_neutros')] = globals()['neu_%s' % fuente]
por_tema['Date'] = fechas_real
por_tema = por_tema.set_index('Date')


## Intento 3: Combino la información de intento 1 y 2 

mix_fuente_tema = por_tema.join(por_fuente)

## Intento 4: Cuento los totales negativos/positivos por tema_fuente (124)

por_fuente_tema = pd.DataFrame()

for source in sources:
    
    for keyword in keywords:

        fuente = str(source)+'_'+str(keyword)
        
    
        filter_col = [col for col in frame.columns if str(fuente) in col]
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
    
        
        por_fuente_tema[str(fuente+'_positivos')] = globals()['pos_%s' % fuente]
        por_fuente_tema[str(fuente+'_negativos')] = globals()['neg_%s' % fuente]
        por_fuente_tema[str(fuente+'_neutros')] = globals()['neu_%s' % fuente]
por_fuente_tema['Date'] = fechas_real
por_fuente_tema = por_fuente_tema.set_index('Date')

## Intento 5: Mezclo todo (168)

mix_todo = por_fuente_tema.join(mix_fuente_tema)

"""
Realmente las mezclas no deberían representar una mejora en el desempeño 
del modelo predictivo, ya que la información se vuelve redundante. Son 
los mismos datos contados de maneras distintas, pero no aportan información
adicional al modelo.
"""
 

"""
#2
 ~~~////////////     AÑADO INFORMACIÓN FINANCIERA      \\\\\\\\\\\\\\\\~~~


Supongo que al añadir la varianza de los datos de apertura, cierre, alto y 
bajo como porcentaje del precio de cierre y apertura respectivamente 
como variables explicativas, podré tener mejor desempeño predictivo, ya que 
incluyo información del movimiento de los precios durante el día.

También incluyo el rango de la apertura/cierre bajo el mismo principio

Considero que incluir el volumen de transacciones también puede ser una variable
explicativa interesante

"""
# Extraigo Información de Yahoo

import fix_yahoo_finance as yf  
yahoo = yf.download("^MXX",'2017-01-01','2019-03-26') # Revisar que las fechas
# coincidan con el rango de los tweets


from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='8RC8G9RS7DXBFN4M', output_format='pandas')
data, meta_data = ts.get_daily(symbol='MSFT', outputsize='full')

# Transformo información relativa a datos del día 

v_apertura=[]
v_cierre=[]
r_ap_ci=[]
vol_tr=[]
ap_nxd=[]
fecha=[]

for i in range(len(yahoo)):
    
    if i == len(yahoo)-1:
        break
    else:

        list_var = [yahoo.iloc[i,0],yahoo.iloc[i,1],yahoo.iloc[i,2],
                    yahoo.iloc[i,3]]
        
        var_apertura = np.var(list_var)/list_var[0]
        var_cierre = np.var(list_var)/list_var[3]
        range_ap_ci = list_var[0]/list_var[3]
        vol_trans = yahoo.iloc[i,5] # No entiendo el dato en el que el vol=0, puede
        # ser por un día que no abre el mercado. Existe eso? Le pongo la media de los datos?
        
        v_apertura.append(var_apertura)
        v_cierre.append(var_cierre)
        r_ap_ci.append(range_ap_ci)
        vol_tr.append(vol_trans)
        fecha.append(str(yahoo.index[i])[:10])
        
        """
                               ---- VARIABLE A PREDECIR ----
        
        Predigo la diferencia del precio de apertura del siguiente día con el precio de 
        cierre del día corriente en porcentaje. 
        
        """
        
        ap_sig_d = (yahoo.iloc[(i+1),0]-yahoo.iloc[i,3])/yahoo.iloc[i,3]
        ap_nxd.append(ap_sig_d)


datos_fin = pd.DataFrame({'var_rel_apertura':v_apertura, 'var_rel_cierre':v_cierre,
                          'rate_ap_cierre':r_ap_ci,'volume':vol_tr,
                          'apertura_next_day':ap_nxd, 'Dates':fecha})
    
    
    
"""
#3

          ----- JUNTO DATAFRAMES DE TWEETS CON INFO FINANCIERA -----
 
Los junto y los guardo como csv
         
"""

# Reviso que en la info financiera estén todas las fechas que puse en los tweets.

fechas_faltantes_fin = list(set(fechas_real)-set(datos_fin['Dates']))

"""
2 APROXIMACIONES PARA LA UNIÓN DE TWEETS CON INFO FINANCIERA

--- PRIMERA APROXIMACIÓN
    INCLUIR SENTIMIENTO DE FECHAS FALTANTES EN DÍA ANTERIOR ---
    
    La idea es incluir el sentimiento de los tweets de los días no laborables
    dentro de la fecha anterior inmediata de la serie de tiempo. Ej: sentimiento
    de sábado y domingo incluirlo en viernes para predecir lunes.
    
"""


fin_index = datos_fin.set_index('Dates')          

# 1 Por fuente 

por_fuente_fin = por_fuente.join(fin_index)

por_fuente_fin.index = pd.to_datetime(por_fuente_fin.index)

por_fuente_fin = por_fuente_fin.sort_index()

# 1.1  APROXIMACIÓN 1 POR FUENTE

# para mañana: Convertir los new_columns en un dataFrame que se pueda join al
# dataFrame una_fuente y eliminar los anteriores. No olvidar normalizarlo por renglón también
        
por_fuente_loop = por_fuente_fin
new_columns=[]
count=[]
for i in range(len(datos_fin)): # Uso datos_fin porque en teoría deberían de quedar
    #ambos conjuntos del mismo tamaño
    
    if np.isnan(por_fuente_loop.iloc[i,13])==True:
        por_fuente_loop=por_fuente_loop.drop(por_fuente_loop.index[i])
        
    if i > len(datos_fin)-10:
        k= len(datos_fin)-i
                                         # Acá hago que la comparativa sea con
                                         # Las 10 siguientes, pero si me aproximo
                                         # al final, lo reduzco para no salir 
                                         # del margen
    if i <= len(datos_fin)-10:
        k=10
    
    
    if np.isnan(por_fuente_loop.iloc[i,13])==False:
        
        
        for j in range(k): # este for evalúa si en las siguientes filas hay nan consecutivos 
            
            j = k-j # Voy del más repetido al menos repetido
            
            
            
            if all(np.isnan(por_fuente_loop.iloc[i+1:i+j,13])==True)==True:
                
                print(j)
                
                suma = (por_fuente_loop.iloc[i:i+j,0:9]).sum(axis=0) # Es desde i
                #porque se le suman a la fila actual
                
                rows_to_drop = list(por_fuente_loop.index[i+1:i+j])
                por_fuente_loop=por_fuente_loop.drop(rows_to_drop)
                new_columns.append(suma)
    
                break




# 2 