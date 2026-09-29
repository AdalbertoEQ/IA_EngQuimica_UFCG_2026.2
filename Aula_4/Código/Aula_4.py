import pandas as pd
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

sns.set_theme(style="darkgrid")

codigo = Path(__file__).resolve()
raiz = codigo.parent.parent
planilha = raiz / "Planilha" / "sensor_readings.csv"

df = pd.read_csv(planilha)

df.set_index('timestamp', inplace=True)

print(f"Shape: {df.shape}")
print(f"\nInfo:")
print(df.info())
print(f"\nDescriptive stats:")
print(df.describe().round(2))

cols = ['temperature_c', 'pressure_kpa', 'current_a', 'rpm']
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, col in zip(axes.ravel(), cols):
    sns.histplot(df[col], bins=50, kde=True, ax=ax, color='steelblue')
    ax.set_title(f'Distribuição de {col}')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df[cols], orient='h', palette='Set2')
plt.title('Boxplot das variáveis principais')
plt.tight_layout()
plt.show()

"""
# Amostra de 3 dias
df_3d = df['2026-08-01':'2026-08-03']
df_3d[['temperature_c', 'pressure_kpa']].plot(figsize=(14, 5), title='Temperaturas — 3 dias')
plt.ylabel('T (°C)')
plt.tight_layout()
plt.show()
"""

# Pairplot (amostra para não travar — 2000 pontos aleatórios)
df_sample = df.sample(2000, random_state=42)
sns.pairplot(df_sample, vars=cols, corner=True, kind='reg',
             plot_kws={'line_kws': {'color': 'red', 'alpha': 0.3}})
plt.suptitle('Pairplot — Variáveis Principais', y=1.02)
plt.show()

# Heatmap de correlação
plt.figure(figsize=(10, 8))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu', center=0,
            square=True, linewidths=0.5)
plt.title('Matriz de Correlação — Coluna de Destilação')
plt.tight_layout()
plt.show()