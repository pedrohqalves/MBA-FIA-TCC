#!/usr/bin/env python
# coding: utf-8

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
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# # ===============================
# 
# 
# # 2 . Fazendo uma análise da ABT Final
# 
# 
# # ===============================

# In[541]:


abt_final = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt_final.csv')


# In[479]:


abt_final.columns


# In[542]:


contagem_cep = abt_final.groupby('cidade').agg({'cep':'nunique'}).reset_index()


# In[543]:


contagem_cep[contagem_cep.cep >1]


# ### 116 cidades apareceram com mais de um cep, em decorrência de pequenas divergências na latitude e longitude fornecidas pelo INMET.
# 
# ### Vamos acabar perdendo alguns registros, mas vamos manter apenas os que possuem cep correto, de acordo com o nome da cidade

# ### Estratégia
# 
# ### ===============================
# 
# ### Usar outro método para validar o cep e descobrir a cidade pelo cep
# 
# ### Comparar com a cidade originalmente pega através da latitude e longitude
# 
# ### Selecionar apenas as cidades que deram correspondência 

# In[544]:


cidades = contagem_cep.cidade
aux_cep = []
aux_cidade = []
df_cidades = pd.DataFrame(columns=['cidade','cep'])
for i in cidades:
    print(i)
    
    for j in (abt_final[abt_final.cidade == i].cep.unique()):
        aux_cidade.append(i)
        aux_cep.append(j)    

        
df_cidades.cidade = aux_cidade
df_cidades.cep = aux_cep


import pycep_correios

df_cidades['cidade_validada'] = pd.Series()

for i in df_cidades.index:
    
    try:
    
        endereco = pycep_correios.consultar_cep(df_cidades.cep[i])
        df_cidades.cidade_validada[i] = endereco['cidade']
        
        
    except:
        pass


# In[545]:


df_cidades['ok'] = pd.Series()
for i in df_cidades.index:
    df_cidades.ok[i] = ((df_cidades.cidade[i] == df_cidades.cidade_validada[i]))


# In[546]:


# Tivemos 104 cidades com correspondência ok

df_cidades.groupby('ok').agg({'cidade':'nunique'})


# In[547]:


df_cidades_ok = df_cidades[df_cidades.ok == True]


# In[548]:


abt_final2 = pd.merge(abt_final,df_cidades_ok,how='inner', on = ['cidade','cep'])


# In[549]:


abt_final2.count()


# In[550]:


len(abt_final2.cidade.unique())


# ### No final temos 100 cidades onde tivemos correspondência correta.
# 
# ### A ABT apenas com as cidades corretas ficou com aprox 90mil registros

# # ===============================
# 
# 
# # 3 . Análise Exploratória
# 
# 
# # ===============================

# In[551]:


# Vamos remover as colunas que não possuem variáveis relevantes e já renomear a coluna de data

abt_final2 = abt_final2.drop(['Unnamed: 0', 'Unnamed: 0.1','Unnamed: 19','Unnamed: 0.1.1'],axis = 1)
abt_final2 = abt_final2.rename(columns={'DATA (YYYY-MM-DD)':'Data'})


# In[552]:


abt_final2.describe()


# In[553]:


abt_final2.columns


# ## Algumas variáveis tem muitos valores como -9999, que possívelmente são outliers derivados de erros de medição da estação meteorológica
# ## Vamos substituir os valores negativos por valores iguais à media a princípio

# In[554]:


abt_final3 = abt_final2


# In[555]:




for i in abt_final3.iloc[:,6:23].columns:
    print(i)
    abt_final3[i] = abt_final3[i].apply(lambda x: np.nan if x <0 else x)
    abt_final3[i] = abt_final3[i].fillna(abt_final3[i].mean())


    


# In[556]:


abt_final3.describe()


# ### Como a estratégia usada foi inserir valores vazios no lugar dos negativos e depois preencher com a média, já não temos tambem valores vazios na base. Então este ponto não será olhado a princípio 
# ### Agora que temos valores mais coerentes, vamos começar a analisar

# In[557]:


# Ainda é possível observar uma base com muitos outliers, o que não necessariamente está errado dado que temos valores 
# referentes a muitos municípios muito diferentes em termos de clima, e ao longo de anos e estações diferentes.


fig, axes = plt.subplots(6,3, sharey=False, sharex=False, figsize = (25,25))
plt.subplots_adjust(hspace = 0.5)
sns.set_context("paper", rc={"font.size":20,"axes.labelsize":20})
for ax, feature in zip(axes.flatten(), abt_final2.iloc[:,6:23].columns):
    sns.boxplot(abt_final2.iloc[:,6:23][feature], ax=ax, color = 'blue')


