import random
import curses
import json

def initialiser_la_grille(size):
    """
    Initialise la grille du jeu avec la taille donnée.
    
    Args:
        size (int): la taille de la grille (nombre de lignes et de colonnes)
        
    Returns:
        list: une liste de listes représentant la grille avec des zéros
    """
    # Crée une liste vide qui va contenir les lignes de la grille
    grid = []

    # Boucle pour chaque ligne de la grille
    for _ in range(size):
        # Crée une liste vide pour la ligne
        row = []

        # Boucle pour chaque colonne de la ligne
        for _ in range(size):
            # Ajoute un zéro à la fin de la ligne
            row.append(0)

        # Ajoute la ligne complète de zéros à la grille
        grid.append(row)

    # Retourne la grille remplie de zéros
    return grid

def ajout_nombre(grid, probabilité):
    """
    Ajoute un nouveau nombre (2 ou 4) à une position vide aléatoire dans la grille.
    
    Args:
        grid (list): la grille actuelle du jeu
        
    Returns:
        list: la grille avec un nouveau nombre ajouté à une position aléatoire
    """

    # Crée une liste vide pour stocker les positions des cases vides
    empty_tiles = []

    # Parcourt les lignes de la grille
    for i in range(len(grid)):
        # Parcourt les colonnes de la grille
        for j in range(len(grid)):
            # Vérifie si la case est vide (contient 0)
            if grid[i][j] == 0:
                # Ajoute les coordonnées (i, j) de la case vide à la liste empty_tiles
                empty_tiles.append((i, j))

    # Choisis une case vide aléatoirement parmi la liste empty_tiles
    i, j = random.choice(empty_tiles)

    # Génère un nombre aléatoire entre 0 et 1 et ajoute 2 à la case si le nombre est inférieur à probabilité, sinon ajoute 4
    if random.random() < probabilité:
        grid[i][j] = 2 
    else:
        grid[i][j] = 4
    # Retourne la grille avec le nouveau nombre ajouté
    return grid

