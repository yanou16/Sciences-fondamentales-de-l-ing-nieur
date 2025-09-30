import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Chemin vers le dossier contenant les fichiers de données
DATA_DIR = "GreenIT_data"

def extract_number(filename):
    """Extrait le nombre du nom de fichier data_list_X.csv"""
    match = re.search(r'data_list_(\d+)\.csv', filename)
    if match:
        return int(match.group(1))
    return 0

def load_data(file_path):
    """Charge les données depuis un fichier CSV"""
    try:
        # Ajouter header=0 pour traiter la première ligne comme en-tête
        df = pd.read_csv(file_path, header=0)
        # Convertir en liste d'entiers
        return df["Value"].astype(int).tolist()  # Utiliser le nom de colonne "Value"
    except Exception as e:
        print(f"Erreur lors du chargement de {file_path}: {e}")
        return []

# Implémentation des trois algorithmes pour résoudre le problème Two Sum

def two_sum_brute_force(nums, target=0):
    """
    Force brute - O(n²)
    Trouve deux nombres dans la liste qui s'additionnent pour donner la cible
    """
    n = len(nums)
    # Forcer le parcours complet pour montrer la vraie complexité O(n²)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None

def two_sum_sorting(nums, target=0):
    """
    Tri + deux pointeurs - O(n log n)
    Trie la liste puis utilise deux pointeurs pour trouver la paire
    """
    # Créer une liste de tuples (valeur, index)
    indexed_nums = [(nums[i], i) for i in range(len(nums))]
    # Trier par valeur
    indexed_nums.sort()
    
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = indexed_nums[left][0] + indexed_nums[right][0]
        if current_sum == target:
            return [indexed_nums[left][1], indexed_nums[right][1]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None

def two_sum_hash_table(nums, target=0):
    """
    Table de hachage - O(n)
    Utilise un dictionnaire pour stocker les valeurs déjà vues
    """
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return None

def measure_execution_time(algorithm, data, target=0):
    """Mesure le temps d'exécution d'un algorithme"""
    start_time = time.perf_counter()
    result = algorithm(data, target)
    end_time = time.perf_counter()
    return end_time - start_time

def estimate_brute_force_time(data_size, reference_size, reference_time):
    """
    Estime le temps d'exécution de la force brute pour une taille donnée
    en utilisant une formule quadratique (O(n²))
    """
    if reference_time is None or reference_size == 0:
        return None
    # Formule quadratique: temps ~ (taille²/référence_taille²) * référence_temps
    return (data_size**2 / reference_size**2) * reference_time

def main():
    # Récupérer tous les fichiers CSV dans le dossier
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and f.startswith('data_list_')]
    
    # Trier les fichiers par taille
    csv_files.sort(key=extract_number)
    
    # Stocker les résultats
    results = {
        'taille_donnees': [],
        'temps_brute': [],
        'temps_tri_pointeurs': [],
        'temps_hachage': []
    }
    
    print("Analyse des performances des algorithmes Two Sum...")
    
    # Variables pour l'estimation de la force brute
    max_brute_force_size = 10000  # Taille maximale pour la force brute réelle (réduite pour montrer la différence)
    reference_size = None
    reference_time = None
    
    # Pour chaque fichier
    for file in csv_files:
        file_path = os.path.join(DATA_DIR, file)
        data_size = extract_number(file)
        
        # Charger les données
        print(f"Traitement du fichier {file} (taille: {data_size})...")
        data = load_data(file_path)
        
        if not data:
            print(f"Données vides pour {file}, on passe au fichier suivant")
            continue
            
        # Définir une cible qui n'existe pas pour forcer le pire cas
        # On utilise une valeur qui n'est probablement pas dans le tableau
        target = -999999
        
        # Mesurer ou estimer le temps pour la force brute
        if data_size <= max_brute_force_size:
            print("  Mesure du temps pour la force brute...")
            brute_time = measure_execution_time(two_sum_brute_force, data, target)
            
            # Stocker la référence pour l'estimation future
            if reference_size is None or data_size > reference_size:
                reference_size = data_size
                reference_time = brute_time
        else:
            print(f"  Estimation du temps pour la force brute (taille {data_size} > {max_brute_force_size})...")
            brute_time = estimate_brute_force_time(data_size, reference_size, reference_time)
            print(f"  Temps estimé: {brute_time} secondes (basé sur la référence: {reference_size} éléments en {reference_time} secondes)")
        
        print("  Mesure du temps pour tri + pointeurs...")
        sorting_time = measure_execution_time(two_sum_sorting, data, target)
        
        print("  Mesure du temps pour la table de hachage...")
        hash_time = measure_execution_time(two_sum_hash_table, data, target)
        
        # Stocker les résultats
        results['taille_donnees'].append(data_size)
        results['temps_brute'].append(brute_time)
        results['temps_tri_pointeurs'].append(sorting_time)
        results['temps_hachage'].append(hash_time)
        
        print(f"  Résultats pour {file}:")
        print(f"    Force brute: {brute_time} secondes {'(estimé)' if data_size > max_brute_force_size else ''}")
        print(f"    Tri + pointeurs: {sorting_time} secondes")
        print(f"    Table de hachage: {hash_time} secondes")
        print()
    
    # Créer un DataFrame avec les résultats
    results_df = pd.DataFrame(results)
    
    # Afficher le tableau des résultats
    print("\nRésultats complets:")
    print(results_df)
    
    # Sauvegarder les résultats dans un CSV
    try:
        results_df.to_csv('resultats_two_sum.csv', index=False)
        print("Résultats sauvegardés dans 'resultats_two_sum.csv'")
    except PermissionError:
        print("Erreur de permission: Impossible d'écrire le fichier resultats_two_sum.csv")
        print("Essai avec un autre nom de fichier...")
        try:
            results_df.to_csv('resultats_two_sum_new.csv', index=False)
            print("Résultats sauvegardés dans 'resultats_two_sum_new.csv'")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des résultats: {e}")
    
    # Tracer le graphique seulement s'il y a des données
    if len(results['taille_donnees']) > 0:
        plt.figure(figsize=(12, 8))
        
        # Tracer tous les résultats, y compris les estimations pour la force brute
        plt.plot(results['taille_donnees'], results['temps_brute'], 'o-', color='red', label='Force brute O(n²)')
        plt.plot(results['taille_donnees'], results['temps_tri_pointeurs'], 'o-', color='blue', label='Tri + pointeurs O(n log n)')
        plt.plot(results['taille_donnees'], results['temps_hachage'], 'o-', color='green', label='Table de hachage O(n)')
        
        plt.xlabel('Taille des données')
        plt.ylabel('Temps d\'exécution (secondes)')
        plt.title('Comparaison des algorithmes pour le problème Two Sum')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # Échelle logarithmique pour mieux visualiser
        plt.yscale('log')  # Échelle logarithmique pour mieux visualiser
        
        # Ajouter une annotation pour indiquer les valeurs estimées
        plt.axvline(x=max_brute_force_size, color='gray', linestyle='--')
        plt.text(max_brute_force_size*1.1, plt.ylim()[0]*2, 
                 f'Valeurs estimées\npour la force brute\nau-delà de {max_brute_force_size}',
                 color='gray')
        
        # Sauvegarder le graphique
        try:
            plt.savefig('comparaison_algos.png', dpi=300, bbox_inches='tight')
            print("Graphique sauvegardé dans 'comparaison_algos.png'")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du graphique: {e}")
        
        # Afficher le graphique
        try:
            plt.show()
        except Exception as e:
            print(f"Erreur lors de l'affichage du graphique: {e}")

if __name__ == "__main__":
    main()