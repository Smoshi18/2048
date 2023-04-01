import time
def palindromes_maximum(nb_chiffres:int)->int:
    """retourne le palindrome le plus grand d'une multiplication de deux nombres de nb_chiffres chiffres
    
    entrée :
        nb_chiffres : int
            correspond au nombre de chiffres des deux nombres à multiplier
    
    sortie :
        return : int
            renvoie le palindrome le plus grand
    """
    
    n = 0.1 #On détermine la valeur finale, qui est le plus petit nombre avec nb_chiffres chiffres.
    max = 1 #Représente le nombre max de nb_chiffres chiffres.
    for i in range(nb_chiffres):
        n *= 10
        max *= 10
    max-=1 #On retire 1 afin d'avoir le nombre le plus grand avec nb_chiffres chiffre. exemple : 1000-1 = 999.
    n = int(n) #On évite de se retrouver avec un reste si nb_chiffres = 0

    palindrome_max = 0 #Représente le palindrome le plus grand. Il est initialisé à 0.

    #On décrémente afin de pouvoir multiplier les plus grands nombres au début et ainsi trouver le plus rapidement palindrome_max
    for i in range(max,n,-1):
        for j in range(i, n, -1):
            produit = j*i
            #Si le produit est inférieur a palindrome_max, alors on n'a pas besoin de vérifier si c'est un palindrome.
            #On passe alors au nombre suivant en cassant la boucle for en cours.
            if produit<palindrome_max:
                break
            #Si le produit est supérieur a palindrome_max, alors on vérifie si c'est lui aussi un palindrome.
            #Si c'est le cas, alors on remplace l'ancien valeur de palindrome_max par le produit.
            if est_un_palindrome(produit):
                palindrome_max = produit
    return palindrome_max

def liste_palindromes(nb_chiffres:int)->list:
    """renvoie la liste des palindromes numériques à nb_chiffres chiffres

    entrée :
        nb_chiffres : entier
            correspond au nombre de chiffres des deux nombres à multiplier
    
    sortie :
        return : liste
            renvoie une liste contenant tous les palindromes obtenues par la multiplication de deux nombres de nb_chiffres chiffres
    """
    #On utilise un set au lieu de liste afin d'éviter les doublons.
    liste_des_palindromes = set()
     
    n = 0.1 #On détermine la valeur initiale, qui est le plus petit nombre avec nb_chiffres chiffres.
    max = 1 #Représente le nombre à ne pas dépasser pour conserver nb_chiffres chiffre.
    for i in range(nb_chiffres):
        n *= 10
        max *= 10
    n = int(n)

    #On calcule toutes les combinaisons possibles entre deux nombres de nb_chiffres chiffres et on ajoute dans liste_des_palindromes si on obtient un palindrome.
    for i in range(n, max):
        #Pour optimiser l'algorithme, on ne part pas de 1 mais de i car sinon on a des répétitions du type 18*23 et 23*18.
        #Le nombre d'opération est donc réduit.
        for j in range(i, max):
            produit = i*j
            #Si le produit est un paladrome alors on l'ajoute dans liste_des_palindromes.
            if est_un_palindrome(produit):
                liste_des_palindromes.add(produit)
    #on retourne le set en une liste triée grâce à sorted().
    return sorted(liste_des_palindromes)

def est_un_palindrome(n:int)->bool:
    """Vérifie si un nombre est un palindrome.

    entrée :
        n : entier
            nombre qu'on vérifie si il est un palindrome
    
    sortie :
        return : booléen
            retourne True si le nombre est un booléen, sinon False
    
    """
    #On convertit le nombre n en une chaine de caractère.
    n = str(n)

    #On récupère l'indice du premier et du dernier caractère de la chaine de caratère.
    p1 = 0
    p2 = len(n)-1 #On retire 1 car l'indice commence à 0, ce qui fait que le dernier indice est à len(n)-1.
    
    #On vérifie que les caractères de par et d'autre du centre sont symétrique.
    #On continue l'opération de comparaison des caractères tant que l'indice p1 est inférieur à l'indice p2.
    #Si p1 est supérieur à p2, alors on a atteint le centre de la chaine de caractère.
    while p1<p2:
        #Si le caractère à p1 est différent de celui à p2 alors le nombre n'est pas un palindrome.
        if not n[p1] == n[p2]:
            return False
        #on incrémente de 1 p1 pour le faire avancer dans la chaine
        p1+=1
        #on decrémente de 1 p2 pour le faire reculer dans la chaine
        p2-=1
    return True

def nombre()->int:
    """Demande à l'utilisateur un nombre valide
    entrée:
        void
    sortie:
        return : str
            retourne le nombre"""
    valid = False
    while(not valid):
                nb_chiffres = str(input("\033[96mentrer un nombre de chiffre :\033[0m "))
                if nb_chiffres.isdigit():
                    valid = True
    return int(nb_chiffres)

def __main__():
    #On demande le nombre de chiffres qu'on souhaite avoir pour les deux nombres à multiplier.
    quitter = False
    
    while not quitter:
        #On demande à l'utilisateur ce qu'il souhaite faire
        choix = input("\033[96mque souhaitez-vous faire ?\n 1 pour afficher le palindrome le plus grand\n 2 pour afficher la liste des palindromes\n 3 pour quitter\n\033[0m ")
        if choix == "1":
            nb_chiffres = nombre()
            #On affiche le palindrome le plus grand
            print("\033[92m")
            print(palindromes_maximum(nb_chiffres))
            print("\033[0m")
        elif choix =="2":
            nb_chiffres = nombre()
            print("\033[92m")
            print(liste_palindromes(nb_chiffres))
            print("\033[0m")
        elif choix == "3":
            quitter = True
        else:
            print("\033[96mErreur : commande non valide\033[0m")

if __name__ == "__main__":
    __main__()