def peut_bouger(grid):
    """
    Vérifie si un mouvement est possible dans la grille.
    
    Args:
        grid (list): la grille actuelle du jeu
        
    Returns:
        bool: True si un mouvement est possible, sinon False
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                return True
            if i > 0 and grid[i][j] == grid[i - 1][j]:
                return True
            if j > 0 and grid[i][j] == grid[i][j - 1]:
                return True
            if i < len(grid) - 1 and grid[i][j] == grid[i + 1][j]:  # Vérifie la case en bas
                return True
            if j < len(grid) - 1 and grid[i][j] == grid[i][j + 1]:  # Vérifie la case à droite
                return True
    return False

def compresser(grid):
    """
    compresser la grille en supprimant tous les zéros (espaces vides).

    Args:
        grid (list): la grille actuelle du jeu

    Returns:
        list: la grille compressée
    """
    new_grid = [[0 for _ in range(len(grid))] for _ in range(len(grid))]
    for i in range(len(grid)):
        non_zero_tiles = [tile for tile in grid[i] if tile != 0]
        for j, tile in enumerate(non_zero_tiles):
            new_grid[i][j] = tile
    return new_grid

def fusionner(grid):
    """
    fusionner les tuiles adjacentes de même valeur.

    Args:
        grid (list): la grille actuelle du jeu

    Returns:
        list: la grille avec les tuiles fusionnées
    """
    for i in range(len(grid)):
        for j in range(len(grid) - 1):
            if grid[i][j] == grid[i][j + 1]:
                grid[i][j] *= 2
                grid[i][j + 1] = 0
    return grid

def inverser(grid):
    """
    inverser l'ordre des éléments de chaque rangée de la grille.

    Args:
        grid (list): la grille actuelle du jeu

    Returns:
        list: la grille inversée
    """
    return [row[::-1] for row in grid]

def transposer(grid):
    """
    transposer la grille (échanger les lignes et les colonnes).

    Args:
        grid (list): la grille actuelle du jeu

    Returns:
        list: la grille transposée
    """
    return [list(row) for row in zip(*grid)]

def bouger(grid, direction):
    """
    Effectue un mouvement dans la direction donnée sur la grille.
    
    Args:
        grid (list): la grille actuelle du jeu
        direction (str): la direction du mouvement ('up', 'down', 'left', 'right')
        
    Returns:
        list: la grille après le mouvement
    """
    if direction == "up":
        grid = transposer(grid)
        grid = compresser(grid)
        grid = fusionner(grid)
        grid = compresser(grid)
        grid = transposer(grid)
    elif direction == "down":
        grid = transposer(grid)
        grid = inverser(grid)
        grid = compresser(grid)
        grid = fusionner(grid)
        grid = compresser(grid)
        grid = inverser(grid)
        grid = transposer(grid)
    elif direction == "left":
        grid = compresser(grid)
        grid = fusionner(grid)
        grid = compresser(grid)
    elif direction == "right":
        grid = inverser(grid)
        grid = compresser(grid)
        grid = fusionner(grid)
        grid = compresser(grid)
        grid = inverser(grid)
    return grid

def is_game_over(grid):
    """
    Vérifie si le jeu est terminé.
    
    Args:
        grid (list): la grille actuelle du jeu
        
    Returns:
        bool: True si le jeu est terminé, sinon False
    """
    return not peut_bouger(grid)


def dessiner_grille(stdscr, grid):
    """
    Dessine la grille du jeu dans le terminal en utilisant curses.

    Args:
        stdscr (curses.window): la fenêtre principale de curses
        grid (list): la grille actuelle du jeu
    """

    color_map = {
    0: 0,
    2: 1,
    4: 2,
    8: 3,
    16: 4,
    32: 5,
    64: 6,
    128: 7,
    256: 1,
    512: 2,
    1024: 3,
    2048: 4
    }

    stdscr.clear()
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile != 0:
                color_pair = color_map[tile]
                stdscr.attron(curses.color_pair(color_pair))
                stdscr.addstr(i * 2, j * 5, f"{tile:4}")
                stdscr.attroff(curses.color_pair(color_pair))
            else:
                stdscr.addstr(i * 2, j * 5, f"{tile:4}")
    stdscr.refresh()


def get_input(stdscr):
    """
    Récupère les entrées utilisateur en utilisant curses.

    Args:
        stdscr (curses.window): la fenêtre principale de curses

    Returns:
        str: la direction choisie par l'utilisateur ('up', 'down', 'left', 'right')
    """
    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP:
            return "up"
        elif key == curses.KEY_DOWN:
            return "down"
        elif key == curses.KEY_LEFT:
            return "left"
        elif key == curses.KEY_RIGHT:
            return "right"


def get_taille_grille(stdscr):
    while True:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, "Entrez la taille de la grille (2-10) : ")
        curses.echo()  # Active l'écho du texte saisi
        size_str = stdscr.getstr().decode("utf-8")
        curses.noecho()  # Désactive l'écho du texte saisi
        try:
            size = int(size_str)
            if 2 <= size <= 10:
                return size
        except ValueError:
            pass


def get_proba_2(stdscr):
    while True:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, "Quelle probabilité pour voir apparître le chiffre 2 (0.0-1.0) ? : ")
        curses.echo()  # Active l'écho du texte saisi
        valeur_str = stdscr.getstr().decode("utf-8")
        curses.noecho()  # Désactive l'écho du texte saisi
        try:
            valeur = float(valeur_str)
            if 0 <= valeur <= 1:
                return valeur
        except ValueError:
            pass


def lire_scores(fichier):
    try:
        with open(fichier, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"meilleur_score": 0, "historique_scores": []}


def ecrire_scores(fichier, scores):
    with open(fichier, "w") as f:
        json.dump(scores, f)


def main(stdscr):
    """
    La fonction principale qui exécute le jeu 2048 avec curses.

    Args:
        stdscr (curses.window): la fenêtre principale de curses
    """

    curses.curs_set(0)  # Masque le curseur
    curses.start_color()
    curses.use_default_colors()
    for i in range(1, 10):  # Initialise 10 paires de couleurs
        curses.init_pair(i, i, -1)

    taille_grille = get_taille_grille(stdscr)
    probabilité = get_proba_2(stdscr)
    grid = initialiser_la_grille(taille_grille)
    grid = ajout_nombre(grid, probabilité)
    grid = ajout_nombre(grid, probabilité)

    scores_fichier = "scores.json"
    scores = lire_scores(scores_fichier)
    meilleur_score = scores["meilleur_score"]
    
    while not is_game_over(grid):
        dessiner_grille(stdscr, grid)
        direction = get_input(stdscr)
        new_grid = bouger(grid, direction)
        if new_grid != grid:
            grid = new_grid
            grid = ajout_nombre(grid, probabilité)

    # Calcule le score final
    score_final = sum([sum(row) for row in grid])

    # Mette à jour le meilleur score si nécessaire
    if score_final > meilleur_score:
        msg = "Nouveau meilleur score : " + str(score_final)
        stdscr.addstr(len(grid) * 2, 0, msg)
        scores["meilleur_score"] = score_final
    else :
        msg = "Score : " + str(score_final) + ", record à battre : " + str(meilleur_score)
        stdscr.addstr(len(grid) * 2, 0, msg)

    # Ajoute le score final à l'historique des scores
    scores["historique_scores"].append(score_final)

    # Écrire les scores mis à jour dans le fichier JSON
    ecrire_scores(scores_fichier, scores)

    
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)