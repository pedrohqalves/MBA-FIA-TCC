#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install geopy')


# # ===============================
# 
# 
# # 1 . Importando as bibliotecas básicas
# 
# 
# # ===============================

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time


# # ==============================
# 
# 
# # 2. Lendo as bases de dados
# 
# 
# # ==============================

# ### Primeiro lendo as bases de Clima
# 
# ### No caso destas bases, temos o nome da estação, que pode ou não ser o mesmo nome da cidade que ela está localizada. Para facilitar posteriormente cruzarmos cidade a cidade com os casos de dengue, vamos usar os dados de latitude e longitude para descobrir a cidade onde está localizada a estação
# 
# ### Vamos acrescentar uma coluna em cada base de cada estação mostrando cidade, estado e cep (que pode facilitar depois a localização também)

# ## ----------------------------------------------
# 
# 
# ### Para cada base vamos ler o cabeçalho, retirar os dados de localização, acrescentar como colunas na base, e guardar os dados para serem empilhados com os da próxima base, e assim por diante

# In[3]:


#Primeiro pegando uma lista com todos os arquivos na pasta onde estão os dados

dadosclima = []

import sys

root = r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima\Bases Anuais'
      
            
for root, dirs, files in os.walk(root):
     for file in files:
        dadosclima.append(os.path.join(root, file))


# In[ ]:


# Como a base de dados ficou muito grande, este comando e o seguinte devem ser rodados separadamente
# com limpeza de memória entre eles

#Importa a lib para descobrir localização através de coordenadas

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='teste_dengue')

clima = pd.DataFrame()


for i in dadosclima:
    if dadosclima.index(i) < 1000:
        
        
        
        print('Faltam ' + str(len(dadosclima) - dadosclima.index(i) +1) +' itens na lista' )
        print('Inicio Item ' + str(dadosclima.index(i)))
        inicio = time.time()
        base1 = pd.read_csv(i, delimiter = ';',engine = 'python', nrows = 3)
        base2 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 3, nrows = 4)
        estado = base1.iloc[0,1]
        estacao = base1.iloc[1,1]
        lat = str(base2.iloc[0,1]).replace(',','.')
        long = str(base2.iloc[1,1]).replace(',','.')
        
        # Tratando casos onde temos latitude que começa apenas com . ou , (positivos e negativos)
        
        if lat[0] == '.':
            lat = str(0)+lat
        elif lat[0] == '-':
            lat = '-' + str(0) + lat[1:]
        else:
            pass
        if long[0] == '.':
            long = str(0)+long
        elif long[0] == '-':
            long = '-'+ str(0) + long [1:]                
        else: 
            pass
        
        # Passa as coordenadas 
        
        location = geolocator.reverse(lat +', ' + long)
        
        
        try:
            cidade = location.raw['address']['city'] 

        except:
            cidade = 'Erro'
            
        try:
            cep = location.raw['address']['postcode'] 
        except:
            cep = 'Erro'
        
        # Pega o restante da base, e adiciona colunas com os valores que descobrimos anteriormente
        
        base3 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 8)
        base3['estacao'] = estacao
        base3['estado'] = estado
        base3['cidade'] = pd.Series()
        base3['cep'] = pd.Series()
        base3['lat'] = lat
        base3['long'] = long
        
        
        try:
            base3['cidade'] = cidade

        except:
            pass
        
        try:
            base3['cep'] = cep
        except:
            pass
        
        
        
        clima = clima.append(base3)
        fim = time.time()
        tempo = fim - inicio

        print('Fim Item ' + str(dadosclima.index(i)))
        print('Duração : ' + str(tempo) + ' segundos')
        

    else:
        pass
    


clima.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part1.csv')
del clima


# In[ ]:


# Como a base de dados ficou muito grande, este comando e o seguinte devem ser rodados separadamente
# com limpeza de memória entre eles

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='teste_dengue')

clima = pd.DataFrame()


