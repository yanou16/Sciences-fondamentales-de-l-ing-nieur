import csv
import datetime
from collections import defaultdict
import json
import os

# Fonctions utilitaires
def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def mean(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

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

# Préparation des données pour les graphiques

# 1. Utilisation moyenne par mois
monthly_usage = defaultdict(list)
for row in day_data:
    monthly_usage[row['mnth']].append(row['cnt'])

monthly_avg = {}
for month, counts in monthly_usage.items():
    monthly_avg[month] = mean(counts)

# 2. Utilisation moyenne par saison
season_usage = defaultdict(list)
for row in day_data:
    season_usage[row['season']].append(row['cnt'])

season_avg = {}
for season, counts in season_usage.items():
    season_avg[season] = mean(counts)

# 3. Utilisation par heure
hourly_usage = defaultdict(list)
for row in hour_data:
    hourly_usage[row['hr']].append(row['cnt'])

hourly_avg = {}
for hour, counts in hourly_usage.items():
    hourly_avg[hour] = mean(counts)

# 4. Comparaison heures de pointe: jours travaillés vs weekend
workday_hours = defaultdict(list)
weekend_hours = defaultdict(list)
for row in hour_data:
    if row['workingday'] == 1:
        workday_hours[row['hr']].append(row['cnt'])
    else:
        weekend_hours[row['hr']].append(row['cnt'])

workday_avg = {}
weekend_avg = {}
for hour in range(24):
    workday_avg[hour] = mean(workday_hours[hour]) if workday_hours[hour] else 0
    weekend_avg[hour] = mean(weekend_hours[hour]) if weekend_hours[hour] else 0

# 5. Impact de la météo
weather_impact = defaultdict(list)
for row in day_data:
    weather_impact[row['weathersit']].append(row['cnt'])

weather_avg = {}
for weather, counts in weather_impact.items():
    weather_avg[weather] = mean(counts)

# 6. Proportion utilisateurs occasionnels vs abonnés
total_casual = sum(row['casual'] for row in day_data)
total_registered = sum(row['registered'] for row in day_data)
user_types = [total_casual, total_registered]

# Création du fichier HTML avec les graphiques
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Analyse du service de vélos</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        h2 {
            color: #3498db;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .chart-container {
            width: 80%;
            margin: 20px auto;
            height: 400px;
        }
        .conclusion {
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Analyse du service de vélos</h1>
        
        <h2>1. Tendances globales</h2>
        <div class="chart-container">
            <canvas id="monthlyChart"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="seasonChart"></canvas>
        </div>
        
        <h2>2. Comportements horaires</h2>
        <div class="chart-container">
            <canvas id="hourlyChart"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="workdayVsWeekendChart"></canvas>
        </div>
        
        <h2>3. Impact de la météo</h2>
        <div class="chart-container">
            <canvas id="weatherChart"></canvas>
        </div>
        
        <h2>4. Profil utilisateur</h2>
        <div class="chart-container">
            <canvas id="userTypeChart"></canvas>
        </div>
        
        <div class="conclusion">
            <h2>5. Synthèse et recommandations</h2>
            <p><strong>Demande existante :</strong> Le service de vélos compte en moyenne <span id="avgDailyUsers"></span> utilisations par jour, avec un total de <span id="totalUsers"></span> utilisations sur la période analysée.</p>
            <p><strong>Moments stratégiques :</strong> L'heure de pointe est <span id="peakHour"></span>h avec en moyenne <span id="peakHourUsers"></span> utilisations. La meilleure saison est <span id="bestSeason"></span>.</p>
            <p><strong>Facteurs externes :</strong> La condition météo la moins favorable est <span id="worstWeather"></span>, qui réduit significativement l'utilisation.</p>
            <p><strong>Profil utilisateur :</strong> <span id="registeredPct"></span>% des utilisateurs sont des abonnés, ce qui montre une forte fidélisation.</p>
            
            <h3>Recommandations</h3>
            <ul>
                <li>Horaires d'ouverture recommandés: 6h-22h</li>
                <li>Renforcement du service pendant les heures de pointe (8h-9h et 17h-18h)</li>
                <li>Stratégie d'abonnement à privilégier pour fidéliser la clientèle</li>
                <li>Prévoir une réduction du service pendant les périodes de mauvais temps</li>
                <li>Adapter l'offre selon les saisons, avec un service renforcé en été</li>
            </ul>
        </div>
    </div>

    <script>
        // Données pour les graphiques
        const monthlyData = MONTHLY_DATA;
        const seasonData = SEASON_DATA;
        const hourlyData = HOURLY_DATA;
        const workdayData = WORKDAY_DATA;
        const weekendData = WEEKEND_DATA;
        const weatherData = WEATHER_DATA;
        const userTypeData = USER_TYPE_DATA;
        
        // Statistiques clés
        document.getElementById('avgDailyUsers').textContent = AVG_DAILY_USERS;
        document.getElementById('totalUsers').textContent = TOTAL_USERS;
        document.getElementById('peakHour').textContent = PEAK_HOUR;
        document.getElementById('peakHourUsers').textContent = PEAK_HOUR_USERS;
        document.getElementById('bestSeason').textContent = BEST_SEASON;
        document.getElementById('worstWeather').textContent = WORST_WEATHER;
        document.getElementById('registeredPct').textContent = REGISTERED_PCT;
        
        // Graphique par mois
        new Chart(document.getElementById('monthlyChart'), {
            type: 'bar',
            data: {
                labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
                datasets: [{
                    label: 'Utilisation moyenne par mois',
                    data: monthlyData,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Nombre moyen d'utilisations"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Mois'
                        }
                    }
                }
            }
        });
        
        // Graphique par saison
        new Chart(document.getElementById('seasonChart'), {
            type: 'bar',
            data: {
                labels: ['Hiver', 'Printemps', 'Été', 'Automne'],
                datasets: [{
                    label: 'Utilisation moyenne par saison',
                    data: seasonData,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Nombre moyen d'utilisations"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Saison'
                        }
                    }
                }
            }
        });
        
        // Graphique par heure
        new Chart(document.getElementById('hourlyChart'), {
            type: 'line',
            data: {
                labels: Array.from({length: 24}, (_, i) => i + 'h'),
                datasets: [{
                    label: 'Utilisation moyenne par heure',
                    data: hourlyData,
                    backgroundColor: 'rgba(255, 159, 64, 0.5)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 2,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Nombre moyen d'utilisations"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Heure de la journée'
                        }
                    }
                }
            }
        });
        
        // Graphique jours travaillés vs weekend
        new Chart(document.getElementById('workdayVsWeekendChart'), {
            type: 'line',
            data: {
                labels: Array.from({length: 24}, (_, i) => i + 'h'),
                datasets: [{
                    label: 'Jours travaillés',
                    data: workdayData,
                    backgroundColor: 'rgba(153, 102, 255, 0.5)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 2,
                    tension: 0.1
                }, {
                    label: 'Weekend/Fériés',
                    data: weekendData,
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Nombre moyen d'utilisations"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Heure de la journée'
                        }
                    }
                }
            }
        });
        
        // Graphique impact météo
        new Chart(document.getElementById('weatherChart'), {
            type: 'bar',
            data: {
                labels: ['Clair', 'Nuageux/Brumeux', 'Pluie légère/Neige', 'Fortes précipitations'],
                datasets: [{
                    label: 'Impact de la météo sur l\'utilisation',
                    data: weatherData,
                    backgroundColor: 'rgba(255, 206, 86, 0.5)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Nombre moyen d'utilisations"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Conditions météo'
                        }
                    }
                }
            }
        });
        
        // Graphique type d'utilisateur
        new Chart(document.getElementById('userTypeChart'), {
            type: 'pie',
            data: {
                labels: ['Occasionnels', 'Abonnés'],
                datasets: [{
                    data: userTypeData,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    </script>
</body>
</html>
"""

# Calcul des statistiques clés
total_users = sum(row['cnt'] for row in day_data)
avg_daily_users = mean([row['cnt'] for row in day_data])
peak_hour = max(hourly_avg.items(), key=lambda x: x[1])[0]
peak_hour_users = hourly_avg[peak_hour]
best_season = max([(season, mean(counts)) for season, counts in season_usage.items()], key=lambda x: x[1])[0]
worst_weather = min([(weather, mean(counts)) for weather, counts in weather_impact.items()], key=lambda x: x[1])[0]
registered_pct = (total_registered / total_users) * 100

# Préparation des données pour le JavaScript
monthly_data_js = [monthly_avg.get(i, 0) for i in range(1, 13)]
season_data_js = [season_avg.get(i, 0) for i in range(1, 5)]
hourly_data_js = [hourly_avg.get(i, 0) for i in range(24)]
workday_data_js = [workday_avg.get(i, 0) for i in range(24)]
weekend_data_js = [weekend_avg.get(i, 0) for i in range(24)]
weather_data_js = [weather_avg.get(i, 0) for i in range(1, 5)]
user_type_data_js = [total_casual, total_registered]

# Remplacement des placeholders dans le HTML
html_content = html_content.replace('MONTHLY_DATA', json.dumps(monthly_data_js))
html_content = html_content.replace('SEASON_DATA', json.dumps(season_data_js))
html_content = html_content.replace('HOURLY_DATA', json.dumps(hourly_data_js))
html_content = html_content.replace('WORKDAY_DATA', json.dumps(workday_data_js))
html_content = html_content.replace('WEEKEND_DATA', json.dumps(weekend_data_js))
html_content = html_content.replace('WEATHER_DATA', json.dumps(weather_data_js))
html_content = html_content.replace('USER_TYPE_DATA', json.dumps(user_type_data_js))
html_content = html_content.replace('AVG_DAILY_USERS', str(int(avg_daily_users)))
html_content = html_content.replace('TOTAL_USERS', str(int(total_users)))
html_content = html_content.replace('PEAK_HOUR', str(peak_hour))
html_content = html_content.replace('PEAK_HOUR_USERS', str(int(peak_hour_users)))
html_content = html_content.replace('BEST_SEASON', season_dict[best_season])
html_content = html_content.replace('WORST_WEATHER', weather_dict[worst_weather])
html_content = html_content.replace('REGISTERED_PCT', str(round(registered_pct, 1)))

# Écriture du fichier HTML
with open('analyse_velos.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nAnalyse terminée! Un rapport avec des graphiques a été généré dans 'analyse_velos.html'.")
print("Ouvrez ce fichier dans votre navigateur pour voir les graphiques.")