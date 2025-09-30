# -*- coding: utf-8 -*-
# Démo Cryptographie : César + RSA
# Rayan 2025

# --- Fonction César ---
def cesar_decrypt(text, shift=4):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        elif char.isdigit():
            result += str((int(char) - shift) % 10)
        else:
            result += char
    return result

# --- Fonction RSA ---
def rsa_decrypt(cipher_list, d, n):
    decrypted = ""
    for c in cipher_list:
        m = pow(c, d, n)   # déchiffrement RSA
        decrypted += chr(m)
    return decrypted


if __name__ == "__main__":
    print("=== Démo Cryptographie ===")
    print("1. Déchiffrement César")
    print("2. Déchiffrement RSA")
    choix = input("Choisissez une option (1 ou 2) : ")

    if choix == "1":
        texte = input("Entrez le texte chiffré (ex: 9153787770964) : ")
        shift = int(input("Décalage (ex: 4) : "))
        print("Texte déchiffré :", cesar_decrypt(texte, shift))

    elif choix == "2":
        n = int(input("Entrez N (ex: 3233) : "))
        d = int(input("Entrez d (ex: 2753) : "))
        cipher = input("Entrez la liste de nombres séparés par des virgules : ")
        cipher_list = [int(x.strip()) for x in cipher.split(",")]
        print("Message déchiffré :", rsa_decrypt(cipher_list, d, n))

    else:
        print("Choix invalide !")