# In[558]:


# Analisando a temperatura ao longo dos estados

plt.figure(figsize = (20,15))
sns.set(font_scale=2)
sns.barplot(data = abt_final3, x =abt_final3['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'] , y = 'estado',  hue_order= sorted(abt_final3.estado.unique()))


# In[559]:


# Analisando a umidade relativa ao longo dos estados

plt.figure(figsize = (20,15))
sns.set(font_scale=2)
sns.barplot(data = abt_final3, y = 'estado', x = abt_final3['UMIDADE RELATIVA DO AR, HORARIA (%)'],  hue_order= sorted(abt_final3.estado.unique()))


# In[560]:


# Analisando os casos de dengue ao longo dos anos

plt.figure(figsize = (20,15))
sns.set(font_scale=2)
plt.title('Soma de Casos de Dengue por Ano')
sns.barplot(data = abt_final3, x = 'NU_ANO', y = abt_final3['NU_NOTIFIC'], estimator=sum)


# ### É possível observar uma tendência de alta até em 2016 em casos de dengue, porém queda em 2017 e novo aumento em 2019. 

# ## Vamos olhar a progressão da doença em duas cidades de grande porte (SP e RJ)

# In[561]:


# Analisando os casos de dengue em São Paulo

plt.figure(figsize = (10,10))
sns.set(font_scale=2)
plt.title('Soma de Casos na Cidade de São Paulo')

sns.lineplot(data = abt_final3[abt_final3.cidade == 'São Paulo'], x = 'NU_ANO', y = abt_final3['NU_NOTIFIC'], estimator=sum, color = 'red')


# In[ ]:


# Analisando os casos de dengue no Rio de Janeiro

plt.figure(figsize = (10,10))
sns.set(font_scale=2)
plt.title('Soma de Casos na Cidade do Rio de Janeiro')

sns.lineplot(data = abt_final3[abt_final3.cidade == 'Rio de Janeiro'], x = 'NU_ANO', y = abt_final3['NU_NOTIFIC'], estimator=sum)


# ### Interessante observar que apesar do ano do pico da dengue na base de dados foi em 2016, mas em ambas as cidades (SP e RJ) temos em 2019 um volume já quase igual ou maior ao de 2016, mostrando que nestas cidades o controle ainda não foi tão efetivo quanto no restante da base

# # ===============================
# 
# 
# #  Respondendo os objetivos do trabalho na análise exploratória
# 
# 
# # ===============================

# ## Separando as variáveis qualitativas

# In[ ]:


abt_final3.columns


# In[ ]:


# Já é possível ver que temos algumas variáveis numéricas que são usadas como qualitativas
# Já iremos transformar

abt_final3['NU_ANO'] = abt_final3['NU_ANO'].apply(lambda x: str(x))
abt_final3['ID_MUNICIP'] = abt_final3['ID_MUNICIP'].apply(lambda x: str(x))


# In[ ]:


abt_final3.dtypes


# In[ ]:


aux1 = []
aux2 = []
for i in abt_final3.columns:
    
    aux1.append(i)
    aux2.append(len(abt_final3[i].unique()))
    
freq = pd.DataFrame(columns=['Coluna','Freq'])
freq.Coluna = aux1
freq.Freq = aux2


tipo = abt_final3.dtypes.reset_index()
tipo = tipo.rename(columns={'index':'Coluna','0':'Tipo'})


# In[ ]:


freq = pd.merge(freq,tipo,how='left',on='Coluna')
freq = freq.rename(columns={0:'Tipo'})


# In[ ]:


freq_qual = freq[freq.Tipo == 'object']


# ### Tabela de Frequência das Variáveis Qualitativas

# In[ ]:


# Vamos retirar as variáveis que não possuem muito significado, e também a variável data que neste caso também não será explicativa

qualitativas = freq_qual[freq_qual.Coluna.isin(['estado','cidade','cep','ID_MUNICIP','NU_ANO','Nome_UF','Nome_Município','cidade_validada'])]


# In[ ]:


qualitativas[['Coluna','Freq']].set_index('Coluna')


# ### Medidas de Posição para as variáveis quantitativas

# In[ ]:


abt_final


# In[ ]:


quantitativas = freq[freq.Tipo != 'object']
quantitativas = list(quantitativas.Coluna)


# In[ ]:


abt_final3[quantitativas].describe()


# ### BoxPlot

# In[ ]:


