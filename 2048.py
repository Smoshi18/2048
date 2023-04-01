import random
import copy


boardSize = 4








def afficher():
    largest = board[0][0]
    for ligne in board:
        for element in ligne:
            if element > largest :
                largest = element
    numSpaces = len(str(largest))
    for ligne in board:
        currRow = "|"
        for element in ligne:
            if element == 0:
                currRow += " " * numSpaces + "\033[96m|\033[96m"
            else:
                currRow += (" " * (numSpaces - len(str(element)))) + str(element) + "\033[96m|\033[96m"
        print(currRow)
    print()





def fusionner_une_ligne(ligne):
    for j in range(boardSize - 1):
        for i in range(boardSize - 1, 0, -1):
            if ligne[i - 1] == 0:
             ligne[i - 1] = ligne[i]
             ligne[i] = 0
    for i in range(boardSize - 1):
        if ligne[i] == ligne[i + 1]:
            ligne[i] *= 2
            ligne[i + 1] = 0
    for i in range(boardSize - 1, 0, -1):
        if ligne[i - 1] == 0:
            ligne[i - 1] = ligne [i]
            ligne[i] = 0
    
    return ligne



def fusionner_gauche(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = fusionner_une_ligne(currentBoard[i])
    
    return currentBoard


def reverse(ligne):
    new = []
    for i in range(boardSize - 1, -1, -1):
        new.append(ligne[i])
    
    return new


def fusionner_droite(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = reverse(currentBoard[i])
        currentBoard[i] = fusionner_une_ligne(currentBoard[i])
        currentBoard[i] = reverse(currentBoard[i])
    
    return currentBoard


def transpose(currentBoard):
    for j in range(boardSize):
        for i in range (j, boardSize):
            if not i == j:
                temp = currentBoard[j][i]
                currentBoard[j][i] = currentBoard[i][j]
                currentBoard[i][j] = temp
    return currentBoard


def fusionner_haut(currentBoard):
    currentBoard = transpose(currentBoard)
    currentBoard = fusionner_gauche(currentBoard)
    currentBoard = transpose(currentBoard)
    
    return currentBoard

def fusionner_bas(currentBoard):
    currentBoard = transpose(currentBoard)
    currentBoard = fusionner_droite(currentBoard)
    currentBoard = transpose(currentBoard)
    
    return currentBoard

def choisir_nouvelle_valeur():
    if random.randint(1, 8) == 1:
        return 4
    else:
        return 2


def ajouter_nouvelle_valeur():
    numero_ligne = random.randint(0, boardSize - 1)
    numero_colonne = random.randint(0, boardSize - 1)
    while not board[numero_ligne][numero_colonne] == 0:
        numero_ligne = random.randint(0, boardSize - 1)
        numero_colonne = random.randint(0, boardSize - 1)
    
    board[numero_ligne][numero_colonne] = choisir_nouvelle_valeur()

def gagné():
    for ligne in board:
        if 2048 in ligne:
            return True
    return False

def aucun_mouvement():
    tempBoard1 = copy.deepcopy(board)
    tempBoard2 = copy.deepcopy(board)
    
    
    tempBoard1 = fusionner_bas(tempBoard1)
    if tempBoard1 == tempBoard2:
        tempBoard1 = fusionner_haut(tempBoard1)
        if tempBoard1 == tempBoard2:
            tempBoard1 = fusionner_gauche(tempBoard1)
            if tempBoard1 == tempBoard2:
                tempBoard1 = fusionner_droite(tempBoard1)
                return True
    return False
            
    
        
   
        
    
    
    

board = []
for i in range(boardSize):
    ligne = []
    for j in range(boardSize):
        ligne.append(0)
    board.append(ligne)
    
    
nombre_requis = 2
while nombre_requis > 0:
    numero_ligne = random.randint(0, boardSize - 1)
    numero_colonne = random.randint(0, boardSize - 1)
    
    if board[numero_ligne][numero_colonne] == 0:
        board[numero_ligne][numero_colonne] = choisir_nouvelle_valeur()
        nombre_requis -= 1


print("\033[96mBienvenue sur le jeu 2048 ! votre objectif est de combiner des nombres pour arriver à la valeur 2048\033[96m")

afficher()

GameOver = False

while not GameOver:
    move = input("\033[96mDe quelle coté voulez vous fusionnez ?\033[96m")
    
    validInput = True
    
    tempBoard = copy.deepcopy(board)
    
    
    if move == "d":
        board = fusionner_droite(board)
    elif move == "z":
        board = fusionner_haut(board)
    elif move == "q":
        board = fusionner_gauche(board)
    elif move == "s":
        board = fusionner_bas(board)
    else:
        validInput = False
    
    
    if not validInput:
        print("\033[96mvotre saisie n'est pas valide, veuillez réessayer\033[96m")
    else:
        if board == tempBoard:
            print("\033[96mEssayer une autre direction\033[96m")
        else:
            if gagné():
                afficher()
                print("\033[96mBravo tu as gagner\033[96m")
                GameOver = True
            else:
                ajouter_nouvelle_valeur()
                afficher()
                
                
                if aucun_mouvement():
                    print("\033[96mDommage, tu n'a plus de mouvement possible tu a perdu !\033[96m")
                    GameOver = True
                    
                    
                    
                    
                    
                