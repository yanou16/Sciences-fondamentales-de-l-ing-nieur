# Projet d'Analyse de Données Serveur

Ce projet permet d'analyser les données d'utilisation d'un serveur, de générer des visualisations et de détecter des anomalies dans les métriques clés.

## Contenu du Projet

### Scripts Principaux
- `test.py` : Script principal d'analyse des données serveur
- `graphiques_serveur.py` : Génération de graphiques pour visualiser les données
- `detection_anomalies.py` : Détection d'anomalies avec trois méthodes différentes

### Données
- `server_usage_data.csv` : Données brutes d'utilisation du serveur
- Fichiers triés : 
  - `serveur_tri_cpu.csv`
  - `serveur_tri_temperature.csv`
  - `serveur_tri_charge_combinee.csv`

### Rapports
- `rapport_analyse_serveur.txt` : Rapport d'analyse général
- `rapport_analyse_serveur_detaille.txt` : Rapport détaillé
- `rapport_anomalies.txt` : Rapport sur les anomalies détectées

### Visualisations
- Dossier `graphiques/` : Visualisations générales des données
- Dossier `anomalies/` : Visualisations des anomalies détectées

## Fonctionnalités

### 1. Analyse des Données (`test.py`)
- Chargement et nettoyage des données
- Statistiques descriptives
- Analyse temporelle (heures, jours, semaine/weekend)
- Identification des pics d'utilisation
- Analyse de corrélation entre métriques
- Tri et sauvegarde des données

### 2. Visualisation des Données (`graphiques_serveur.py`)
- Évolution temporelle des métriques
- Heatmap de corrélation
- Utilisation moyenne par heure
- Comparaison semaine vs weekend
- Distribution des métriques
- Corrélation réseau-température
- Boxplot d'utilisation CPU par jour

### 3. Détection d'Anomalies (`detection_anomalies.py`)
Implémentation de trois méthodes de détection :

- **Méthode par Seuil** : Utilise le Z-score pour définir des seuils dynamiques
  - Seuil = moyenne + (facteur Z-score × écart-type)
  
- **Méthode IQR (Interquartile Range)** :
  - Limites = Q1 - 1.5*IQR et Q3 + 1.5*IQR
  - Détecte les valeurs en dehors de ces limites
  
- **Méthode Z-score** :
  - Calcule le Z-score = (valeur - moyenne) / écart-type
  - Détecte les valeurs avec |Z-score| > 3

## Comment Utiliser

### Prérequis
- Python 3.x
- Bibliothèques : pandas, matplotlib, numpy, seaborn

### Exécution des Scripts

1. **Analyse des données** :
```bash
python test.py
```

2. **Génération des graphiques** :
```bash
python graphiques_serveur.py
```

3. **Détection des anomalies** :
```bash
python detection_anomalies.py
```

## Résultats

### Statistiques Clés
- Utilisation CPU moyenne : 41.41%
- Utilisation mémoire moyenne : 7.20%
- Utilisation réseau moyenne : 115.01%
- Température moyenne : 41.37°C

### Corrélations Importantes
- Forte corrélation (0.94) entre utilisation réseau et température
- Corrélation modérée (0.60) entre utilisation CPU et température
- Corrélation modérée (0.43) entre utilisation CPU et mémoire

### Anomalies
Le script de détection d'anomalies identifie les valeurs anormales selon trois méthodes et génère des visualisations comparatives pour aider à choisir la méthode la plus appropriée pour chaque métrique.

## Personnalisation

Pour ajuster les seuils de détection d'anomalies, modifiez les paramètres suivants dans `detection_anomalies.py` :
- Méthode par seuil : variable `z_score_factor` (par défaut : 2)
- Méthode IQR : paramètre `multiplicateur` (par défaut : 1.5)
- Méthode Z-score : paramètre `seuil` (par défaut : 3)