# Ainda é possível observar uma base com muitos outliers, o que não necessariamente está errado dado que temos valores 
# referentes a muitos municípios muito diferentes em termos de clima, e ao longo de anos e estações diferentes.


fig, axes = plt.subplots(5,4, sharey=False, sharex=False, figsize = (30,30))
plt.subplots_adjust(hspace = 0.6,wspace=0.9)
sns.set(font_scale=1.3)
for ax, feature in zip(axes.flatten(), abt_final3[quantitativas].columns):
    sns.boxplot(abt_final3[quantitativas][feature], ax=ax, color = 'orange')


# ## ===============================
# 
# 
# # 4 . Modelagem - Estatística Tradicional
# 
# 
# # ===============================

# ### Antes de começar a modelagem, vamos criar as mesmas variáveis com dados históricos, por exemplo, temperatura média dos ultimos 7 dias, ou 30 dias. 
# 
# ### Pode ser que mais adiante estas variaveis não se provem importantes, mas sabendo que a doença leva um ciclo até se desenvolver, iremos colocar estas variáveis com o intuito de ajudar o modelo

# In[ ]:


abt_final3.columns


# In[ ]:


# Já vamos manter as variáveis que fazem sentido, tirando ID e variáveis repetidas
# A nossa variável resposta será o número de notificações de dengue

abt_final4 = abt_final3[['Data', 'lat', 'long',
       'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
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
       'VENTO, VELOCIDADE HORARIA (m/s)', 'NU_NOTIFIC']]


# In[ ]:


abt_final4.Data = abt_final4.Data.apply(lambda x: datetime.strptime(x,'%Y-%m-%d').date())


# In[ ]:


aux7 = []
aux30 = []

for i in abt_final4.iloc[:,3:-1].columns:
    nome7dias = i+ '_7dias'
    nome30dias = i+ '_30dias'
    aux7.append(nome7dias)
    aux30.append(nome30dias)
    


# In[ ]:


for i in aux7:
    abt_final4[i] = pd.Series()
for i in aux30:
    abt_final4[i] = pd.Series()


# In[ ]:


# Preenchendo as variáveis de média de 7 dias

for i in abt_final4.index:
    
    data_inicio = abt_final4.Data[i] - pd.Timedelta(7,unit='D')
    data_fim = abt_final4.Data[i]
    
    df = abt_final4[(abt_final4['Data'] >= data_inicio) & (abt_final4['Data'] <= data_fim)][(abt_final4.lat == abt_final4.lat[i]) & (abt_final4.long == abt_final4.long[i])]
    
    for j in abt_final4.iloc[:,3:20].columns:
        
        abt_final4[j+'_7dias'][i] = df[j].mean()


# In[ ]:


# Preenchendo as variáveis de média de 30 dias

for i in abt_final4.index:
    
    data_inicio = abt_final4.Data[i] - pd.Timedelta(30,unit='D')
    data_fim = abt_final4.Data[i]
    
    df = abt_final4[(abt_final4['Data'] >= data_inicio) & (abt_final4['Data'] <= data_fim)][(abt_final4.lat == abt_final4.lat[i]) & (abt_final4.long == abt_final4.long[i])]
    
    for j in abt_final4.iloc[:,3:20].columns:
        
        abt_final4[j+'_30dias'][i] = df[j].mean()


# In[2]:


abt_final4.to_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt_final4.csv')


# In[2]:


abt_final4 = pd.read_csv(r'E:\Users\quadr\Documents\MBA\Trabalhos\TCC\Dengue\Bases\Bases Tratadas//abt_final4.csv')


# In[3]:


abt_final5 = abt_final4.drop('Data',axis = 1)


# In[4]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaled_abt = pd.DataFrame(scaler.fit_transform(abt_final5), index=abt_final5.index, columns=abt_final5.columns)


# In[5]:


#Tratando caracteres especiais nos nomes de colunas


scaled_abt.columns = ["".join (c if c.isalnum() else "_" for c in str(x)) for x in scaled_abt.columns]



import re
scaled_abt = scaled_abt.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))


# In[6]:


x = scaled_abt.drop(['NU_NOTIFIC'], axis =1)
y = scaled_abt.NU_NOTIFIC


# ##  Começando a Modelagem

# In[7]:


from sklearn.metrics import mean_absolute_error as mae,mean_squared_error as mse
from sklearn.model_selection import train_test_split


# In[8]:


x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.3, random_state = 42)


# ## Regressão Linear

# In[9]:


from sklearn.linear_model import LinearRegression

lr = LinearRegression()

