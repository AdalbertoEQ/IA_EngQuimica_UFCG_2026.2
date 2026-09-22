import pandas as pd
from pathlib import Path
import numpy as np

caminho = Path(__file__).resolve()
raiz = caminho.parent.parent
planilha = raiz / 'Planilha' / 'petrochemical_advanced_data.csv'

df = pd.read_csv(planilha)

df['T atraso 30 min'] = df['Reactor_Temp_C'].shift(1)
df['T atraso 60 min'] = df['Reactor_Temp_C'].shift(2)
df['T atraso 90 min'] = df['Reactor_Temp_C'].shift(3)

df['T atrasado 90 min suave'] = df['T atraso 90 min'].rolling(3).mean()
df['dT coluna'] = df['T atraso 90 min'].diff()

df['P atraso 30 min'] = df['Reactor_Pressure_Bar'].shift(1)
df['P atraso 60 min'] = df['Reactor_Pressure_Bar'].shift(2)
df['P atraso 90 min'] = df['Reactor_Pressure_Bar'].shift(3)

df['P atrasado 90 min suave'] = df['P atraso 90 min'].rolling(3).mean()
df['dP coluna'] = df['P atraso 90 min'].diff()

df.dropna(inplace=True)
print(f"Shape final: {df.shape}")
print(f"Features: {[c for c in df.columns if c != 'Product_Yield_Tons']}")
print(f"Target: Product_Yield_Tons")

corr = df.corr(numeric_only=True)['Product_Yield_Tons'].sort_values(ascending=False)
print("Correlação de cada feature com a produção:")
print(corr)
print(f"\nTop 5 features:")
print(corr.head(5))