for i in dadosclima:
    if 1000 <= dadosclima.index(i) < 2000:
        
 
        
        print('Faltam ' + str(len(dadosclima) - dadosclima.index(i) +1) +' itens na lista' )
        print('Inicio Item ' + str(dadosclima.index(i)))
        inicio = time.time()
        base1 = pd.read_csv(i, delimiter = ';',engine = 'python', nrows = 3)
        base2 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 3, nrows = 4)
        estado = base1.iloc[0,1]
        estacao = base1.iloc[1,1]
        lat = str(base2.iloc[0,1]).replace(',','.')
        long = str(base2.iloc[1,1]).replace(',','.')
        
        # Tratando casos onde temos latitude que começa apenas com . ou , (positivos e negativos)
        
        if lat[0] == '.':
            lat = str(0)+lat
        elif lat[0] == '-':
            lat = '-' + str(0) + lat[1:]
        else:
            pass
        if long[0] == '.':
            long = str(0)+long
        elif long[0] == '-':
            long = '-'+ str(0) + long [1:]                
        else: 
            pass
        
        # Passa as coordenadas 
        
        location = geolocator.reverse(lat +', ' + long)
        
         
        try:
            cidade = location.raw['address']['city'] 

        except:
            cidade = 'Erro'
            
        try:
            cep = location.raw['address']['postcode'] 
        except:
            cep = 'Erro'
        
        
        # Pega o restante da base, e adiciona colunas com os valores que descobrimos anteriormente
        
        base3 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 8)
        base3['estacao'] = estacao
        base3['estado'] = estado
        base3['cidade'] = pd.Series()
        base3['cep'] = pd.Series()
        base3['lat'] = lat
        base3['long'] = long
        
        
        try:
            base3['cidade'] = cidade

        except:
            pass
        
        try:
            base3['cep'] = cep
        except:
            pass
        
        
        
        clima = clima.append(base3)
        fim = time.time()
        tempo = fim - inicio

        print('Fim Item ' + str(dadosclima.index(i)))
        print('Duração : ' + str(tempo) + ' segundos')
        

    else:
        pass

    
clima.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part2.csv')
del clima


# In[4]:


# Como a base de dados ficou muito grande, este comando e o seguinte devem ser rodados separadamente
# com limpeza de memória entre eles

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='teste_dengue')

clima = pd.DataFrame()


for i in dadosclima:
    if 2000 <=dadosclima.index(i) < 3000:
        
 
        
        print('Faltam ' + str(len(dadosclima) - dadosclima.index(i) +1) +' itens na lista' )
        print('Inicio Item ' + str(dadosclima.index(i)))
        inicio = time.time()
        base1 = pd.read_csv(i, delimiter = ';',engine = 'python', nrows = 3)
        base2 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 3, nrows = 4)
        estado = base1.iloc[0,1]
        estacao = base1.iloc[1,1]
        lat = str(base2.iloc[0,1]).replace(',','.')
        long = str(base2.iloc[1,1]).replace(',','.')
        
        # Tratando casos onde temos latitude que começa apenas com . ou , (positivos e negativos)
        
        if lat[0] == '.':
            lat = str(0)+lat
        elif lat[0] == '-':
            lat = '-' + str(0) + lat[1:]
        else:
            pass
        if long[0] == '.':
            long = str(0)+long
        elif long[0] == '-':
            long = '-'+ str(0) + long [1:]                
        else: 
            pass
        
        # Passa as coordenadas 
        
        location = geolocator.reverse(lat +', ' + long)
        
        
        try:
            cidade = location.raw['address']['city'] 

        except:
            cidade = 'Erro'
            
        try:
            cep = location.raw['address']['postcode'] 
        except:
            cep = 'Erro'
        
        # Pega o restante da base, e adiciona colunas com os valores que descobrimos anteriormente
        
        base3 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 8)
        base3['estacao'] = estacao
        base3['estado'] = estado
        base3['cidade'] = pd.Series()
        base3['cep'] = pd.Series()
        base3['lat'] = lat
        base3['long'] = long
        
        
        try:
            base3['cidade'] = cidade

        except:
            pass
        
        try:
            base3['cep'] = cep
        except:
            pass
        
        
        
        
        clima = clima.append(base3)
        fim = time.time()
        tempo = fim - inicio

        print('Fim Item ' + str(dadosclima.index(i)))
        print('Duração : ' + str(tempo) + ' segundos')
        

    else:
        pass

    
clima.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part3.csv')
del clima


# In[ ]:


# Como a base de dados ficou muito grande, este comando e o seguinte devem ser rodados separadamente
# com limpeza de memória entre eles

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='teste_dengue')

clima = pd.DataFrame()