lr_model = lr.fit(x_train, y_train)
lr_pred = lr_model.predict(x_test)
lr_pred_train = lr_model.predict(x_train)


# Verificando a performance do modelo

print('treino')
print('O Score do Modelo na base de treino é : ',lr_model.score(x_train,y_train))
print('O MAE do Modelo  é : ', mae(y_train,lr_pred_train))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_train,lr_pred_train)))



print('O Score do Modelo de Regressão Linear na base de teste é : ', lr.score(x_test,y_test))
print('O MAE do Modelo de Regressão Linear é : ', mae(y_test,lr_pred))
print('O MSRE do Modelo de Regressão Linear é : ', np.sqrt(mse(y_test,lr_pred)))


# ## Árvore de Decisão

# In[10]:


from sklearn.tree import DecisionTreeRegressor

tree = DecisionTreeRegressor(random_state=42)
tree_model = tree.fit(x_train,y_train)
tree_pred = tree_model.predict(x_test)
tree_pred_train = tree_model.predict(x_train)


# Verificando a performance do modelo

print('treino')
print('O Score do Modelo na base de treino é : ',tree_model.score(x_train,y_train))
print('O MAE do Modelo  é : ', mae(y_train,tree_pred_train))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_train,tree_pred_train)))

print('O Score do Modelo de Árvore de Decisão na base de teste é : ',tree_model.score(x_test,y_test))
print('O MAE do Modelo de Árvore de Decisão é : ', mae(y_test,tree_pred))
print('O MSRE do Modelo de Árvore de Decisão é : ', np.sqrt(mse(y_test,tree_pred)))


# In[11]:


abt_final5.NU_NOTIFIC.describe()


# ## ===============================
# 
# 
# # 5 . Modelagem - Inteligência Artificial
# 
# 
# # ===============================

# ### Ainda sem realizar nenhum tipo de tratamento adicional, vamos aplicar alguns modelos de inteligência artificial, para comparar o resultado e definir quais os modelos seguiriam para uma etapa de otimização

# ## Random Forest

# In[25]:


from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(random_state=42)
rf_model = rf.fit(x_train,y_train)
rf_pred_train = rf.predict(x_train)
rf_pred = rf_model.predict(x_test)


# Verificando a performance do modelo

print('treino')
print('O Score do Modelo na base de treino é : ',rf_model.score(x_train,y_train))
print('O MAE do Modelo  é : ', mae(y_train,rf_pred_train))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_train,rf_pred_train)))

print('teste')
print('O Score do Modelo  na base de teste é : ',rf_model.score(x_test,y_test))
print('O MAE do Modelo  é : ', mae(y_test,rf_pred))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_test,rf_pred)))


# ## XGBoost

# In[11]:


from xgboost import XGBRegressor

xgb = XGBRegressor(random_state=42)
xgb_model = xgb.fit(x_train,y_train)
xgb_pred = xgb.predict(x_test)
xgb_pred_train = xgb.predict(x_train)


# Verificando a performance do modelo

print('treino')
print('O Score do Modelo na base de treino é : ',xgb_model.score(x_train,y_train))
print('O MAE do Modelo  é : ', mae(y_train,xgb_pred_train))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_train,xgb_pred_train)))

print('teste')
print('O Score do Modelo  na base de teste é : ',xgb_model.score(x_test,y_test))
print('O MAE do Modelo  é : ', mae(y_test,xgb_pred))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_test,xgb_pred)))


# ## LGBM

# In[19]:


from lightgbm import LGBMRegressor

lgbm = LGBMRegressor(random_state=42)
lgbm_model = lgbm.fit(x_train,y_train)
lgbm_pred = lgbm_model.predict(x_test)
lgbm_pred_train = lgbm_model.predict(x_train)


# Verificando a performance do modelo

print('treino')
print('O Score do Modelo na base de treino é : ',lgbm_model.score(x_train,y_train))
print('O MAE do Modelo  é : ', mae(y_train,lgbm_pred_train))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_train,lgbm_pred_train)))

print('teste')
print('O Score do Modelo  na base de teste é : ',lgbm_model.score(x_test,y_test))
print('O MAE do Modelo  é : ', mae(y_test,lgbm_pred))
print('O MSRE do Modelo  é : ', np.sqrt(mse(y_test,lgbm_pred)))


# ## ===============================
# 
# 
# # 6 . Otimização dos Modelos
# 
# 
# # ===============================

# ### Os modelos com melhor desempenho foram o Random Forest e o LightGBM
# 

# ### Começando com o Cross Validation

# In[16]:


rf_model.get_params


# In[22]:


