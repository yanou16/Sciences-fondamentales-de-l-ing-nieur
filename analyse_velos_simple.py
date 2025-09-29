import pandas as pd

# Chargement des données
print("Chargement des données...")
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

# Conversion des dates
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Dictionnaires pour les valeurs catégorielles
season_dict = {1: 'Hiver', 2: 'Printemps', 3: 'Été', 4: 'Automne'}
weather_dict = {1: 'Clair', 2: 'Nuageux/Brumeux', 3: 'Pluie légère/Neige', 4: 'Fortes précipitations'}
workingday_dict = {0: 'Weekend/Férié', 1: 'Jour travaillé'}

# 1. ANALYSE DES TENDANCES GLOBALES (day.csv)
print("\n1. ANALYSE DES TENDANCES GLOBALES")

# Tendance globale sur la période
monthly_usage = df_day.groupby(df_day['dteday'].dt.month).agg({'cnt': 'mean'})
print("\nUtilisation moyenne par mois:")
for month, count in monthly_usage.iterrows():
    month_name = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 
                 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}
    print(f"{month_name[month]}: {count['cnt']:.1f} utilisations")

# Saisonnalité par saison
season_data = df_day.groupby('season').agg({'cnt': 'mean'})
print("\nUtilisation moyenne par saison:")
for season, count in season_data.iterrows():
    print(f"{season_dict[season]}: {count['cnt']:.1f} utilisations")

# 2. ANALYSE DES COMPORTEMENTS HORAIRES (hour.csv)
print("\n2. ANALYSE DES COMPORTEMENTS HORAIRES")

# Utilisation par heure
hourly_usage = df_hour.groupby('hr').agg({'cnt': 'mean'})
print("\nHeures de pointe (top 5):")
top_hours = hourly_usage.sort_values('cnt', ascending=False).head(5)
for hour, count in top_hours.iterrows():
    print(f"{hour}h: {count['cnt']:.1f} utilisations")

# Comparaison heures de pointe: jours travaillés vs weekend
workday_hours = df_hour[df_hour['workingday'] == 1].groupby('hr').agg({'cnt': 'mean'})
weekend_hours = df_hour[df_hour['workingday'] == 0].groupby('hr').agg({'cnt': 'mean'})

print("\nComparaison des heures de pointe:")
print("Heure | Jours travaillés | Weekend/Fériés")
print("-" * 45)
for hour in range(24):
    workday_count = workday_hours.loc[hour, 'cnt'] if hour in workday_hours.index else 0
    weekend_count = weekend_hours.loc[hour, 'cnt'] if hour in weekend_hours.index else 0
    print(f"{hour:2d}h  | {workday_count:15.1f} | {weekend_count:13.1f}")

# 3. IMPACT DE LA MÉTÉO
print("\n3. IMPACT DE LA MÉTÉO")

# Impact de la météo sur l'utilisation quotidienne
weather_impact = df_day.groupby('weathersit').agg({'cnt': 'mean'})
print("\nImpact de la météo sur l'utilisation quotidienne:")
for weather, count in weather_impact.iterrows():
    print(f"{weather_dict[weather]}: {count['cnt']:.1f} utilisations")

# 4. PROFIL UTILISATEUR
print("\n4. PROFIL UTILISATEUR")

# Proportion utilisateurs occasionnels vs abonnés
total_casual = df_day['casual'].sum()
total_registered = df_day['registered'].sum()
total_users = total_casual + total_registered
casual_pct = total_casual / total_users * 100
registered_pct = total_registered / total_users * 100

print("\nRépartition des utilisateurs:")
print(f"Occasionnels: {total_casual} ({casual_pct:.1f}%)")
print(f"Abonnés: {total_registered} ({registered_pct:.1f}%)")

# 5. SYNTHÈSE ET RECOMMANDATIONS
print("\n5. SYNTHÈSE ET RECOMMANDATIONS")

# Calcul des statistiques clés
total_users = df_day['cnt'].sum()
avg_daily_users = df_day['cnt'].mean()
peak_hour = hourly_usage['cnt'].idxmax()
peak_hour_users = hourly_usage['cnt'].max()
best_season = season_dict[season_data['cnt'].idxmax()]
worst_weather = weather_dict[weather_impact['cnt'].idxmin()]

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

print("\nAnalyse terminée! Le rapport de synthèse a été généré.")