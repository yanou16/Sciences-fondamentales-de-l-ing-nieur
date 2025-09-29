import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import sys

# Fonction pour gérer les erreurs
def main():
    try:
        # Créer un dossier pour les graphiques d'anomalies
        if not os.path.exists('anomalies'):
            os.makedirs('anomalies')
            print("Dossier 'anomalies' créé avec succès")

        # Charger les données
        print("Chargement des données...")
        if not os.path.exists("server_usage_data.csv"):
            print("ERREUR: Le fichier 'server_usage_data.csv' n'existe pas!")
            return
            
        df = pd.read_csv("server_usage_data.csv")
        print(f"Données chargées avec succès: {len(df)} lignes")
        
        df['Time'] = pd.to_datetime(df['Time'])
        df['Hour'] = df['Time'].dt.hour
        df['Date'] = df['Time'].dt.date
        df['Day_of_week'] = df['Time'].dt.dayofweek
        df['Is_weekend'] = df['Day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

        print("Statistiques de base:")
        print(df[['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']].describe())

        # Calculer les Z-scores pour chaque métrique
        z_score_factor = 2  # Facteur Z-score pour définir les seuils (2 écarts-types)
        
        seuils = {}
        for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
            mean = df[metrique].mean()
            std = df[metrique].std()
            seuils[metrique] = mean + z_score_factor * std
            
        # 1. MÉTHODE PAR SEUIL (basée sur Z-score)
        print("\n1. Détection d'anomalies par SEUIL (basé sur Z-score)")
        
        anomalies_seuil = {}
        for metrique in seuils:
            anomalies_seuil[metrique] = df[df[metrique] > seuils[metrique]]
            print(f"Anomalies {metrique} (seuil {seuils[metrique]:.2f}, Z-score = {z_score_factor}): {len(anomalies_seuil[metrique])} détectées")
            
            # Visualiser les anomalies par seuil
            plt.figure(figsize=(12, 6))
            plt.plot(df['Time'], df[metrique], label=f'{metrique}', color='blue', alpha=0.5)
            plt.scatter(anomalies_seuil[metrique]['Time'], anomalies_seuil[metrique][metrique], 
                        color='red', label=f'Anomalies {metrique}', s=50)
            plt.axhline(y=seuils[metrique], color='r', linestyle='--', 
                       label=f"Seuil Z-score ({seuils[metrique]:.2f}, {z_score_factor} écarts-types)")
            plt.title(f'Détection d\'anomalies par seuil (Z-score) - {metrique}')
            plt.xlabel('Date et heure')
            plt.ylabel(metrique)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'anomalies/anomalies_seuil_{metrique}.png')
            plt.close()
            print(f"Graphique sauvegardé: anomalies/anomalies_seuil_{metrique}.png")

        # 2. MÉTHODE PAR IQR
        print("\n2. Détection d'anomalies par IQR")
        def detecter_anomalies_iqr(serie, multiplicateur=1.5):
            Q1 = serie.quantile(0.25)
            Q3 = serie.quantile(0.75)
            IQR = Q3 - Q1
            
            limite_inf = Q1 - multiplicateur * IQR
            limite_sup = Q3 + multiplicateur * IQR
            
            anomalies = serie[(serie < limite_inf) | (serie > limite_sup)]
            return anomalies, limite_inf, limite_sup

        anomalies_iqr = {}
        limites_iqr = {}

        for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
            anomalies_indices, limite_inf, limite_sup = detecter_anomalies_iqr(df[metrique])
            anomalies_iqr[metrique] = df.loc[anomalies_indices.index]
            limites_iqr[metrique] = (limite_inf, limite_sup)
            
            print(f"Anomalies {metrique} (IQR): {len(anomalies_iqr[metrique])} détectées")
            print(f"Limites IQR pour {metrique}: {limite_inf:.2f} à {limite_sup:.2f}")
            
            # Visualiser les anomalies IQR
            plt.figure(figsize=(12, 6))
            plt.plot(df['Time'], df[metrique], label=f'{metrique}', color='blue', alpha=0.5)
            plt.scatter(anomalies_iqr[metrique]['Time'], anomalies_iqr[metrique][metrique], 
                        color='orange', label=f'Anomalies {metrique} (IQR)', s=50)
            plt.axhline(y=limite_sup, color='orange', linestyle='--', label=f"Limite sup. IQR ({limite_sup:.2f})")
            plt.axhline(y=limite_inf, color='orange', linestyle='--', label=f"Limite inf. IQR ({limite_inf:.2f})")
            plt.title(f'Détection d\'anomalies par IQR - {metrique}')
            plt.xlabel('Date et heure')
            plt.ylabel(metrique)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'anomalies/anomalies_iqr_{metrique}.png')
            plt.close()
            print(f"Graphique sauvegardé: anomalies/anomalies_iqr_{metrique}.png")

        # 3. MÉTHODE PAR Z-SCORE
        print("\n3. Détection d'anomalies par Z-SCORE")
        def detecter_anomalies_zscore(serie, seuil=3):
            mean = serie.mean()
            std = serie.std()
            z_scores = (serie - mean) / std
            
            anomalies = serie[abs(z_scores) > seuil]
            return anomalies, mean - seuil * std, mean + seuil * std

        anomalies_zscore = {}
        limites_zscore = {}

        for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
            anomalies_indices, limite_inf, limite_sup = detecter_anomalies_zscore(df[metrique])
            anomalies_zscore[metrique] = df.loc[anomalies_indices.index]
            limites_zscore[metrique] = (limite_inf, limite_sup)
            
            print(f"Anomalies {metrique} (Z-score): {len(anomalies_zscore[metrique])} détectées")
            print(f"Limites Z-score pour {metrique}: {limite_inf:.2f} à {limite_sup:.2f}")
            
            # Visualiser les anomalies Z-score
            plt.figure(figsize=(12, 6))
            plt.plot(df['Time'], df[metrique], label=f'{metrique}', color='blue', alpha=0.5)
            plt.scatter(anomalies_zscore[metrique]['Time'], anomalies_zscore[metrique][metrique], 
                        color='green', label=f'Anomalies {metrique} (Z-score)', s=50)
            plt.axhline(y=limite_sup, color='green', linestyle='--', label=f"Limite sup. Z-score ({limite_sup:.2f})")
            plt.axhline(y=limite_inf, color='green', linestyle='--', label=f"Limite inf. Z-score ({limite_inf:.2f})")
            plt.title(f'Détection d\'anomalies par Z-score - {metrique}')
            plt.xlabel('Date et heure')
            plt.ylabel(metrique)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'anomalies/anomalies_zscore_{metrique}.png')
            plt.close()
            print(f"Graphique sauvegardé: anomalies/anomalies_zscore_{metrique}.png")

        # 4. GRAPHIQUE COMPARATIF DES MÉTHODES
        print("\n4. Création du graphique comparatif des méthodes")
        for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
            plt.figure(figsize=(15, 8))
            
            # Tracer les données originales
            plt.plot(df['Time'], df[metrique], label=f'{metrique}', color='blue', alpha=0.3)
            
            # Tracer les anomalies détectées par chaque méthode
            plt.scatter(anomalies_seuil[metrique]['Time'], anomalies_seuil[metrique][metrique], 
                        color='red', label=f'Anomalies (Seuil Z-score)', s=50, alpha=0.7)
            plt.scatter(anomalies_iqr[metrique]['Time'], anomalies_iqr[metrique][metrique], 
                        color='orange', label=f'Anomalies (IQR)', s=50, alpha=0.7)
            plt.scatter(anomalies_zscore[metrique]['Time'], anomalies_zscore[metrique][metrique], 
                        color='green', label=f'Anomalies (Z-score)', s=50, alpha=0.7)
            
            # Tracer les limites
            plt.axhline(y=seuils[metrique], color='red', linestyle='--', 
                       label=f"Seuil Z-score ({seuils[metrique]:.2f}, {z_score_factor} écarts-types)")
            plt.axhline(y=limites_iqr[metrique][1], color='orange', linestyle='--', label=f"Limite sup. IQR ({limites_iqr[metrique][1]:.2f})")
            plt.axhline(y=limites_zscore[metrique][1], color='green', linestyle='--', label=f"Limite sup. Z-score ({limites_zscore[metrique][1]:.2f})")
            
            plt.title(f'Comparaison des méthodes de détection d\'anomalies - {metrique}')
            plt.xlabel('Date et heure')
            plt.ylabel(metrique)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'anomalies/comparaison_methodes_{metrique}.png')
            plt.close()
            print(f"Graphique comparatif sauvegardé: anomalies/comparaison_methodes_{metrique}.png")

        # 5. GÉNÉRER UN RAPPORT D'ANOMALIES
        print("\n5. Génération du rapport d'anomalies")
        with open('rapport_anomalies.txt', 'w') as f:
            f.write("RAPPORT DE DÉTECTION D'ANOMALIES\n")
            f.write("===============================\n\n")
            f.write(f"Période analysée: {df['Time'].min()} à {df['Time'].max()}\n")
            f.write(f"Nombre total de mesures: {len(df)}\n\n")
            
            f.write("1. MÉTHODE PAR SEUIL (basée sur Z-score)\n")
            f.write(f"Facteur Z-score utilisé: {z_score_factor} écarts-types\n")
            for metrique in seuils:
                f.write(f"Anomalies {metrique} (seuil {seuils[metrique]:.2f}): {len(anomalies_seuil[metrique])} détectées\n")
                if len(anomalies_seuil[metrique]) > 0:
                    f.write(f"  - Valeur maximale: {anomalies_seuil[metrique][metrique].max():.2f} à {anomalies_seuil[metrique]['Time'].iloc[anomalies_seuil[metrique][metrique].argmax()]}\n")
            f.write("\n")
            
            f.write("2. MÉTHODE PAR IQR\n")
            for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
                f.write(f"Anomalies {metrique}: {len(anomalies_iqr[metrique])} détectées\n")
                f.write(f"Limites IQR pour {metrique}: {limites_iqr[metrique][0]:.2f} à {limites_iqr[metrique][1]:.2f}\n")
            f.write("\n")
            
            f.write("3. MÉTHODE PAR Z-SCORE\n")
            for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
                f.write(f"Anomalies {metrique}: {len(anomalies_zscore[metrique])} détectées\n")
                f.write(f"Limites Z-score pour {metrique}: {limites_zscore[metrique][0]:.2f} à {limites_zscore[metrique][1]:.2f}\n")
            f.write("\n")
            
            f.write("COMPARAISON DES MÉTHODES\n")
            f.write("=======================\n\n")
            
            f.write("Nombre d'anomalies détectées par méthode:\n")
            f.write("| Métrique       | Seuil (Z-score) | IQR    | Z-score |\n")
            f.write("|----------------|-----------------|--------|--------|\n")
            
            for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
                f.write(f"| {metrique:<14} | {len(anomalies_seuil[metrique]):<15} | {len(anomalies_iqr[metrique]):<6} | {len(anomalies_zscore[metrique]):<6} |\n")
            
            f.write("\nRECOMMANDATIONS\n")
            f.write("==============\n\n")
            
            # Déterminer la méthode la plus appropriée pour chaque métrique
            for metrique in ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']:
                f.write(f"Pour {metrique}:\n")
                
                # Compter les anomalies par méthode
                count_seuil = len(anomalies_seuil[metrique])
                count_iqr = len(anomalies_iqr[metrique])
                count_zscore = len(anomalies_zscore[metrique])
                
                if count_seuil == 0 and count_iqr == 0 and count_zscore == 0:
                    f.write("  - Aucune anomalie détectée par les trois méthodes. Les données semblent normales.\n")
                else:
                    # Recommandation basée sur le nombre d'anomalies
                    if count_seuil > 0 and (count_seuil < count_iqr or count_iqr == 0) and (count_seuil < count_zscore or count_zscore == 0):
                        f.write(f"  - La méthode par seuil (Z-score {z_score_factor}) semble la plus appropriée avec {count_seuil} anomalies détectées.\n")
                    elif count_iqr > 0 and (count_iqr < count_seuil or count_seuil == 0) and (count_iqr < count_zscore or count_zscore == 0):
                        f.write(f"  - La méthode IQR semble la plus appropriée avec {count_iqr} anomalies détectées.\n")
                    elif count_zscore > 0:
                        f.write(f"  - La méthode Z-score semble la plus appropriée avec {count_zscore} anomalies détectées.\n")
                    else:
                        # Si plusieurs méthodes détectent le même nombre d'anomalies
                        f.write("  - Plusieurs méthodes détectent un nombre similaire d'anomalies. Une analyse plus approfondie est recommandée.\n")
            
            f.write("\nCONCLUSION\n")
            f.write("=========\n\n")
            f.write("Cette analyse a permis de détecter des anomalies dans les données du serveur en utilisant trois méthodes différentes.\n")
            f.write("La méthode par seuil utilisant le Z-score offre un bon équilibre entre sensibilité et spécificité.\n")
            f.write("Pour une surveillance en temps réel, nous recommandons d'utiliser une combinaison de ces méthodes\n")
            f.write("afin de détecter efficacement les anomalies tout en minimisant les faux positifs.\n")
            
        print(f"Rapport d'anomalies généré: rapport_anomalies.txt")
        
        print("\nAnalyse terminée! Les résultats ont été enregistrés dans:")
        print("- Dossier 'anomalies/' pour les graphiques")
        print("- Fichier 'rapport_anomalies.txt' pour le rapport détaillé")
        
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")
        print(f"Détails: {sys.exc_info()}")

if __name__ == "__main__":
    main()