for i in dadosclima:
    if dadosclima.index(i) >= 3000:
        
 
        
        print('Faltam ' + str(len(dadosclima) - dadosclima.index(i) +1) +' itens na lista' )
        print('Inicio Item ' + str(dadosclima.index(i)))
        inicio = time.time()
        base1 = pd.read_csv(i, delimiter = ';',engine = 'python', nrows = 3)
        base2 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 3, nrows = 4)
        estado = base1.iloc[0,1]
        estacao = base1.iloc[1,1]
        lat = str(base2.iloc[0,1]).replace(',','.')
        long = str(base2.iloc[1,1]).replace(',','.')
        
        # Tratando casos onde temos latitude que começa apenas com . ou , (positivos e negativos)
        
        if lat[0] == '.':
            lat = str(0)+lat
        elif lat[0] == '-':
            lat = '-' + str(0) + lat[1:]
        else:
            pass
        if long[0] == '.':
            long = str(0)+long
        elif long[0] == '-':
            long = '-'+ str(0) + long [1:]                
        else: 
            pass
        
        # Passa as coordenadas 
        
        location = geolocator.reverse(lat +', ' + long)
        
        
         
        try:
            cidade = location.raw['address']['city'] 

        except:
            cidade = 'Erro'
            
        try:
            cep = location.raw['address']['postcode'] 
        except:
            cep = 'Erro'
        
        
        # Pega o restante da base, e adiciona colunas com os valores que descobrimos anteriormente
        
        base3 = pd.read_csv(i, delimiter = ';',engine = 'python', skiprows = 8)
        base3['estacao'] = estacao
        base3['estado'] = estado
        base3['cidade'] = pd.Series()
        base3['cep'] = pd.Series()
        base3['lat'] = lat
        base3['long'] = long
        
        
        try:
            base3['cidade'] = cidade

        except:
            pass
        
        try:
            base3['cep'] = cep
        except:
            pass
        
        
        
        clima = clima.append(base3)
        fim = time.time()
        tempo = fim - inicio

        print('Fim Item ' + str(dadosclima.index(i)))
        print('Duração : ' + str(tempo) + ' segundos')
        

    else:
        pass
    
clima.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part4.csv')
del clima


# ### Carregando agora a base de casos de dengue
# ### Vamos seguir a estratégia: Com os dados de Dengue, tentar cruzar os dados com as bases de clima individualmente, para evitar de termos que consolidar uma base completa de clima que ficaria muito grande em memória.
# 
# ### As cidades e Estados onde não conseguirmos dados de dengue x clima, iremos retirar da análise e assim faremos o filtro para tentar reduzir um pouco os dados possibilitando uso da memória para consolidar uma abt

# In[ ]:


#Primeiro pegando uma lista com todos os arquivos na pasta onde estão os dados

dadosdengue = []

import sys

root = r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Casos Dengue\DadosAnuaisCSV'
      
            
for root, dirs, files in os.walk(root):
     for file in files:
        dadosdengue.append(os.path.join(root, file))


# In[ ]:


#Casos de Dengue

#Criando um DataFrame

dengue = pd.DataFrame()


for i in dadosdengue:
    print(i)
    inicio = time.time()
    base1 = pd.read_csv(i, engine = 'python')
    dengue = dengue.append(base1, sort = False)
    fim = time.time()
    duracao = fim - inicio
    print(duracao)
    
dengue.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Casos Dengue//dengue.csv')


# In[ ]:


dengue = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Casos Dengue//dengue.csv')


# In[ ]:


notific_dengue = dengue[['DT_NOTIFIC','ID_MUNICIP','NU_ANO','NU_NOTIFIC']].groupby(['DT_NOTIFIC','NU_ANO','ID_MUNICIP']).agg('count').reset_index()


# In[ ]:


# Vamos usar o campo ID_MUNICIP posteriormente para fazer um join e descobrir o nome da cidade.
# Vamos transformar o campo em string para não termos problemas no join

notific_dengue['ID_MUNICIP'] = notific_dengue.ID_MUNICIP.apply(lambda x: str(x))


# In[ ]:


notific_dengue.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Casos Dengue//notific_dengue.csv')


# In[ ]:


del dengue


# ### Lendo agora a base de cidades
# ### Usaremos a base de cidades para identificar as cidades onde tivemos casos de dengue, para depois cruzar através da cidade os casos com os dados de clima

# In[ ]:


