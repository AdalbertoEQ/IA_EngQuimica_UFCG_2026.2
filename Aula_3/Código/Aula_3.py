import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pylab as plt

caminho = Path(__file__).resolve()
raiz = caminho.parent.parent
planilha = raiz / 'Planilha' / 'Distillation Column Dataset.csv'

df = pd.read_csv(planilha)

df['T1 atraso 30 min'] = df['Sensor1'].shift(1)
df['T1 atraso 60 min'] = df['Sensor1'].shift(2)
df['T1 atraso 90 min'] = df['Sensor1'].shift(3)

df['T1 atrasado 90 min suave'] = df['T1 atraso 90 min'].rolling(3).mean()
df['dT1 coluna'] = df['T1 atraso 90 min'].diff()

df['S5 atraso 30 min'] = df['Sensor5'].shift(1)
df['S5 atraso 60 min'] = df['Sensor5'].shift(2)
df['S5 atraso 90 min'] = df['Sensor5'].shift(3)

df['S5 atrasado 90 min suave'] = df['S5 atraso 90 min'].rolling(3).mean()
df['dS5 coluna'] = df['S5 atraso 90 min'].diff()

df.dropna(inplace=True)
print(f"Shape final: {df.shape}")
print(f"Features: {[c for c in df.columns if c != 'conversao']}")
print(f"Target: Fração")

corr = df.corr()['MoleFractionTX'].sort_values(ascending=False)
print("Correlação de cada feature com a conversão:")
print(corr)
print(f"\nTop 5 features:")
print(corr.head(5))