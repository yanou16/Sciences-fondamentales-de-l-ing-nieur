import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration pour de meilleurs graphiques
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Chargement des données
print("Chargement des données...")
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

# Conversion des dates
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Ajout de colonnes utiles
df_day['month_name'] = df_day['dteday'].dt.month_name()
df_day['day_name'] = df_day['dteday'].dt.day_name()
df_hour['hour'] = df_hour['hr']

# Dictionnaires pour les valeurs catégorielles
season_dict = {1: 'Hiver', 2: 'Printemps', 3: 'Été', 4: 'Automne'}
weather_dict = {1: 'Clair', 2: 'Nuageux/Brumeux', 3: 'Pluie légère/Neige', 4: 'Fortes précipitations'}
workingday_dict = {0: 'Weekend/Férié', 1: 'Jour travaillé'}

# Application des dictionnaires
df_day['season_name'] = df_day['season'].map(season_dict)
df_day['weather_name'] = df_day['weathersit'].map(weather_dict)
df_day['workingday_name'] = df_day['workingday'].map(workingday_dict)
df_hour['season_name'] = df_hour['season'].map(season_dict)
df_hour['weather_name'] = df_hour['weathersit'].map(weather_dict)
df_hour['workingday_name'] = df_hour['workingday'].map(workingday_dict)

# 1. ANALYSE DES TENDANCES GLOBALES (day.csv)
print("\n1. ANALYSE DES TENDANCES GLOBALES")

# Tendance globale sur la période
plt.figure()
df_day.groupby('dteday')['cnt'].sum().plot(title="Évolution de l'utilisation des vélos sur la période")
plt.xlabel("Date")
plt.ylabel("Nombre total d'utilisations")
plt.tight_layout()
plt.savefig('tendance_globale.png')

