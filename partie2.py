from typing import List,Tuple
import os.path
import random
import sys
import time
import partie1

# Fonction pour initialiser le plateau de jeu en fonction d'un fichier ou d'une configuration par défaut
def init_board(file_path: str or None) -> List[List[int]]:
    # Initialisation de la variable 'board'
    board = []
    
    # Si 'file_path' n'est pas None (c'est-à-dire si un chemin de fichier est spécifié)
    if file_path is not None:
        # Vérification de l'existence du fichier
        if not (os.path.isfile(file_path)):
            return "Le fichier n'existe pas"
        
        # Ouverture du fichier en mode lecture
        with open(file_path, "r") as f:
            # Lecture de la première ligne du fichier
            line1 = f.readline()
            # Récupération de la taille du plateau depuis la première ligne
            n = int(line1[0])
            
            # Initialisation du plateau avec des cases vides
            board = [[0 for m in  range(n)] for d in range(n)]
            
            # Lecture de la deuxième ligne du fichier
            line2 = f.readline()
            
            # Séparation des éléments de la deuxième ligne en utilisant la virgule comme séparateur
            l = line2.split(',') 
            
            # Remplissage du plateau avec des pions du joueur 2 aux positions spécifiées dans 'line2'
            for x in l:
                indice = partie1.extract_pos(n, x)
                i, j = indice[0], indice[1]
                board[i][j] = 2
            
            # Lecture de la troisième ligne du fichier
            line3 = f.readline()
            
            # Séparation des éléments de la troisième ligne en utilisant la virgule comme séparateur
            l = line3.split(',')
            
            # Remplissage du plateau avec des pions du joueur 1 aux positions spécifiées dans 'line3'
            for x in l:
                indice = partie1.extract_pos(n, x)
                i, j = indice[0], indice[1]
                board[i][j] = 1
    
    # Si 'file_path' est None (c'est-à-dire si aucun chemin de fichier n'est spécifié),
    # initialisation d'un plateau par défaut
    else:
        board = [[0 for i in range(7)] for j in range(7)]
        for i in range(7):
            for j in range(7):
                if i < 2:
                    board[i][j] = 1
                elif 7 - i <= 2:
                    board[i][j] = 2
        
    return board


# Fonction pour que l'IA sélectionne une pièce (pawn)
def ai_select_peg(board: List[List[int]], player: int) -> tuple:
    # Obtenir les positions valides pour le joueur donné
    valid_positions = get_valid_positions(board, player)
    
    # Sélectionner une position aléatoire parmi les positions valides
    # Note: random.choice renvoie une seule position, donc nous utilisons random.choice deux fois pour obtenir un tuple de coordonnées (i, j)
    return random.choice(random.choice(valid_positions))


