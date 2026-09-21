# ETAPA 1 - IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
"""
serão utilizadas 3 bibliotecas:
pandas para que possa mos abrir e ler os dataframes/datasets
função Path dentro da biblioteca pathlib para que possamos localizar o dataset
matplotlib.pyplot afim de plotar nossas séries temporais
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ETAPA 2 - LOCALIZAÇÃO E ABERTURA DO DATASET

caminho = Path(__file__).resolve() #localizar esse codigo dentro dos arquivos do PC
raiz = caminho.parent.parent #encontrar a pasta raiz
planilha = raiz / 'Planilha' / 'reactor_sample_5k.csv' #a partir da raiz encontrar o dataset 

df = pd.read_csv(planilha) #leitura do dataset pela biblioteca pandas
print(f"Dataset carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")

# ETAPA 3 - DIAGNOSTICO DOS DADOS FALTANTES

print("NaNs por coluna:")
print(df.isnull().sum())
print(f"\n% missing por coluna:")
print((df.isnull().mean() * 100).round(2))
print(f"\nTotal de NaNs: {df.isnull().sum().sum()}")

"""
essas linhas de codigo foram meramente para poder ter acesso a
algumas informações como nome de variaveis e etc

linhas = df.head()
print(linhas)

info = df.info()
print(info)

Est_desc = df.describe()
print(Est_desc)
"""

# ETAPA 4 - PLOT DA SÉRIE NÃO TRATADA

plt.figure(figsize=(12, 4))
plt.plot(df.index, df['Reactor_Temp_C'], 'r-', alpha=0.6, linewidth=0.8)
plt.xlabel('Tempo')
plt.ylabel('Temperatura da água')
plt.title('Temperatura da água — Dados Brutos (com anomalias)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""
aqui, nesse grafico podemos ver a presença de
diversos outliers dentro da coletania de dados
"""

# ETAPA 5 - PREENCHIMENTO DOS DADOS FALTANTES COM O DADO VALIDO ANTERIOR
"""
particularmente, eu vejo mais sentido em tomar um valor médio entre o ultimo valor valido
e o valor valido imediatamente posterior ao dado faltante.
exemplo:

5, 5, 6 , --- , 8
se for preencher com o dado valido anterior fica:
5, 5, 6, 6 ,8
acho mais condizente tomar:
5, 5, 6, 7, 8
"""

# Série temporal → forward fill (propaga o último valor válido)
df_ffill = df.ffill()
print(f"NaNs após ffill: {df_ffill.isnull().sum().sum()}")

# ETAPA 6 - DETERMINAÇÃO DOS OUTLIERS

Q1 = df_ffill['Reactor_Temp_C'].quantile(0.25)
Q3 = df_ffill['Reactor_Temp_C'].quantile(0.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR
outliers = (df_ffill['Reactor_Temp_C'] < lim_inf) | (df_ffill['Reactor_Temp_C'] > lim_sup)
print(f"Outliers detectados: {outliers.sum()} ({outliers.mean()*100:.1f}%)")
print(f"Limites: [{lim_inf:.1f}, {lim_sup:.1f}] °C")

# ETAPA 7 - SUBSTITUIÇÃO DOS OUTLIERS POR UMA MÉDIANA

mediana = df_ffill['Reactor_Temp_C'].median()
df_ffill.loc[outliers, 'Reactor_Temp_C'] = mediana
print(f"Mediana usada para substituição: {mediana:.1f} °C")

# ETAPA 8 - SUAVIZAÇÃO DA CURVA VIA MÉDIA MÓVEL
"""
nessa etapa é crucial não tomar muitos ponstos para a média movel
pois isso tende a suavisar subidas e descidas ja que estaremos diluindo
os numeros com outros significativamente maiores ou menores
"""

df_ffill['T_saida_suave'] = df_ffill['Reactor_Temp_C'].rolling(window=5).mean()
print(f"\nEstatísticas após limpeza:")
print(f"  Média:  {df_ffill['Reactor_Temp_C'].mean():.1f} °C")
print(f"  Desvio: {df_ffill['Reactor_Temp_C'].std():.1f} °C")
print(f"  Mín:    {df_ffill['Reactor_Temp_C'].min():.1f} °C")
print(f"  Máx:    {df_ffill['Reactor_Temp_C'].max():.1f} °C")

# ETAPA 9 - PLOT DAS SÉRTIES SUJAS E TRATADAS PARA CRITÉRIO COMPARATIVO

fig, axes = plt.subplots(1, 2, figsize=(14, 4))
axes[0].plot(df.index, df['Reactor_Temp_C'], 'r-', alpha=0.7, linewidth=0.8)
axes[0].set_title('Original (sujo)')
axes[0].set_ylabel('T_saída (°C)')
axes[1].plot(df_ffill.index, df_ffill['T_saida_suave'], 'b-', linewidth=0.8)
axes[1].set_title('Após limpeza (ffill + IQR + média móvel)')
axes[1].set_ylabel('T_saída (°C)')
for ax in axes:
    ax.set_xlabel('Tempo')
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

"""
REFLEXÃO 2 MINUTOS:
eu não gosto da ideia de substituir todos os outliers por um valor médio do sistema, em especial
nos processos monitorados em janelas curtas.
janelas curtas podem não ser tão significativas para avaliar o comportamento geral do processo
isso pode levar a substituuição de valores muito baixos em regioes com tendencia de crescimento
e vice versa.
gosto muito da ideia de usar média movel para tratar ouliers com uma determinada janela e esse
calculo ser feito (logicamente) não envolvendo os outlier ja que eles levaraiam o resultado muito para cima ou para baixo
"""

"""
EXERCICIO EM GRUPO DISCUTIDO NA SALA
essa discussão foi feita a partir dos dados fornecidos pelo repositório do proprio professor
por isso não estão abordados nesse codigo.
nossa equipe (C) respondeu que:
1. média móvel como tecnica de limpeza, pode ser usado IQR
"""