# Saisonnalité par mois
plt.figure()
monthly_data = df_day.groupby(df_day['dteday'].dt.month).agg({'cnt': 'mean'})
sns.barplot(x=monthly_data.index, y=monthly_data['cnt'])
plt.title("Utilisation moyenne par mois")
plt.xlabel("Mois")
plt.ylabel("Nombre moyen d'utilisations")
plt.xticks(range(12), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
plt.tight_layout()
plt.savefig('utilisation_par_mois.png')

# Saisonnalité par saison
plt.figure()
season_data = df_day.groupby('season_name').agg({'cnt': 'mean'})
sns.barplot(x=season_data.index, y=season_data['cnt'])
plt.title("Utilisation moyenne par saison")
plt.xlabel("Saison")
plt.ylabel("Nombre moyen d'utilisations")
plt.tight_layout()
plt.savefig('utilisation_par_saison.png')

# 2. ANALYSE DES COMPORTEMENTS HORAIRES (hour.csv)
print("\n2. ANALYSE DES COMPORTEMENTS HORAIRES")

# Utilisation par heure
plt.figure()
hourly_usage = df_hour.groupby('hr').agg({'cnt': 'mean'})
sns.lineplot(x=hourly_usage.index, y=hourly_usage['cnt'])
plt.title("Utilisation moyenne par heure")
plt.xlabel("Heure de la journée")
plt.ylabel("Nombre moyen d'utilisations")
plt.xticks(range(24))
plt.tight_layout()
plt.savefig('utilisation_par_heure.png')

# Comparaison heures de pointe: jours travaillés vs weekend
plt.figure()
workday_hours = df_hour[df_hour['workingday'] == 1].groupby('hr').agg({'cnt': 'mean'})
weekend_hours = df_hour[df_hour['workingday'] == 0].groupby('hr').agg({'cnt': 'mean'})

plt.plot(workday_hours.index, workday_hours['cnt'], label='Jours travaillés')
plt.plot(weekend_hours.index, weekend_hours['cnt'], label='Weekend/Fériés')
plt.title("Utilisation par heure: Jours travaillés vs Weekend/Fériés")
plt.xlabel("Heure de la journée")
plt.ylabel("Nombre moyen d'utilisations")
plt.xticks(range(24))
plt.legend()
plt.tight_layout()
plt.savefig('jours_travailles_vs_weekend.png')

# 3. IMPACT DE LA MÉTÉO
print("\n3. IMPACT DE LA MÉTÉO")

# Impact de la météo sur l'utilisation quotidienne
plt.figure()
weather_impact = df_day.groupby('weather_name').agg({'cnt': 'mean'})
sns.barplot(x=weather_impact.index, y=weather_impact['cnt'])
plt.title("Impact de la météo sur l'utilisation quotidienne")
plt.xlabel("Conditions météo")
plt.ylabel("Nombre moyen d'utilisations")
plt.tight_layout()
plt.savefig('impact_meteo.png')

# 4. PROFIL UTILISATEUR
print("\n4. PROFIL UTILISATEUR")

# Proportion utilisateurs occasionnels vs abonnés
plt.figure()
user_types = df_day[['casual', 'registered']].sum()
plt.pie(user_types, labels=['Occasionnels', 'Abonnés'], autopct='%1.1f%%')
plt.title("Répartition des utilisateurs")
plt.tight_layout()
plt.savefig('repartition_utilisateurs.png')

# Évolution des types d'utilisateurs dans le temps
plt.figure()
df_day['casual_pct'] = df_day['casual'] / df_day['cnt'] * 100
df_day['registered_pct'] = df_day['registered'] / df_day['cnt'] * 100

# Moyenne mobile sur 30 jours pour lisser la courbe
casual_ma = df_day.set_index('dteday')['casual_pct'].rolling(window=30).mean()
registered_ma = df_day.set_index('dteday')['registered_pct'].rolling(window=30).mean()

plt.plot(casual_ma.index, casual_ma, label='Occasionnels (%)')
plt.plot(registered_ma.index, registered_ma, label='Abonnés (%)')
plt.title("Évolution de la proportion des types d'utilisateurs")
plt.xlabel("Date")
plt.ylabel("Pourcentage")
plt.legend()
plt.tight_layout()
plt.savefig('evolution_types_utilisateurs.png')

# 5. SYNTHÈSE ET RECOMMANDATIONS
print("\n5. SYNTHÈSE ET RECOMMANDATIONS")

# Calcul des statistiques clés
total_users = df_day['cnt'].sum()
avg_daily_users = df_day['cnt'].mean()
peak_hour = hourly_usage['cnt'].idxmax()
peak_hour_users = hourly_usage['cnt'].max()
best_season = season_data['cnt'].idxmax()
worst_weather = weather_impact['cnt'].idxmin()
registered_pct = df_day['registered'].sum() / total_users * 100

# Affichage des statistiques clés
print(f"Nombre total d'utilisations: {total_users:.0f}")
print(f"Moyenne quotidienne d'utilisations: {avg_daily_users:.0f}")
print(f"Heure de pointe: {peak_hour}h avec en moyenne {peak_hour_users:.0f} utilisations")
print(f"Meilleure saison: {best_season}")
print(f"Condition météo la moins favorable: {worst_weather}")
print(f"Pourcentage d'utilisateurs abonnés: {registered_pct:.1f}%")

# Création d'un rapport de synthèse
with open('rapport_synthese.txt', 'w', encoding='utf-8') as f:
    f.write("RAPPORT DE SYNTHÈSE - SERVICE DE VÉLOS\n")
    f.write("=====================================\n\n")
    
    f.write("1. DEMANDE EXISTANTE\n")
    f.write(f"- Nombre total d'utilisations: {total_users:.0f}\n")
    f.write(f"- Moyenne quotidienne d'utilisations: {avg_daily_users:.0f}\n")
    f.write(f"- Pourcentage d'utilisateurs abonnés: {registered_pct:.1f}%\n\n")
    
    f.write("2. MOMENTS STRATÉGIQUES\n")
    f.write(f"- Heure de pointe: {peak_hour}h avec en moyenne {peak_hour_users:.0f} utilisations\n")
    f.write(f"- Meilleure saison: {best_season}\n")
    f.write("- Les jours travaillés ont une utilisation plus importante que les weekends\n\n")
    
    f.write("3. FACTEURS EXTERNES\n")
    f.write(f"- Condition météo la moins favorable: {worst_weather}\n")
    f.write("- L'utilisation diminue significativement par mauvais temps\n\n")
    
    f.write("4. RECOMMANDATIONS\n")
    f.write("- Horaires d'ouverture recommandés: 6h-22h\n")
    f.write("- Renforcement du service pendant les heures de pointe (8h-9h et 17h-18h)\n")
    f.write("- Stratégie d'abonnement à privilégier pour fidéliser la clientèle\n")
    f.write("- Prévoir une réduction du service pendant les périodes de mauvais temps\n")
    f.write("- Adapter l'offre selon les saisons, avec un service renforcé en été\n")

print("\nAnalyse terminée! Les graphiques et le rapport de synthèse ont été générés.")