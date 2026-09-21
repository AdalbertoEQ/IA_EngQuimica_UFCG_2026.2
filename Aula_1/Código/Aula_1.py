"""
Essa atividade foi realizada por José Adalberto Martins Filho e Isadora Maria Neves Feitosa.
por motivos pessoais não foi possivel enviar separadamente, caso o senhor deseje podemos refazer e reenviar oq aunto antes

OBS:
devido a problemas enfrentados no colab e a falta de tempo devido à participação na semana do engenehiro quimico
não pudemos enviar atrvés do Colab, pedimos mil desculpas por isso e na proxima atividade enviaremos corretamente.
"""


# ETAPA 1 - IMPORTAR AS BIBLIOTECAS DE INTERESSE
"""
para trabalhar com os dataframes/dataset vamos precisar da biblioteca pandas para tanto abrir esses arquivos
quanto para esecutar algumas analises importantes quanto a caracteristicas desses dados alem da função Path dentro da
biblioteca pathlib para que possamos nos lacalizar dentro dos arquivos e assim, encontrar os dados de interesse além da matplotlib 
para relizar o plot de nosso grafico.
"""

import pandas as pd
from pathlib import Path
import matplotlib.pylab as plt

# ETAPA 2 - LOCALIZAR OS DADOS COM RELAÇÂO A ESSE SCRIPT

caminho_script = Path(__file__).resolve() #essa linha de codigo vai definir o caminho do presente codigo independente de que pasta está salvo
raiz = caminho_script.parent.parent #essa linha de codigo vai determinar a raiz da pasta do programa, a partir dela vamos ao dataset
planilha = raiz / 'PLanilha' / 'waterquality.csv' #esse é o diretorio para acessar nossos dados

df = pd.read_csv(planilha) #essa linha usa a biblioteca pandas para ler os dados

# ETAPA 3 - LEITURA DE PARAMETROS DE INTERESSE

    # vejamos as 5 primeiras linhas do dataset
linhas = df.head()
print(linhas)

    # informações sobre o dataset
info = df.info()
print(info)

    # estatistica descritiva dos dados contidos no dataset
Est_desc = df.describe()
print(Est_desc)


#PAUSA REFLEXIVA

"""
a parte estatistica descritiva com df.describe() nos trás diversas informações importantes, em espcial a média e o desvio padrão
além dos valores maximos, 25%, 50%, 75% e máximo.
observamos que os dados coletados em plantas reais são muito abrangentes.
nesse caso em particular temo:
pressão, temperatura, vazão, setpoints, etc.
"""

#PERGUNTA 1 - CORRELAÇÂO ENTRE VARIÁVEIS
df_numeric = df.select_dtypes(include='number')
correelacoes = df_numeric.corr()
print(correelacoes) # essa matriz mostra como as diversas variaveis do processo se relacionam 2x2

#PERGUNTA 2 - VISUALIZAÇÃO TEMPORAL
df['timestamp'] = pd.to_datetime(df['Date'])

df = df.drop_duplicates(subset=["timestamp"])
df = df.sort_values(by="timestamp").reset_index(drop=True) #essas duas linhas 54 e 55 estão ai para corrigir problema de dados duplicados

plt.plot(df['timestamp'], df['WaterTemp (C)'], linewidth=0.5)
plt.xlabel('Tempo')
plt.ylabel('T_agua (°C)')
plt.title('Temperatura da agua vs tempo')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

#PERGUNTA 3 - INTERPRETAÇÂO

"""
trata-se meramente de um grafico de temperatura versus tempo, não há muito o que observar ou concluir ja que o contexto dos dados não é conhecido,
mas, quanto à cara do grafico podemos observar que a temperatura varia consistentemente dentro de uma faixa muito bem definida com dois possiveis
outlier. Para concluir isso seria necessario realizar um tratamento nos dados e buscar relacionar a outros dados da planta para determinar se é um
diusturbio real ou ruídos na leitura.
"""