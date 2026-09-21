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
df_Z = df
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
df_Z_ffill = df_Z.ffill()
print(f"NaNs após ffill: {df_ffill.isnull().sum().sum()}")

# ETAPA 6 - DETERMINAÇÃO DOS OUTLIERS

    # determinação via IQR
Q1 = df_ffill['Reactor_Temp_C'].quantile(0.25)
Q3 = df_ffill['Reactor_Temp_C'].quantile(0.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR
outliersIQR = (df_ffill['Reactor_Temp_C'] < lim_inf) | (df_ffill['Reactor_Temp_C'] > lim_sup)
print(f"Outliers detectados: {outliersIQR.sum()} ({outliersIQR.mean()*100:.1f}%)")
print(f"Limites: [{lim_inf:.1f}, {lim_sup:.1f}] °C")

    # determinação via Z score
def z_score(df, nome):
    u = df[nome].mean()
    var = (df[nome].var())**0.5
    Z_s = (df[nome]-u)/var
    return(Z_s)

z_score = z_score(df_Z, 'Reactor_Temp_C')
outliers = (z_score < -3) | (z_score > 3)
print(f"Outliers detectados: {outliers.sum()} ({outliers.mean()*100:.1f}%)")
print(f"Limites: [{-3:.1f}, {3:.1f}] °C")

# ETAPA 7 - SUBSTITUIÇÃO DOS OUTLIERS POR UMA MÉDIANA

    # determinação via IQR
mediana = df_ffill['Reactor_Temp_C'].median()
df_ffill.loc[outliersIQR, 'Reactor_Temp_C'] = mediana
print(f"Mediana usada para substituição: {mediana:.1f} °C")

    # determinação via Z score
mediana = df_Z_ffill['Reactor_Temp_C'].median()
df_ffill.loc[outliers, 'Reactor_Temp_C'] = mediana
print(f"Mediana usada para substituição: {mediana:.1f} °C")

# ETAPA 8 - SUAVIZAÇÃO DA CURVA VIA MÉDIA MÓVEL
"""
nessa etapa é crucial não tomar muitos ponstos para a média movel
pois isso tende a suavisar subidas e descidas ja que estaremos diluindo
os numeros com outros significativamente maiores ou menores
"""

    # determinação via IQR
df_ffill['T_saida_suave'] = df_ffill['Reactor_Temp_C'].rolling(window=5).mean()
print(f"\nEstatísticas após limpeza:")
print(f"  Média:  {df_ffill['Reactor_Temp_C'].mean():.1f} °C")
print(f"  Desvio: {df_ffill['Reactor_Temp_C'].std():.1f} °C")
print(f"  Mín:    {df_ffill['Reactor_Temp_C'].min():.1f} °C")
print(f"  Máx:    {df_ffill['Reactor_Temp_C'].max():.1f} °C")

    # determinação via Z score
df_Z_ffill['T_saida_suave'] = df_Z_ffill['Reactor_Temp_C'].rolling(window=5).mean()
print(f"\nEstatísticas após limpeza:")
print(f"  Média:  {df_Z_ffill['Reactor_Temp_C'].mean():.1f} °C")
print(f"  Desvio: {df_Z_ffill['Reactor_Temp_C'].std():.1f} °C")
print(f"  Mín:    {df_Z_ffill['Reactor_Temp_C'].min():.1f} °C")
print(f"  Máx:    {df_Z_ffill['Reactor_Temp_C'].max():.1f} °C")

# ETAPA 9 - PLOT DAS SÉRTIES SUJAS E TRATADAS PARA CRITÉRIO COMPARATIVO

    # determinação via IQR
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

    # determinação via Z score
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
axes[0].plot(df.index, df['Reactor_Temp_C'], 'r-', alpha=0.7, linewidth=0.8)
axes[0].set_title('Original (sujo)')
axes[0].set_ylabel('T_saída (°C)')
axes[1].plot(df_Z_ffill.index, df_Z_ffill['T_saida_suave'], 'b-', linewidth=0.8)
axes[1].set_title('Após limpeza (ffill + Z score + média móvel)')
axes[1].set_ylabel('T_saída (°C)')
for ax in axes:
    ax.set_xlabel('Tempo')
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

    # plot comparativo dos dois metodos
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
axes[0].plot(df_ffill.index, df_ffill['T_saida_suave'], 'b-', linewidth=0.8)
axes[0].set_title('Após limpeza (ffill + IQR + média móvel)')
axes[0].set_ylabel('T_saída (°C)')
axes[1].plot(df_Z_ffill.index, df_Z_ffill['T_saida_suave'], 'b-', linewidth=0.8)
axes[1].set_title('Após limpeza (ffill + Z score + média móvel)')
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
Podemos observar que os graficos sairam bem similares, entretanto na serie onde outliers foram identificados via Z podemos
obervar que ele apresenta apresenta picos maiores. Isso indica que a determinação de ouliert via IQR é mais sensivel a
valores absolutos maiores classificando um numero maior de dados como outliers do que via Z score.
Eu, particularmente, gosto do Z score ser menos sensivel embora hajam ressalvas se os picos são disturbios reais na planta
eles mostram como o sistema funciona, mas, se forem ruídos significa que o Z score deixa passar sujeira que deveria ser
retida.

Como sabemos, nos processos quimicos todas as variaveis estão correlacionadas de uma forma ou de outra, podemos
através de um estudo estensivo determinar se algo é disturbio real ou rído na leitura, como?
Suponhamos um vaso de volume constante onde ocorre um processo qualquer, as variaveis lidas são a pressão e a
temperatura no sistema. Se meu dataset apresenta um pico na pressão e ao verificar a temperatura observamos que esse
pico não ocorreu nela, muito provavelmente o pico visto na pressão se trata de ruído ja que em um gás pressão e temperatura
se correlacionam. Podemos argumentar que nessa situação pode ter ocorrido uma falhar no sensor de temperatura e então não
pudemos observar o pico.
Para evitar esse tipo de problema podemos colocar mais sensores na planta para que haja confiabilidade estatistica.

se houver 3 sensores de temperature e 3 sensores de pressão que estão com seus timstamp sincronizados:
T1, T2, T3 e P1, P2, P3 
Podemos avaliar os 6 ao mesmo tempo e determinar que um outlier na temperatura (exemplo) é ruido caso em apenas 1 entre os
3 sensores apresentar o pico observado, ou se os efeitos do pico da temperatura forem observados em pelo menos 2 dos
sensores de pressão.

outlier de T se:
apenas 1 sensor de temperatura apresentar o pico ou
se 2 sensores de pressão não apresentarem o pico

essa forma de avaliar comparando dados correlacionados retira os dois principais problemas:
falsa exclusão de dados reais da planta
não ver um disturbio por falha no sensor
"""