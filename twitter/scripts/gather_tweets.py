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
data = Fetcher("^MXX", [2016,12,31], [2019,3,26]) #Reviso que las fechas estén 
# en el rango de las fechas_real

yahoo = data.getHistorical()

#yahoo_dat = yahoo.set_index('Date')


# Transformo información relativa a datos del día 

v_apertura=[]
v_cierre=[]
r_ap_ci=[]
vol_tr=[]
ap_nxd=[]
fechas=[] #lo hago así para asegurar que el orden de las fechas no vaya a cambiar 

for i in range(len(yahoo)):
    
    if i == len(yahoo)-1:
        break
    else:

        list_var = [yahoo.iloc[i,1],yahoo.iloc[i,2],yahoo.iloc[i,3],
                    yahoo.iloc[i,4]]
        
        var_apertura = np.var(list_var)/list_var[0]
        var_cierre = np.var(list_var)/list_var[3]
        range_ap_ci = list_var[0]/list_var[3]
        vol_trans = yahoo.iloc[i,6] # No entiendo el dato en el que el vol=0, puede
        # ser por un día que no abre el mercado. Existe eso? Le pongo la media de los datos?
        
        v_apertura.append(var_apertura)
        v_cierre.append(var_cierre)
        r_ap_ci.append(range_ap_ci)
        vol_tr.append(vol_trans)
        fechas.append(yahoo.iloc[i,0])
        
        
        """
                               ---- VARIABLE A PREDECIR ----
        
        Predigo la diferencia del precio de apertura del siguiente día con el precio de 
        cierre del día corriente en porcentaje. 
        
        """
        
        ap_sig_d = (yahoo.iloc[(i+1),1]-yahoo.iloc[i,4])/yahoo.iloc[i,4]
        ap_nxd.append(ap_sig_d)


datos_fin = pd.DataFrame({'var_rel_apertura':v_apertura, 'var_rel_cierre':v_cierre,
                          'rate_ap_cierre':r_ap_ci,'volume':vol_tr,
                          'apertura_next_day':ap_nxd, 'Date':fechas})
    
    
    
"""
#3

          ----- JUNTO DATAFRAMES DE TWEETS CON INFO FINANCIERA -----
 
Los junto y los guardo como csv
         
"""

fin_index = datos_fin.set_index('Date')          

# 1 Por fuente 

por_fuente 

# 2 