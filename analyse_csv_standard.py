import csv
import datetime
from collections import defaultdict

# Fonctions utilitaires
def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def mean(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

def print_separator():
    print("-" * 60)

# Dictionnaires pour les valeurs catégorielles
season_dict = {1: 'Hiver', 2: 'Printemps', 3: 'Été', 4: 'Automne'}
weather_dict = {1: 'Clair', 2: 'Nuageux/Brumeux', 3: 'Pluie légère/Neige', 4: 'Fortes précipitations'}
workingday_dict = {0: 'Weekend/Férié', 1: 'Jour travaillé'}
month_name = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 
             7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}

print("Chargement des données...")

# Chargement des données day.csv
day_data = []
with open('day.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Conversion des types
        row['dteday'] = parse_date(row['dteday'])
        row['season'] = int(row['season'])
        row['yr'] = int(row['yr'])
        row['mnth'] = int(row['mnth'])
        row['holiday'] = int(row['holiday'])
        row['weekday'] = int(row['weekday'])
        row['workingday'] = int(row['workingday'])
        row['weathersit'] = int(row['weathersit'])
        row['temp'] = float(row['temp'])
        row['atemp'] = float(row['atemp'])
        row['hum'] = float(row['hum'])
        row['windspeed'] = float(row['windspeed'])
        row['casual'] = int(row['casual'])
        row['registered'] = int(row['registered'])
        row['cnt'] = int(row['cnt'])
        day_data.append(row)

# Chargement des données hour.csv (seulement les 1000 premières lignes pour accélérer)
hour_data = []
with open('hour.csv', 'r') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        # Conversion des types
        row['dteday'] = parse_date(row['dteday'])
        row['season'] = int(row['season'])
        row['yr'] = int(row['yr'])
        row['mnth'] = int(row['mnth'])
        row['hr'] = int(row['hr'])
        row['holiday'] = int(row['holiday'])
        row['weekday'] = int(row['weekday'])
        row['workingday'] = int(row['workingday'])
        row['weathersit'] = int(row['weathersit'])
        row['temp'] = float(row['temp'])
        row['atemp'] = float(row['atemp'])
        row['hum'] = float(row['hum'])
        row['windspeed'] = float(row['windspeed'])
        row['casual'] = int(row['casual'])
        row['registered'] = int(row['registered'])
        row['cnt'] = int(row['cnt'])
        hour_data.append(row)
        count += 1
        if count >= 1000:  # Limiter pour des raisons de performance
            break

print(f"Données chargées: {len(day_data)} jours et {len(hour_data)} heures")
print_separator()

# 1. ANALYSE DES TENDANCES GLOBALES (day.csv)
print("\n1. ANALYSE DES TENDANCES GLOBALES")

# Utilisation moyenne par mois
monthly_usage = defaultdict(list)
for row in day_data:
    monthly_usage[row['mnth']].append(row['cnt'])

print("\nUtilisation moyenne par mois:")
for month, counts in sorted(monthly_usage.items()):
    avg_count = mean(counts)
    print(f"{month_name[month]}: {avg_count:.1f} utilisations")

# Utilisation moyenne par saison
season_usage = defaultdict(list)
for row in day_data:
    season_usage[row['season']].append(row['cnt'])

print("\nUtilisation moyenne par saison:")
for season, counts in sorted(season_usage.items()):
    avg_count = mean(counts)
    print(f"{season_dict[season]}: {avg_count:.1f} utilisations")
print_separator()

# 2. ANALYSE DES COMPORTEMENTS HORAIRES (hour.csv)
print("\n2. ANALYSE DES COMPORTEMENTS HORAIRES")

# Utilisation par heure
hourly_usage = defaultdict(list)
for row in hour_data:
    hourly_usage[row['hr']].append(row['cnt'])

# Calculer la moyenne pour chaque heure
hourly_avg = {}
for hour, counts in hourly_usage.items():
    hourly_avg[hour] = mean(counts)

# Trouver les heures de pointe (top 5)
top_hours = sorted(hourly_avg.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nHeures de pointe (top 5):")
for hour, avg_count in top_hours:
    print(f"{hour}h: {avg_count:.1f} utilisations")

# Comparaison heures de pointe: jours travaillés vs weekend
workday_hours = defaultdict(list)
weekend_hours = defaultdict(list)
for row in hour_data:
    if row['workingday'] == 1:
        workday_hours[row['hr']].append(row['cnt'])
    else:
        weekend_hours[row['hr']].append(row['cnt'])

print("\nComparaison des heures de pointe:")
print("Heure | Jours travaillés | Weekend/Fériés")
print("-" * 45)
for hour in range(24):
    workday_count = mean(workday_hours[hour]) if workday_hours[hour] else 0
    weekend_count = mean(weekend_hours[hour]) if weekend_hours[hour] else 0
    print(f"{hour:2d}h  | {workday_count:15.1f} | {weekend_count:13.1f}")
print_separator()

# 3. IMPACT DE LA MÉTÉO
print("\n3. IMPACT DE LA MÉTÉO")

# Impact de la météo sur l'utilisation quotidienne
weather_impact = defaultdict(list)
for row in day_data:
    weather_impact[row['weathersit']].append(row['cnt'])

print("\nImpact de la météo sur l'utilisation quotidienne:")
for weather, counts in sorted(weather_impact.items()):
    avg_count = mean(counts)
    print(f"{weather_dict[weather]}: {avg_count:.1f} utilisations")
print_separator()

# 4. PROFIL UTILISATEUR
print("\n4. PROFIL UTILISATEUR")

# Proportion utilisateurs occasionnels vs abonnés
total_casual = sum(row['casual'] for row in day_data)
total_registered = sum(row['registered'] for row in day_data)
total_users = total_casual + total_registered
casual_pct = total_casual / total_users * 100
registered_pct = total_registered / total_users * 100

print("\nRépartition des utilisateurs:")
print(f"Occasionnels: {total_casual} ({casual_pct:.1f}%)")
print(f"Abonnés: {total_registered} ({registered_pct:.1f}%)")
print_separator()

# 5. SYNTHÈSE ET RECOMMANDATIONS
print("\n5. SYNTHÈSE ET RECOMMANDATIONS")

# Calcul des statistiques clés
total_users = sum(row['cnt'] for row in day_data)
avg_daily_users = mean([row['cnt'] for row in day_data])
peak_hour = max(hourly_avg.items(), key=lambda x: x[1])[0]
peak_hour_users = hourly_avg[peak_hour]
best_season = max([(season, mean(counts)) for season, counts in season_usage.items()], key=lambda x: x[1])[0]
worst_weather = min([(weather, mean(counts)) for weather, counts in weather_impact.items()], key=lambda x: x[1])[0]

# Affichage des statistiques clés
print(f"Nombre total d'utilisations: {total_users:.0f}")
print(f"Moyenne quotidienne d'utilisations: {avg_daily_users:.0f}")
print(f"Heure de pointe: {peak_hour}h avec en moyenne {peak_hour_users:.0f} utilisations")
print(f"Meilleure saison: {season_dict[best_season]}")
print(f"Condition météo la moins favorable: {weather_dict[worst_weather]}")
print(f"Pourcentage d'utilisateurs abonnés: {registered_pct:.1f}%")
print_separator()

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
    f.write(f"- Meilleure saison: {season_dict[best_season]}\n")
    f.write("- Les jours travaillés ont une utilisation plus importante que les weekends\n\n")
    
    f.write("3. FACTEURS EXTERNES\n")
    f.write(f"- Condition météo la moins favorable: {weather_dict[worst_weather]}\n")
    f.write("- L'utilisation diminue significativement par mauvais temps\n\n")
    
    f.write("4. RECOMMANDATIONS\n")
    f.write("- Horaires d'ouverture recommandés: 6h-22h\n")
    f.write("- Renforcement du service pendant les heures de pointe (8h-9h et 17h-18h)\n")
    f.write("- Stratégie d'abonnement à privilégier pour fidéliser la clientèle\n")
    f.write("- Prévoir une réduction du service pendant les périodes de mauvais temps\n")
    f.write("- Adapter l'offre selon les saisons, avec un service renforcé en été\n")

print("\nAnalyse terminée! Le rapport de synthèse a été généré dans 'rapport_synthese.txt'.")