cidades = pd.read_excel(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Cidades//RELATORIO_DTB_BRASIL_DISTRITO.xls')


# In[ ]:


# Em uma das bases temos o código do município com 7 dígitos e em outra com 6, vamos igualar

cidades['ID_MUNICIP'] = cidades['Código Município Completo'].apply(lambda x: str(x)[:-1])


# In[ ]:


dengue_cidades = pd.merge(notific_dengue,cidades,how='inner',on='ID_MUNICIP')


# In[ ]:


# Deletando as bases anteriores para liberar memória

del cidades


# In[ ]:


dengue_cidades.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Casos Dengue//denguecidades.csv')


# # -------------------------------------------------
# 
# # 3 . Tratando a base inicial de dados
# 
# # --------------------------------------------------
# 
# 
# 
# 
# ### Temos todas as bases de dados que precisamos agora. Precisamos agregar e fazer join para começar a atacar o problema.
# 
# ### Temos a base de clima com dados de hora em hora de todas as estações de medição espalhadas pelo Brasil
# ### Temos a base de número de notificações de dengue em cada cidade
# 
# ### Para cruzar estas duas bases a chave será o nome da cidade e data
# 
# ### A estratégia será verificar quantos cruzamentos temos de dados de clima x dengue para começar a análise

# In[11]:


dengue_cidades = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Casos Dengue//denguecidades.csv')


# In[12]:


dengue_cidades = dengue_cidades[['DT_NOTIFIC','ID_MUNICIP','NU_ANO','Nome_UF','Nome_Município','NU_NOTIFIC']]
dengue_cidades = dengue_cidades.drop_duplicates(subset = ['DT_NOTIFIC','ID_MUNICIP'])


# In[13]:


states = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

states = {v: k for k, v in states.items()}


# In[14]:


dengue_cidades['UF'] = dengue_cidades['Nome_UF'].map(states)


# ### Começando com as bases de clima

# In[ ]:


# Tratando os dados das bases.
# Começando pelo clima 1

clima1 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part1.csv')


# In[ ]:


# Como temos colunas com tipos diferentes de dados, vamos detectar o que está com tipos diferentes para poder tratar

for i in clima1.columns:
    print(clima1[i].apply(type).value_counts())


# In[ ]:


# Temos muitos dados sendo lidos como string, provavelmente por conta da virgula em campos numericos. 
# Vamos começar ajustando esse ponto
# Esta parte vai transformar colunas que são inteiras string para valores numéricos



for i in clima1.iloc[:,3:20].columns:
    
    
    print(i)
    clima1[i] = [float(x.replace(',','.')) if isinstance(x, str) else float(x) for x in clima1[i]]

    
# cidade e cep precisamos transformar para string

clima1.cidade = clima1.cidade.apply(lambda x: str(x))
clima1.cep = clima1.cep.apply(lambda x: str(x))


# for i in clima1.iloc[:,3:20].columns:
#     print(i)
#     print(type(clima1[i][0]))
#     if isinstance(clima1[i][0], str) == True:        
#         clima1[i] = clima1[i].apply(lambda x: float(x.replace(',','.')))
#         print(type(clima1[i][0]))
#     else: 
#         pass


# In[ ]:


# Vamos verificar se o tratamento foi efetivo

for i in clima1.columns:
    print(clima1[i].apply(type).value_counts())


# In[ ]:


# Agora que todos os valores estão devidamente tratados, vamos reduzir a base para facilitar o trabalho em memória
# Vamos reduzir a base a valores diários e não mais horários.

# Como o efeito da dengue será visto em dias, não há necessidade a princípio de termos dados de clima de hora em hora
# A tentativa será feita em cima de médias diárias


clima1_reduzida = clima1.groupby(['DATA (YYYY-MM-DD)','estado','cidade','cep','lat','long']).agg('mean').reset_index()
abt1 = pd.merge(clima1_reduzida,dengue_cidades, how = 'inner', left_on = ['DATA (YYYY-MM-DD)','estado','cidade'], right_on = ['DT_NOTIFIC','UF','Nome_Município'])


# In[ ]:


abt1.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt1.csv')


# In[ ]:


del clima1
del clima1_reduzida
del abt1


# ### Vamos executar a mesma estratégia para as bases de clima 2, 3 e 4

# ### Clima 2

# In[ ]:


# Tratando a base clima 2

clima2 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part2.csv')


# In[ ]:


# Como temos colunas com tipos diferentes de dados, vamos detectar o que está com tipos diferentes para poder tratar

for i in clima2.columns:
    print(clima2[i].apply(type).value_counts())


# In[ ]:



for i in clima2.iloc[:,3:20].columns:
    
    
    print(i)
    clima2[i] = [float(x.replace(',','.')) if isinstance(x, str) else float(x) for x in clima2[i]]
    
    
    
#     print(i)
#     print(type(clima2[i][0]))
#     if isinstance(clima2[i][0], str) == True:        
#         clima2[i] = clima2[i].apply(lambda x: float(x.replace(',','.')))
#         print(type(clima2[i][0]))
#     else: 
#         pass


# In[ ]:


# cidade e cep precisamos transformar para string

clima2.cidade = clima2.cidade.apply(lambda x: str(x))
clima2.cep = clima2.cep.apply(lambda x: str(x))


# In[ ]:


# Chegando se o tratamento foi efetivo

for i in clima2.columns:
    print(clima2[i].apply(type).value_counts())


# In[ ]:


# Agora que todos os valores estão devidamente tratados, vamos reduzir a base para facilitar o trabalho em memória
# Vamos reduzir a base a valores diários e não mais horários.

# Como o efeito da dengue será visto em dias, não há necessidade a princípio de termos dados de clima de hora em hora
# A tentativa será feita em cima de médias diárias


clima2_reduzida = clima2.groupby(['DATA (YYYY-MM-DD)','estado','cidade','cep','lat','long']).agg('mean').reset_index()
abt2 = pd.merge(clima2_reduzida,dengue_cidades, how = 'inner', left_on = ['DATA (YYYY-MM-DD)','estado','cidade'], right_on = ['DT_NOTIFIC','UF','Nome_Município'])


# In[ ]:


abt2.count()


# In[ ]:


abt2.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt2.csv')


# In[ ]:


del clima2
del clima2_reduzida
del abt2


# ### Clima 3

# In[5]:


# Agora para a base clima 3
# A partir da base clima 3, o INMET adiciona uma outra coluna de data diferente. No meio da base temos essa mudança no schema
# Teremos que tratar isso transformando tudo em uma coluna unica de data 

clima3 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part3.csv')


# In[6]:


clima3.Data = clima3.Data.apply(lambda x: str(x))

clima3_part1 = clima3[clima3['DATA (YYYY-MM-DD)'].notnull()]
clima3_part2 = clima3[clima3['DATA (YYYY-MM-DD)'].isnull()]


# In[7]:


# Tratando a coluna de Data

def ajuste_data(x : str):    
    return(x[:4]+'-'+x[5:7]+'-'+x[8:10])

# --------------------------------------------------

    
clima3_part2['DATA (YYYY-MM-DD)'] = clima3_part2.Data.apply(lambda x: ajuste_data(x))

clima3 = pd.concat([clima3_part1,clima3_part2], sort= False)


# In[8]:


clima3 = clima3.drop('Data', axis = 1)
clima3 = clima3.drop('Hora UTC', axis = 1)

del clima3_part1
del clima3_part2


# In[9]:


for i in clima3.iloc[:,3:21].columns:
    
    
    print(i)
    clima3[i] = [float(x.replace(',','.')) if isinstance(x, str) else float(x) for x in clima3[i]]
    
    
# cidade e cep precisamos transformar para string

clima3.cidade = clima3.cidade.apply(lambda x: str(x))
clima3.cep = clima3.cep.apply(lambda x: str(x))
    


# In[ ]:


# Chegando se o tratamento foi efetivo

for i in clima3.columns:
    print(clima3[i].apply(type).value_counts())


# In[15]:


# Agora que todos os valores estão devidamente tratados, vamos reduzir a base para facilitar o trabalho em memória
# Vamos reduzir a base a valores diários e não mais horários.

# Como o efeito da dengue será visto em dias, não há necessidade a princípio de termos dados de clima de hora em hora
# A tentativa será feita em cima de médias diárias


clima3_reduzida = clima3.groupby(['DATA (YYYY-MM-DD)','estado','cidade','cep','lat','long']).agg('mean').reset_index()
abt3 = pd.merge(clima3_reduzida,dengue_cidades, how = 'inner', left_on = ['DATA (YYYY-MM-DD)','estado','cidade'], right_on = ['DT_NOTIFIC','UF','Nome_Município'])


# In[16]:


abt3.count()


# In[17]:


abt3.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt3.csv')


# In[18]:


del clima3
del clima3_reduzida
del abt3


# ### Clima 4

# In[ ]:


# Agora para a base clima 4

clima4 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Clima//clima_part4.csv')


# In[ ]:


# Tratando a coluna de Data

def ajuste_data(x : str):    
    return(x[:4]+'-'+x[5:7]+'-'+x[8:10])

# --------------------------------------------------

    
clima4.Data = clima4.Data.apply(lambda x: ajuste_data(x))
clima4 = clima4.rename(columns={'Data': 'DATA (YYYY-MM-DD)'})


# In[ ]:


for i in clima4.iloc[:,3:21].columns:
    
    
    print(i)
    clima4[i] = [float(x.replace(',','.')) if isinstance(x, str) else float(x) for x in clima4[i]]
    
    
# cidade e cep precisamos transformar para string

clima4.cidade = clima4.cidade.apply(lambda x: str(x))
clima4.cep = clima4.cep.apply(lambda x: str(x))
    


# In[ ]:


# Chegando se o tratamento foi efetivo

for i in clima4.columns:
    print(clima4[i].apply(type).value_counts())


# In[ ]:


# Agora que todos os valores estão devidamente tratados, vamos reduzir a base para facilitar o trabalho em memória
# Vamos reduzir a base a valores diários e não mais horários.

# Como o efeito da dengue será visto em dias, não há necessidade a princípio de termos dados de clima de hora em hora
# A tentativa será feita em cima de médias diárias


clima4_reduzida = clima4.groupby(['DATA (YYYY-MM-DD)','estado','cidade','cep','lat','long']).agg('mean').reset_index()
abt4 = pd.merge(clima4_reduzida,dengue_cidades, how = 'inner', left_on = ['DATA (YYYY-MM-DD)','estado','cidade'], right_on = ['DT_NOTIFIC','UF','Nome_Município'])


# In[ ]:


abt4.count()


# In[ ]:


abt4.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt4.csv')


# # -----------------------------------------------------------

# ### Finalizando a ABT empilhando os dados
# 
# ### Até então o que poderíamos tirar de informação das bases foi retirado. O Refinamento da informação será feito no próximo notebook antes da análise exploratória

# In[19]:


abt1 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt1.csv')
abt2 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt2.csv')
abt3 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt3.csv')
abt4 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt4.csv')


# In[ ]:


abt1.columns


# In[ ]:


abt2.columns


# In[ ]:


abt3.columns


# In[ ]:


abt4.columns


# In[20]:


abt_final = pd.concat([abt1,abt2], sort=False)


# In[21]:


abt3 = abt3[['Unnamed: 0', 'DATA (YYYY-MM-DD)', 'estado', 'cidade', 'cep', 'lat',
       'long', 'Unnamed: 0.1', 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
       'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
       'PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)',
       'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)',
       'RADIACAO GLOBAL (W/m²)',
       'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
       'TEMPERATURA DO PONTO DE ORVALHO (°C)',
       'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
       'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
       'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)',
       'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)',
       'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)',
       'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)',
       'UMIDADE RELATIVA DO AR, HORARIA (%)',
       'VENTO, DIREÇÃO HORARIA (gr) (° (gr))', 'VENTO, RAJADA MAXIMA (m/s)',
       'VENTO, VELOCIDADE HORARIA (m/s)', 'Unnamed: 19', 'DT_NOTIFIC',
       'ID_MUNICIP', 'NU_ANO', 'Nome_UF', 'Nome_Município', 'NU_NOTIFIC']]


# In[22]:


abt4 = abt4[['Unnamed: 0', 'DATA (YYYY-MM-DD)', 'estado', 'cidade', 'cep', 'lat',
       'long', 'Unnamed: 0.1', 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
       'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
       'PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)',
       'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)',
       'RADIACAO GLOBAL (W/m²)',
       'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
       'TEMPERATURA DO PONTO DE ORVALHO (°C)',
       'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
       'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
       'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)',
       'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)',
       'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)',
       'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)',
       'UMIDADE RELATIVA DO AR, HORARIA (%)',
       'VENTO, DIREÇÃO HORARIA (gr) (° (gr))', 'VENTO, RAJADA MAXIMA (m/s)',
       'VENTO, VELOCIDADE HORARIA (m/s)', 'Unnamed: 19', 'DT_NOTIFIC',
       'ID_MUNICIP', 'NU_ANO', 'Nome_UF', 'Nome_Município', 'NU_NOTIFIC']]


# In[23]:


abt_final = pd.concat([abt_final,abt3,abt4], sort = False)


# In[24]:


abt_final.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt_final.csv')


# In[ ]:




