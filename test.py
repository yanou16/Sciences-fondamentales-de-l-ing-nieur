import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 1. Charger le CSV
print("Chargement des données...")
df_original = pd.read_csv("server_usage_data.csv")
print(f"Nombre de lignes dans le fichier original: {len(df_original)}")

# 2. Nettoyer les données
duplicates_count = df_original.duplicated().sum()
df = df_original.drop_duplicates()
na_count = df_original.isna().sum().sum() - df.isna().sum().sum()
df = df.dropna()
print(f"Nombre de doublons supprimés: {duplicates_count}")
print(f"Nombre de valeurs manquantes supprimées: {na_count}")
print(f"Nombre de lignes après nettoyage: {len(df)}")

# 3. Convertir la colonne Time en datetime
df['Time'] = pd.to_datetime(df['Time'])
df['Hour'] = df['Time'].dt.hour
df['Date'] = df['Time'].dt.date
df['Day_of_week'] = df['Time'].dt.dayofweek
df['Is_weekend'] = df['Day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# 4. Analyse statistique de base
print("\n--- STATISTIQUES DE BASE ---")
print(df.describe())

# 5. Identifier les pics d'utilisation
print("\n--- PICS D'UTILISATION ---")
max_cpu = df.loc[df['CPU_Usage'].idxmax()]
max_memory = df.loc[df['Memory_Usage'].idxmax()]
max_network = df.loc[df['Network_Usage'].idxmax()]
max_temp = df.loc[df['Temperature'].idxmax()]

print(f"Pic d'utilisation CPU: {max_cpu['CPU_Usage']:.2f}% à {max_cpu['Time']}")
print(f"Pic d'utilisation mémoire: {max_memory['Memory_Usage']:.2f}% à {max_memory['Time']}")
print(f"Pic d'utilisation réseau: {max_network['Network_Usage']:.2f}% à {max_network['Time']}")
print(f"Température maximale: {max_temp['Temperature']:.2f}°C à {max_temp['Time']}")

# 6. Analyser les corrélations
print("\n--- CORRÉLATIONS ---")
correlation_matrix = df[['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']].corr()
print(correlation_matrix)

# 7. Trier et sauvegarder les données selon différents critères
print("\n--- SAUVEGARDE DES DONNÉES TRIÉES ---")

# Par CPU (décroissant)
df_cpu = df.sort_values(by='CPU_Usage', ascending=False)
df_cpu.to_csv("serveur_tri_cpu.csv", index=False)
print("Données triées par CPU sauvegardées dans 'serveur_tri_cpu.csv'")
print(f"Top 5 des utilisations CPU les plus élevées:")
print(df_cpu[['Time', 'CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']].head())

# Par température (décroissant)
df_temp = df.sort_values(by='Temperature', ascending=False)
df_temp.to_csv("serveur_tri_temperature.csv", index=False)
print("\nDonnées triées par température sauvegardées dans 'serveur_tri_temperature.csv'")
print(f"Top 5 des températures les plus élevées:")
print(df_temp[['Time', 'CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']].head())

# Par charge combinée (CPU + Réseau)
df['Combined_Load'] = df['CPU_Usage'] * 0.6 + df['Network_Usage'] * 0.4
df_load = df.sort_values(by='Combined_Load', ascending=False)
df_load.to_csv("serveur_tri_charge_combinee.csv", index=False)
print("\nDonnées triées par charge combinée sauvegardées dans 'serveur_tri_charge_combinee.csv'")
print(f"Top 5 des charges combinées les plus élevées:")
print(df_load[['Time', 'CPU_Usage', 'Network_Usage', 'Combined_Load', 'Temperature']].head())

# 8. Analyse par heure de la journée
print("\n--- UTILISATION MOYENNE PAR HEURE ---")
hourly_avg = df.groupby('Hour').mean(numeric_only=True)
print(hourly_avg[['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']])

# Identifier les heures de pointe
peak_hours = hourly_avg['CPU_Usage'].nlargest(3)
print("\nHeures de pointe (CPU):")
for hour, value in peak_hours.items():
    print(f"- {hour}h: {value:.2f}% d'utilisation CPU")

# 9. Analyse par jour de la semaine
print("\n--- UTILISATION PAR JOUR DE LA SEMAINE ---")
day_names = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
daily_avg = df.groupby('Day_of_week').mean(numeric_only=True)
daily_avg['Day_Name'] = [day_names[i] for i in range(7)]
print(daily_avg[['Day_Name', 'CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']])

# Comparaison semaine vs weekend
print("\n--- COMPARAISON SEMAINE VS WEEKEND ---")
weekend_comparison = df.groupby('Is_weekend').mean(numeric_only=True)
print("Jours de semaine (0) vs Weekend (1):")
print(weekend_comparison[['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']])

# 10. Créer un rapport de synthèse détaillé
with open("rapport_analyse_serveur_detaille.txt", "w") as f:
    f.write("RAPPORT D'ANALYSE DÉTAILLÉE DES DONNÉES SERVEUR\n")
    f.write("============================================\n\n")
    
    f.write("1. STATISTIQUES GÉNÉRALES\n")
    f.write(f"Période analysée: {df['Time'].min()} à {df['Time'].max()}\n")
    f.write(f"Nombre total de mesures: {len(df)}\n")
    f.write(f"Nombre de doublons supprimés: {duplicates_count}\n")
    f.write(f"Nombre de valeurs manquantes supprimées: {na_count}\n")
    f.write(f"Utilisation CPU moyenne: {df['CPU_Usage'].mean():.2f}%\n")
    f.write(f"Utilisation mémoire moyenne: {df['Memory_Usage'].mean():.2f}%\n")
    f.write(f"Utilisation réseau moyenne: {df['Network_Usage'].mean():.2f}%\n")
    f.write(f"Température moyenne: {df['Temperature'].mean():.2f}°C\n\n")
    
    f.write("2. PICS D'UTILISATION\n")
    f.write(f"Pic d'utilisation CPU: {max_cpu['CPU_Usage']:.2f}% à {max_cpu['Time']}\n")
    f.write(f"Pic d'utilisation mémoire: {max_memory['Memory_Usage']:.2f}% à {max_memory['Time']}\n")
    f.write(f"Pic d'utilisation réseau: {max_network['Network_Usage']:.2f}% à {max_network['Time']}\n")
    f.write(f"Température maximale: {max_temp['Temperature']:.2f}°C à {max_temp['Time']}\n\n")
    
    f.write("3. CORRÉLATIONS\n")
    f.write(str(correlation_matrix))
    f.write("\n\n")
    
    f.write("4. ANALYSE TEMPORELLE\n")
    f.write("a) Heures de pointe (CPU):\n")
    for hour, value in peak_hours.items():
        f.write(f"   - {hour}h: {value:.2f}% d'utilisation CPU\n")
    
    f.write("\nb) Comparaison jours de semaine vs weekend:\n")
    f.write("   Jours de semaine:\n")
    f.write(f"   - CPU: {weekend_comparison.loc[0, 'CPU_Usage']:.2f}%\n")
    f.write(f"   - Température: {weekend_comparison.loc[0, 'Temperature']:.2f}°C\n")
    f.write("   Weekend:\n")
    f.write(f"   - CPU: {weekend_comparison.loc[1, 'CPU_Usage']:.2f}%\n")
    f.write(f"   - Température: {weekend_comparison.loc[1, 'Temperature']:.2f}°C\n\n")
    
    f.write("5. RECOMMANDATIONS\n")
    if df['CPU_Usage'].max() > 80:
        f.write("- Attention: Pics d'utilisation CPU élevés, considérer une mise à niveau\n")
    if df['Temperature'].max() > 70:
        f.write("- Attention: Températures élevées détectées, vérifier le système de refroidissement\n")
    if df['Memory_Usage'].mean() > 70:
        f.write("- Attention: Utilisation mémoire moyenne élevée, envisager d'augmenter la RAM\n")
    
    # Recommandations basées sur l'analyse temporelle
    peak_hour = hourly_avg['CPU_Usage'].idxmax()
    f.write(f"- Planifier les tâches intensives en dehors de {peak_hour}h, heure de pointe identifiée\n")
    
    # Recommandations basées sur les corrélations
    if correlation_matrix.loc['Network_Usage', 'Temperature'] > 0.7:
        f.write("- Optimiser le trafic réseau pour réduire l'échauffement du système\n")
    
    f.write("\n6. CONCLUSION\n")
    f.write("Cette analyse détaillée des données serveur a permis d'identifier:\n")
    f.write("- Les périodes de charge maximale\n")
    f.write("- Les corrélations entre les différentes métriques\n")
    f.write("- Les tendances d'utilisation par heure et par jour\n")
    f.write("- Des recommandations techniques pour optimiser les performances\n")
    f.write(f"\nRapport généré le {datetime.now().strftime('%Y-%m-%d à %H:%M:%S')}")

print("\nAnalyse détaillée terminée! Rapport sauvegardé dans 'rapport_analyse_serveur_detaille.txt'")