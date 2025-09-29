import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# Charger les données
print("Chargement des données...")
df = pd.read_csv("server_usage_data.csv")
df['Time'] = pd.to_datetime(df['Time'])
df['Hour'] = df['Time'].dt.hour
df['Date'] = df['Time'].dt.date
df['Day_of_week'] = df['Time'].dt.dayofweek
df['Is_weekend'] = df['Day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# Créer un dossier pour les graphiques si nécessaire
import os
if not os.path.exists('graphiques'):
    os.makedirs('graphiques')

# 1. Graphique d'évolution temporelle
plt.figure(figsize=(12, 6))
plt.plot(df['Time'], df['CPU_Usage'], label='CPU Usage (%)')
plt.plot(df['Time'], df['Temperature'], label='Temperature (°C)')
plt.title('Évolution de l\'utilisation CPU et de la température')
plt.xlabel('Date et heure')
plt.ylabel('Valeur')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('graphiques/evolution_temporelle.png')
plt.close()
print("Graphique d'évolution temporelle créé")

# 2. Graphique de corrélation (heatmap)
plt.figure(figsize=(8, 6))
correlation_matrix = df[['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matrice de corrélation des métriques')
plt.tight_layout()
plt.savefig('graphiques/correlation_heatmap.png')
plt.close()
print("Graphique de corrélation créé")

# 3. Graphique d'utilisation moyenne par heure
hourly_avg = df.groupby('Hour').mean(numeric_only=True)
plt.figure(figsize=(12, 6))
plt.plot(hourly_avg.index, hourly_avg['CPU_Usage'], marker='o', label='CPU Usage (%)')
plt.plot(hourly_avg.index, hourly_avg['Temperature'], marker='s', label='Temperature (°C)')
plt.title('Utilisation moyenne par heure de la journée')
plt.xlabel('Heure')
plt.ylabel('Valeur moyenne')
plt.xticks(range(0, 24))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('graphiques/utilisation_par_heure.png')
plt.close()
print("Graphique d'utilisation par heure créé")

# 4. Graphique comparatif semaine vs weekend
plt.figure(figsize=(10, 6))
weekend_comparison = df.groupby('Is_weekend').mean(numeric_only=True)
metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
x = np.arange(len(metrics))
width = 0.35

plt.bar(x - width/2, weekend_comparison.loc[0, metrics], width, label='Semaine')
plt.bar(x + width/2, weekend_comparison.loc[1, metrics], width, label='Weekend')
plt.title('Comparaison des métriques : Semaine vs Weekend')
plt.xticks(x, metrics)
plt.ylabel('Valeur moyenne')
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('graphiques/semaine_vs_weekend.png')
plt.close()
print("Graphique comparatif semaine vs weekend créé")

# 5. Histogramme de distribution des valeurs
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.hist(df['CPU_Usage'], bins=20, color='blue', alpha=0.7)
plt.title('Distribution de l\'utilisation CPU')
plt.xlabel('CPU Usage (%)')
plt.ylabel('Fréquence')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.hist(df['Memory_Usage'], bins=20, color='green', alpha=0.7)
plt.title('Distribution de l\'utilisation mémoire')
plt.xlabel('Memory Usage (%)')
plt.ylabel('Fréquence')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.hist(df['Network_Usage'], bins=20, color='red', alpha=0.7)
plt.title('Distribution de l\'utilisation réseau')
plt.xlabel('Network Usage (%)')
plt.ylabel('Fréquence')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.hist(df['Temperature'], bins=20, color='orange', alpha=0.7)
plt.title('Distribution de la température')
plt.xlabel('Temperature (°C)')
plt.ylabel('Fréquence')
plt.grid(True)

plt.tight_layout()
plt.savefig('graphiques/distributions.png')
plt.close()
print("Histogrammes de distribution créés")

# 6. Nuage de points pour visualiser la corrélation
plt.figure(figsize=(10, 8))
plt.scatter(df['Network_Usage'], df['Temperature'], alpha=0.5)
plt.title('Corrélation entre utilisation réseau et température')
plt.xlabel('Network Usage (%)')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.tight_layout()
plt.savefig('graphiques/correlation_reseau_temperature.png')
plt.close()
print("Graphique de corrélation réseau-température créé")

# 7. Boxplot pour visualiser la distribution par jour de la semaine
plt.figure(figsize=(12, 6))
day_names = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
df['Day_Name'] = df['Day_of_week'].map(day_names)
sns.boxplot(x='Day_Name', y='CPU_Usage', data=df)
plt.title('Distribution de l\'utilisation CPU par jour de la semaine')
plt.xlabel('Jour')
plt.ylabel('CPU Usage (%)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('graphiques/boxplot_cpu_par_jour.png')
plt.close()
print("Boxplot par jour de la semaine créé")

print("\nTous les graphiques ont été créés dans le dossier 'graphiques'")