# Fonction pour que l'IA effectue un déplacement
def ai_move(board: List[List[int]], pos: Tuple[int, int], player: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    # Récupérer les coordonnées actuelles du pion
    i, j = pos
    n = len(board)
    possible_move = []  # Liste pour stocker les mouvements possibles
    direction = 1 if player == 1 else -1  # Direction de déplacement en fonction du joueur

    # Vérifier si le déplacement vers l'avant est possible
    if board[i + direction][j] == 0:
        possible_move.append((i + direction, j))

    # Vérifier les mouvements en diagonale si le pion est sur une bordure
    if j == 0:
        if board[i + direction][j + 1] != player:
            possible_move.append((i + direction, j + 1))
    elif j == n - 1:
        if board[i + direction][j - 1] != player:
            possible_move.append((i + direction, j - 1))
    else:
        if board[i + direction][j + 1] != player:
            possible_move.append((i + direction, j + 1))
        if board[i + direction][j - 1] != player:
            possible_move.append((i + direction, j - 1))

    # Sélectionner aléatoirement l'une des positions possibles pour le prochain mouvement
    selected_move = random.choice(possible_move)
    
    # Retourner à la fois la position actuelle et la position sélectionnée
    return pos, selected_move

# Fonction qui recuper les positions valides
def get_valid_positions(board: List[List[int]], player: int) -> List[List[Tuple[int, int]]]:
    # Initialiser la taille du plateau
    n = len(board)
    
    # Liste pour stocker les positions valides
    valid_positions = []
    
    # Définir la direction de déplacement en fonction du joueur
    direction = 1 if player == 1 else -1
    
    # Parcourir le plateau de jeu
    for i in range(n):
        list_indice = []  # Liste temporaire pour stocker les positions valides d'une ligne
        for j in range(n):
            # Vérifier si la case contient le pion du joueur actuel
            if board[i][j] == player:
                # Vérifier le déplacement vers l'avant
                if 0 <= i + direction < n and board[i + direction][j] == 0:
                    list_indice.append((i, j))
                # Vérifier les déplacements en diagonale
                elif 0 <= j + 1 < n and board[i + direction][j + 1] != player:
                    list_indice.append((i, j))
                elif 0 <= j - 1 < n and board[i + direction][j - 1] != player:
                    list_indice.append((i, j))

        # Si des positions valides ont été trouvées dans cette ligne, les ajouter à la liste principale
        if list_indice:
            valid_positions.append(list_indice)

    # Retourner la liste des positions valides
    return valid_positions
     
# Fonction pour que l'utilisateur sélectionne une pièce (pawn)  
def input_select_peg(board: List[List[int]], player: int) -> tuple:
    # Obtenir les positions valides pour le joueur actuel
    valid_positions = get_valid_positions(board, player)
    
    # Initialiser les indices pour suivre la position actuelle
    i, j = 0, 0
    
    # Obtenir la position actuelle
    current_pos = valid_positions[i][j]
    
    # Marquer la position actuelle sur le tableau
    board[current_pos[0]][current_pos[1]] = 3
    
    print("Utilisez i (haut), k (bas), j (gauche), l (droite) pour sélectionner, y pour confirmer la sélection")
    
    while True:
        print_board(board)  # Afficher le plateau de jeu
        
        selection = input(">")  # Attendre une entrée utilisateur
        
        if selection == 'y':
            # L'utilisateur a confirmé la sélection, retourner la position actuelle
            board[current_pos[0]][current_pos[1]] = player
            return current_pos
        
        elif selection == 'i':
            # Déplacement vers le haut
            if i == 0:
                # Si nous sommes au début de la liste des lignes, revenir à la fin
                board[current_pos[0]][current_pos[1]] = player
                i = len(valid_positions) - 1
                next_line = valid_positions[i]
                j = find_closest_peg(current_pos, next_line)
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
            else:
                # Sinon, monter d'une ligne
                board[current_pos[0]][current_pos[1]] = player
                i -= 1
                next_line = valid_positions[i]
                j = find_closest_peg(current_pos, next_line)
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
    
        elif selection == 'k':
            # Déplacement vers le bas
            if i == len(valid_positions) - 1:
                # Si nous sommes à la fin de la liste des lignes, revenir au début
                board[current_pos[0]][current_pos[1]] = player
                i = 0
                next_line = valid_positions[i]
                j = find_closest_peg(current_pos, next_line)
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
            else:
                # Sinon, descendre d'une ligne
                board[current_pos[0]][current_pos[1]] = player
                i += 1
                next_line = valid_positions[i]
                j = find_closest_peg(current_pos, next_line)
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
                
        elif selection == 'j':
            # Déplacement vers la gauche
            if j == 0:
                # Si nous sommes au début de la ligne, revenir à la fin
                board[current_pos[0]][current_pos[1]] = player
                j = len(valid_positions[i]) - 1
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
            else:
                # Sinon, déplacer vers la gauche
                board[current_pos[0]][current_pos[1]] = player
                j -= 1
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
                
        elif selection == 'l':
            # Déplacement vers la droite
            if j == len(valid_positions[i]) - 1:
                # Si nous sommes à la fin de la ligne, revenir au début
                board[current_pos[0]][current_pos[1]] = player
                j = 0
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
            else:
                # Sinon, déplacer vers la droite
                board[current_pos[0]][current_pos[1]] = player
                j += 1
                current_pos = valid_positions[i][j]
                board[current_pos[0]][current_pos[1]] = 3
            
        else:
            print("Sélection invalide, veuillez recommencer")
            
    return current_pos


# Fonction pour que l'utilisateur effectue un déplacement
def input_move(board: List[List[int]], pos: Tuple[int, int], player: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    # Initialisation de l'indice et de la position courante
    moves = valid_moves(board, pos, player)
    print(moves)
    k = 0
    current_pos = moves[k]
    
    # Sauvegarde de la valeur précédente à la position courante
    preced_value = board[current_pos[0]][current_pos[1]]
    
    # Marquage de la position courante
    board[current_pos[0]][current_pos[1]] = 3
    
    # Nombre de mouvements valides
    n = len(moves)
    
    print(valid_moves)
        
    while True:
        print_board(board)  # Affichage du plateau de jeu
        print("Utiliser j (gauche), l (droite) pour sélectionner, y pour confirmer la sélection")
        selection = input(">")  # Attente de l'entrée utilisateur
        
        if selection == 'y':
            # L'utilisateur a confirmé la sélection, restaurer la valeur précédente et retourner le mouvement
            board[current_pos[0]][current_pos[1]] = preced_value
            return pos, current_pos
        
        elif selection == 'j':
            # Déplacement vers la gauche
            board[current_pos[0]][current_pos[1]] = preced_value
            k = (k - 1 + n) % n  # Passage au mouvement précédent (circulaire)
            current_pos = moves[k]
            preced_value = board[current_pos[0]][current_pos[1]]
            board[current_pos[0]][current_pos[1]] = 3
            
        elif selection == 'l':
            # Déplacement vers la droite
            board[current_pos[0]][current_pos[1]] = preced_value
            k = (k + 1) % n  # Passage au mouvement suivant (circulaire)
            current_pos = moves[k]
            preced_value = board[current_pos[0]][current_pos[1]]
            board[current_pos[0]][current_pos[1]] = 3

# Fonctin qui recupere les pions jouables
def valid_moves(board: List[List[int]], pos: Tuple[int, int], player: int) -> List[Tuple[int, int]]:
    # Obtention des coordonnées de la position
    i, j = pos
    
    # Taille du plateau de jeu
    n = len(board)
    
    # Liste des mouvements valides
    valid_moves = []
    
    # Direction du mouvement en fonction du joueur
    direction = 1 if player == 1 else -1
    
    # Vérification des mouvements possibles
    
    # Mouvement en avant (bas pour le joueur 1, haut pour le joueur 2)
    if board[i + direction][j] == 0:
        valid_moves.append((i + direction, j))
    
    # Mouvements en diagonale
    
    # Si le joueur est au bord gauche du plateau
    if j == 0:
        # Vérification du mouvement diagonal droit
        if board[i + direction][j + 1] != player:
            valid_moves.append((i + direction, j + 1))
    
    # Si le joueur est au bord droit du plateau
    elif j == n - 1:
        # Vérification du mouvement diagonal gauche
        if board[i + direction][j - 1] != player:
            valid_moves.append((i + direction, j - 1))
    
    # Si le joueur est au milieu du plateau
    else:
        # Vérification des mouvements diagonaux droit et gauche
        if board[i + direction][j + 1] != player:
            valid_moves.append((i + direction, j + 1))
        if board[i + direction][j - 1] != player:
            valid_moves.append((i + direction, j - 1))
    
    return valid_moves

  
# Fonction pour trouver la pièce la plus proche
def find_closest_peg(current_peg: Tuple[int, int], next_line: List[Tuple[int, int]]) -> List[int] :
    # Crée une liste vide pour stocker les paires (position, distance)
    l = []
    # Parcourt toutes les positions dans la liste next_line
    for t in next_line:
        # Calcule la distance de Manhattan entre current_peg et la position t
        distance = abs(current_peg[0]-t[0]) + abs(current_peg[1]-t[1])
        # Ajoute la paire (position, distance) à la liste l
        l.append((t,distance))
    
    # Retourne l'indice de la position la plus proche dans la liste next_line
    return l.index(min(l, key=lambda x: x[1]))

# Fonction pour afficher le plateau de jeu
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
            elif board[i][j] == 3:
                line += " " + "#"
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
    
def main() -> None:
    # Initialisation des variables
    file_path = None
    play_against_ai = False

    # Vérifie les arguments en ligne de commande
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2] == '--ai':
        play_against_ai = True

    # Initialisation du plateau de jeu
    board = init_board(file_path)
    current_player = 1

    # Boucle principale du jeu
    while True:
        # Tour du Joueur 1
        if current_player == 1:
            print("Joueur :", current_player)
            selected_peg = None
            
            # Sélection du pion par le joueur ou l'IA
            if play_against_ai:
                selected_peg = ai_select_peg(board, current_player)
                time.sleep(1)
            else:
                selected_peg = input_select_peg(board, current_player)
                
            # Déplacement du pion par l'IA ou le joueur
            moved_peg = ai_move(board, selected_peg, current_player) if play_against_ai else input_move(board, selected_peg, current_player)
    
            # Joue le coup
            partie1.play_move(board, moved_peg, current_player)
            print_board(board)
          
            # Vérifie s'il y a un gagnant
            winner_result = partie1.winner(board)
            if winner_result is not None:
                print(f"Le joueur {winner_result} a gagné le jeu!")
                break
    
        # Tour du Joueur 2
        else:
            print("Joueur :", current_player)
            selected_peg = None 
            
            # Sélection du pion par le joueur
            selected_peg = input_select_peg(board, current_player) 
            
            # Déplacement du pion par le joueur
            moved_peg = input_move(board, selected_peg, current_player)
          
            # Joue le coup
            partie1.play_move(board, moved_peg, current_player)
            print_board(board)
          
            # Vérifie s'il y a un gagnant
            winner_result = partie1.winner(board)
            if winner_result is not None:
                player = "W" if current_player == 2 else "B"
                print(f"Le joueur {winner_result} ({player}) a gagné le jeu!")
                break
    
        # Change le joueur actif
        current_player = 2 if current_player == 1 else 1

# Point d'entrée du programme
if __name__ == '__main__':
    main()


#pos = ai_select_peg(M, 2)
#print(pos)
#print(ai_move(M, pos, 2))

#partie1.print_board(M)

#input_select_peg(M, 2)
#input_move(M, (4,6), 1)