lgbm_model.get_params


# In[23]:


# Primeiro para o Random Forest

inicio = time.time()

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


rf = RandomForestRegressor(random_state=42)
rf_model = rf.fit(x_train,y_train)
rf_pred = rf.predict(x_test)

parameters = {'max_depth':[30,50,100], 'criterion':['mse'], 'n_estimators':[50,100,150]}


grid_rf = GridSearchCV(estimator= rf, param_grid=parameters ,verbose=1)
grid_rf_model = grid_rf.fit(x_train,y_train)
grid_rf_pred = grid_rf_model.predict(x_test)
grid_rf_pred_train = grid_rf_model.predict(x_train)




# Verificando a performance do modelo


print('treino')
print('O Score do Modelo com Cross Validation é : ',grid_rf_model.score(x_train,y_train))
print('O MAE do com Cross Validation é : ', mae(y_train,grid_rf_pred_train))
print('O MSRE do Modelo com Cross Validation  é : ', np.sqrt(mse(y_train,grid_rf_pred_train)))


print('teste')
print('O Score do Modelo com Cross Validation é : ',grid_rf_model.score(x_test,y_test))
print('O MAE do com Cross Validation é : ', mae(y_test,grid_rf_pred))
print('O MSRE do Modelo com Cross Validation  é : ', np.sqrt(mse(y_test,grid_rf_pred)))



grid_rf_model.get_params

fim = time.time()

print('Tempo Gasto = ', (fim - inicio))


# In[24]:


# Para o LGBM

inicio = time.time()

from lightgbm import LGBMRegressor
from sklearn.model_selection import GridSearchCV


lgbm = LGBMRegressor(random_state=42)
lgbm_model = lgbm.fit(x_train,y_train)
lgbm_pred = lgbm_model.predict(x_test)


parameters = {'max_depth':[30,50,100],'boosting_type':['gbdt','dart','goss'] ,'n_estimators':[50,100,150]}


grid_lgbm = GridSearchCV(estimator= lgbm, param_grid=parameters ,verbose=1)
grid_lgbm_model = grid_lgbm.fit(x_train,y_train)
grid_lgbm_pred = grid_lgbm_model.predict(x_test)
grid_lgbm_pred_train = grid_lgbm_model.predict(x_train)




# Verificando a performance do modelo

print('treino')
print('O Score do Modelo com Cross Validation é : ',grid_lgbm_model.score(x_train,y_train))
print('O MAE do com Cross Validation é : ', mae(y_train,grid_lgbm_pred_train))
print('O MSRE do Modelo com Cross Validation  é : ', np.sqrt(mse(y_train,grid_lgbm_pred_train)))


print('teste')
print('O Score do Modelo com Cross Validation é : ',grid_lgbm_model.score(x_test,y_test))
print('O MAE do com Cross Validation é : ', mae(y_test,grid_lgbm_pred))
print('O MSRE do Modelo com Cross Validation  é : ', np.sqrt(mse(y_test,grid_lgbm_pred)))

grid_lgbm_model.get_params

fim = time.time()

print('Tempo Gasto = ', (fim - inicio))


# ## Fazendo feature selection

# In[22]:


from sklearn.feature_selection import SelectPercentile, f_regression

for i in range(2,12,2):
    
    print(str(i*10)+'%')
    print('-------------')
    x_new = SelectPercentile(f_regression,percentile=i*10).fit_transform(x,y)
    
    x_train,x_test,y_train,y_test = train_test_split(x_new,y,test_size = 0.3, random_state = 42)
    
    from lightgbm import LGBMRegressor

    lgbm = LGBMRegressor(random_state=42)
    lgbm_model = lgbm.fit(x_train,y_train)
    lgbm_pred = lgbm_model.predict(x_test)
    lgbm_pred_train = lgbm_model.predict(x_train)


    # Verificando a performance do modelo

    print('treino')
    print('O Score do Modelo na base de treino é : ',lgbm_model.score(x_train,y_train))
    print('O MAE do Modelo  é : ', mae(y_train,lgbm_pred_train))
    print('O MSRE do Modelo  é : ', np.sqrt(mse(y_train,lgbm_pred_train)))

    print('teste')
    print('O Score do Modelo  na base de teste é : ',lgbm_model.score(x_test,y_test))
    print('O MAE do Modelo  é : ', mae(y_test,lgbm_pred))
    print('O MSRE do Modelo  é : ', np.sqrt(mse(y_test,lgbm_pred))) 
    
    print('-----------')


# ### Não tivemos mudanças positivas com número de features menor, manteremos 100%
