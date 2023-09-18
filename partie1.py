from typing import List,Tuple
import re
import string

# Fonction qui initialise la matrice avec des 0,1 et 2 selon qu'une case est occupé par un vide, un pion noir ou blanc
def init_board(n: int) -> List[List[int]]:
    # Initialisation d'une matrice n x n avec toutes les valeurs à 0
    board = [[0 for j in range(n)] for i in range(n)]
    
    # Boucle à travers toutes les lignes et colonnes de la matrice
    for i in range(2):
        for j in range(n):
            board[i][j] = 1
            board[-i-1][j] = 2
    return board


# Fonction qui permet d'afficher l'état actuel du plateau de jeu avec W,B ou . 
def print_board(board: List[List[int]]) -> None:
    n = len(board)
    # Définition d'une liste de tirets pour les bords du plateau
    tiret = ['-' for i in range(n)]
    # Définition de la liste des lettres pour les colonnes
    letters = [chr(i) for i in range(97, 97 + n)]
    # Définition de la largeur du numéro de ligne
    line_number_width = len(str(n))
    # Définition des espaces pour aligner l'affichage
    space1 = "    "
    space2 = "     "
    # Affichage des tirets en haut du plateau
    if line_number_width == 1:
        print(space1+" ".join(tiret))
    else:
        print(space2+" ".join(tiret))
    # Boucle pour afficher les lignes du plateau
    for i in range(n):
        # Calcul et mise en forme du numéro de ligne
        if len(str(n - i)) == 1:
            line = str(n - i).rjust(line_number_width, " " ) + " |"
        
        else:
            line = str(n - i) + " |"
        
        # Boucle pour ajouter les valeurs dans la ligne    
        for j in range(n):
            if board[i][j] == 1:
                line += " " + "B"
            elif board[i][j] == 2:
                line += " " + "W"
            else:
                line += " " + "."
        # Ajout du bord droit et affichage de la ligne
        line += " |"
        print(line)  
    # Affichage des tirets en bas du plateau
    if line_number_width == 1:
        print(space1+" ".join(tiret))
        print(space1+" ".join(letters))
    else:
        print(space2+" ".join(tiret))
        print(space2+" ".join(letters))   

# Fonction pour déterminer le gagnant de la partie    
def winner(board: List[List[int]]) -> int or None:
    n = len(board)
    
    # Boucle pour parcourir les lignes du plateau et verifier si un joueur a gagné
    for i in range(n):
        if board[0][i] == 2:
            return 1
        if board[n-1][i] == 1:
            return 2
    return None

# Fonction qui vérifie si une position est à l'intérieur du plateau de jeu
def is_in_board(n: int, pos: Tuple[int, int]) -> bool:
    i, j = pos
    return (i >= 0 and i < n and j >= 0 and j < n)

# Fonction qui permet de boucler jusqu'à ce qu'un coup valide soit entré par l'utilisateur
def input_move() -> str:
    while True:
        move = input("Entrez votre coup : ")
        # Vérifier si le coup entré correspond au format attendu en utilisant les expressions régulières
        # Un coup est considéré comme valide s'il correspond au format de la variable pattern
        pattern = r"[a-z][0-9]{1,2}>[a-z][0-9]{1,2}"
        if re.match(pattern, move):
            return move
        else:
            print("Veuillez entrer un coup au format valide (exemple : a7>a6)")
    
    print("")


# Fonction qui permet de convertir le format par exemple (a3) en indice d'une case de plateau
def extract_pos(n: int, str_pos: str) -> Tuple[int, int]:
    if len(str_pos) < 2:
        return None
    col = string.ascii_lowercase.index(str_pos[0])
    try:
        row = n - int(str_pos[1]) 
    except ValueError:
        return None
    if row < 0 or col >= n:
        return None
    return row, col

# Fonction qui permet de verifier le deplacement d'un pion
def check_move(board: List[List[int]], player: int, str_move: str) -> bool:
    # Récupération des positions de départ et d'arrivée du mouvement
    start, end = extract_pos(len(board), str_move[:2]), extract_pos(len(board), str_move[3:])
    i, j = start # Indices de départ
    x, y = end # Indices d'arrivée
    
    # Vérification que la case de départ contient bien un pion du joueur en question
    if board[i][j] != player:
        return False
    
    # Vérification que la case d'arrivée n'est pas occupée par un pion du même joueur
    if board[x][y] == player:
        return False
    
    # Vérification du déplacement en avant (tout droit)
    if j == y:
        if abs(x - i) == 1:
            if board[x][y] != 0:  
                return False
        return True
    # Vérification du déplacement en diagonale (avant-gauche ou avant-droit)
    elif abs(j - y) == 1:
        if abs(x - i) == 1:
            return True
    
    # Si aucune condition n'a été remplie, le mouvement n'est pas valide
    return False

# Fonction qui permet de déplacer un pion
def play_move(board: List[List[int]], move: Tuple[Tuple[int, int], Tuple[int, int]], player: int) -> None:
    
    start, end = move
    i, j = start
    x, y = end
    board[x][y] = player
    board[i][j] = 0
 
# Fonction principale du jeu qui vas lancer le jeu en utilisant les fonctions définies ci-dessus
def main(n: int):
    board = init_board(n)
    player = 1
    current_player = "Noir (B)"
    
    # Boucle infinie pour jouer le jeu
    while True:
        # Affiche le plateau de jeu
        print_board(board)
        # Demande au joueur actuel de saisir son mouvement
        print("Joueur ",current_player,": ",end="")
        str_move = input_move()
        # Extrait les positions de départ et d'arrivée du mouvement
        move = extract_pos(n, str_move[:2]), extract_pos(n, str_move[-2:])
        
        # Vérifie si les positions sont dans le plateau de jeu
        if not is_in_board(n, move[0]) or not is_in_board(n, move[1]):
            print("Les coordonnées saisies sont en dehors du plateau.")
            # Retourne au début de la boucle pour demander à nouveau le mouvement
            continue
        
        # Vérifie si le mouvement est autorisé    
        if not check_move(board, player, str_move):
            print("Ce mouvement n'est pas autorisé.")
            continue
        
        # Joue le mouvement sur le plateau de jeu    
        play_move(board, move, player)
        
        # Vérifie si un joueur a gagné
        winner_ = winner(board)
        
        # Si un joueur a gagné
        if winner_:
            
            # Affiche le plateau final
            print_board(board)
            
            # Affiche le message de victoire pour le joueur blanc ou noir
            if winner_ == 1:
                print("Le joueur blanc a gagné !")
            else:
                print("Le joueur noir a gagné !")
            break
        
        # Change de joueur
        player = 2 if player == 1 else 1
        current_player = "Blanc (W)" if current_player == "Noir (B)" else "Noir (B)"
        
if __name__ == '__main__':
    main(8)


