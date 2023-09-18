import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QGroupBox, QComboBox, QScrollBar, QSpacerItem, QSizePolicy,QHBoxLayout,QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPainter,QColor, QPixmap
from partie1 import init_board, winner,  play_move
from partie2 import valid_moves, get_valid_positions, ai_select_peg, ai_move


 # Classe principale de l'interface graphique du jeu Breakthrough
class BreakthroughMainWindow(QMainWindow):
    
    """
     La classe BreakthroughMainWindow est la fenêtre principale de l'application.
     Elle crée un widget central (self.central_widget) et y ajoute le plateau de jeu (self.board_widget)
     ainsi que les paramètres du jeu (self.settings_widget).

     Le plateau de jeu est une instance de BoardWidget, qui représente la grille de jeu.

     La méthode create_container_widget() crée un widget pour contenir le plateau de jeu
     et les paramètres du jeu. Ce widget est configuré avec une taille fixe et une couleur de fond.

     La méthode setup_ui() configure la disposition de l'interface utilisateur. Elle ajoute
     le widget des paramètres du jeu et le plateau de jeu au widget de conteneur.

     Le plateau de jeu et les paramètres du jeu sont créés dans les classes correspondantes (BoardWidget
     et SettingsWidget) mais ne sont pas montrés ici.
    """
    
    
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Breakthrough")
        self.setGeometry(10, 0, 600, 800)

        # Création d'un widget central pour la fenêtre principale
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background: green")
        self.setCentralWidget(self.central_widget)

        # Création d'une instance de BoardWidget (qui représente le plateau de jeu)
        self.board_widget = BoardWidget()
        self.container_widget = self.create_container_widget()  # Crée un widget pour contenir le plateau et les paramètres du jeu
        self.settings_widget = SettingsWidget(self.board_widget)  # Crée un widget pour les paramètres du jeu

        # Configuration de l'interface utilisateur
        self.setup_ui()

    def create_container_widget(self):
        # Crée un widget de conteneur pour le plateau de jeu
        container_widget = QWidget()
        container_widget.setFixedSize(800, 700)
        container_widget.setStyleSheet("background-color: rgba(255,255,255,0.4)")
        return container_widget

    def setup_ui(self):
        # Configuration de la disposition principale
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.container_widget, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.central_widget.setLayout(central_layout)

        container_layout = QHBoxLayout()
        container_layout.addStretch(1)
        container_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addWidget(self.settings_widget)  # Ajoute le widget des paramètres du jeu
        layout.addWidget(self.board_widget)  # Ajoute le plateau de jeu
        layout.addLayout(container_layout)
        self.container_widget.setLayout(layout)


    
# Classe représentant le widget des paramètres du jeu
class SettingsWidget(QWidget):
    
    """
    La classe SettingsWidget est une composante de l'interface utilisateur d'un jeu 
    de dames réalisé avec PyQt5. Elle est principalement destinée à la configuration 
    des paramètres du jeu avant le début de la partie
    """
    
    def __init__(self, board_widget):
        super().__init__()
        self.board_widget = board_widget  # Une référence au widget du plateau de jeu
        self.player1 = None  # Pour stocker le choix du joueur 1
        self.player2 = None  # Pour stocker le choix du joueur 2
        self.ia_scrollbar = QScrollBar(Qt.Horizontal)  # La barre de défilement pour le délai de l'IA
        self.ai_delay = self.get_scrollbar_value()  # Le délai actuel de l'IA
        self.charged = False  # Indique si le plateau de jeu a été chargé
        self.msg = "Aucun plateau chargé"  # Message d'état affiché

        self.init_ui()  # Initialise l'interface utilisateur

    def init_ui(self):
        # Crée et configure les éléments de l'interface utilisateur

        font1 = QFont()
        font1.setPointSize(17)  # Définir la taille de la police ici (par exemple, 17 points)

        # Crée un groupe de paramètres
        self.group_box = QGroupBox("Paramètres")
        self.group_box.setFont(font1)

        self.init_labels()  # Initialise les étiquettes
        self.init_comboboxes()  # Initialise les menus déroulants
        self.init_scrollbar()  # Initialise la barre de défilement
        self.init_load_button()  # Initialise le bouton de chargement
        self.init_default_label()  # Initialise l'étiquette d'état

        self.create_layout()  # Crée la disposition de l'interface utilisateur

    def init_labels(self):
        # Initialise les étiquettes pour les options de sélection des joueurs et du délai de l'IA
        font2 = QFont()
        font2.setPointSize(15)  # Définir la taille de la police ici (par exemple, 15 points)

        self.label_1 = QLabel("Joueur 1:")
        self.label_1.setFont(font2)
        self.label_1.setFixedWidth(100)

        self.label_2 = QLabel("Joueur 2:")
        self.label_2.setFont(font2)
        self.label_2.setFixedWidth(100)

        self.label_3 = QLabel("Délai de l'IA:")
        self.label_3.setFont(font2)
        self.label_3.setFixedWidth(100)

    def init_comboboxes(self):
        # Initialise les menus déroulants pour la sélection des joueurs

        font2 = QFont()
        font2.setPointSize(15)

        self.player_1_combo = QComboBox()
        self.player_1_combo.setFont(font2)

        # Ajoute des options aux menus déroulants
        self.player_1_combo.addItem("Choisissez le Joueur 1 :")
        self.player_1_combo.addItem("Joueur 1")
        self.player_1_combo.addItem("Ordinateur 1")

        # Désactive la possibilité de sélectionner l'élément indicatif
        self.player_1_combo.model().item(0).setFlags(Qt.ItemIsEnabled)

        self.player_1_combo.currentIndexChanged.connect(self.on_player_1_combo_changed)

        self.player_2_combo = QComboBox()
        self.player_2_combo.setFont(font2)

        # Ajoute des options aux menus déroulants
        self.player_2_combo.addItem("Choisissez le Joueur 2 :")
        self.player_2_combo.addItem("Joueur 2")
        self.player_2_combo.addItem("Ordinateur 2")

        # Désactive la possibilité de sélectionner l'élément indicatif
        self.player_2_combo.model().item(0).setFlags(Qt.ItemIsEnabled)

        self.player_2_combo.currentIndexChanged.connect(self.on_player_2_combo_changed)

        # Définit la feuille de style pour les éléments sélectionnés
        combo_stylesheet = (
            "QComboBox::item:selected {"
            "    background: rgba(139, 69, 19, 0.78); /* Couleur de fond de l'élément sélectionné */"
            "    color: #000000; /* Couleur du texte de l'élément sélectionné */"
            "}"
        )

        self.player_1_combo.setStyleSheet(combo_stylesheet)
        self.player_2_combo.setStyleSheet(combo_stylesheet)

    def init_scrollbar(self):
        # Initialise la barre de défilement pour le délai de l'IA

        self.ia_scrollbar = QScrollBar(Qt.Horizontal)
        self.ia_scrollbar.setRange(1, 5)
        self.ia_scrollbar.setEnabled(False)  # Par défaut, désactive la barre de défilement

        # Définit la taille du curseur de la barre de défilement en utilisant une feuille de style
        slider_width = 20  # Ajuste la largeur selon les besoins
        slider_stylesheet = f"QScrollBar::horizontal {{ height: {slider_width}px; }}"
        self.ia_scrollbar.setStyleSheet(slider_stylesheet)

        self.ia_scrollbar.valueChanged.connect(self.update_ai_delay)

    def init_load_button(self):
        # Initialise le bouton de chargement

        font2 = QFont()
        font2.setPointSize(15)

        self.load_button = QPushButton("Charger")
        self.load_button.setStyleSheet("background-color: rgba(139, 69, 19, 0.78);")
        self.load_button.setFixedWidth(107)
        self.load_button.setFont(font2)
        self.load_button.clicked.connect(self.on_load_button_click)

    def init_default_label(self):
        # Initialise l'étiquette d'état

        font2 = QFont()
        font2.setPointSize(15)

        self.default_label = QLabel(self.msg)
        self.default_label.setFont(font2)
        self.default_label.adjustSize()
        self.default_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

    def create_layout(self):
        # Crée la disposition de l'interface utilisateur

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label_1, 0, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.player_1_combo, 0, 1)
        layout.addWidget(self.label_2, 1, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.player_2_combo, 1, 1)
        layout.addWidget(self.label_3, 2, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.ia_scrollbar, 2, 1)
        layout.addWidget(self.load_button, 3, 0, 1, 1)
        layout.addWidget(self.default_label, 3, 1, 2, 1)
        layout.setColumnStretch(0, 30)
        layout.setColumnStretch(1, 70)

        self.group_box.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.group_box)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(main_layout)

    def on_load_button_click(self):
        # Récupérer l'état de chargement depuis le widget du plateau
        self.charged = self.board_widget.charged
        
        # Vérifier si le plateau n'est pas déjà chargé
        if not self.charged:
            # Vérifier si les joueurs n'ont pas été choisis
            if self.player1 is None or self.player2 is None:
                # Afficher une boîte de dialogue d'alerte
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Alerte")
                msg_box.setText("Veuillez choisir les deux joueurs avant de charger le plateau.")
                msg_box.exec_()
            else:
                # Activer les contrôles du jeu et initialiser le plateau
                if not self.player_1_combo.isEnabled():
                    self.player_1_combo.setEnabled(True) 
                    self.player_2_combo.setEnabled(True) 
                    self.ia_scrollbar.setEnabled(True) 
                    return 
                
                # Marquer le plateau comme chargé et initialiser le jeu
                self.charged = True
                self.board_widget.charged = True
                self.board_widget.create_plateau()
                self.board_widget.board = init_board(8)
                if self.board_widget.start_button.text() == "Relancer":
                    self.board_widget.start_button.setText("Commencer")
                self.board_widget.init_plateau()
                self.board_widget.player1 = self.player1
                self.board_widget.player2 = self.player2
                self.board_widget.ai_delai = self.ai_delay
                self.board_widget.current_player = (self.player2, 2)
                self.player_1_combo.setEnabled(False) 
                self.player_2_combo.setEnabled(False) 
                self.ia_scrollbar.setEnabled(False) 
        else:
            # Afficher une alerte si le plateau est déjà chargé
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Alerte")
            msg_box.setText("Le plateau est déjà chargé.")
            msg_box.exec_()
        pass

    def on_player_1_combo_changed(self, index):
        # Mettre à jour le nom du joueur 1 en fonction de la sélection dans la combo box
        self.player1 = self.player_1_combo.currentText()
        
        # Activer la barre de défilement si l'un des joueurs est un ordinateur
        if self.player1 == "Ordinateur 1" or self.player2 == "Ordinateur 2":
            self.ia_scrollbar.setEnabled(True)
        else:
            # Désactiver la barre de défilement et la réinitialiser
            self.ia_scrollbar.setEnabled(False)
            self.ia_scrollbar.setSliderPosition(0)
    
    def on_player_2_combo_changed(self, index):
        # Mettre à jour le nom du joueur 2 en fonction de la sélection dans la combo box
        self.player2 = self.player_2_combo.currentText()
        
        # Activer la barre de défilement si l'un des joueurs est un ordinateur
        if self.player1 == "Ordinateur 1" or self.player2 == "Ordinateur 2":
            self.ia_scrollbar.setEnabled(True)
        else:
            # Désactiver la barre de défilement et la réinitialiser
            self.ia_scrollbar.setEnabled(False)
            self.ia_scrollbar.setSliderPosition(0)
    
    def update_scrollbar_state(self):
        # Mettre à jour l'état de la barre de défilement en fonction des sélections des joueurs
        if self.player1 == "Ordinateur 1" or self.player2 == "Ordinateur 2":
            self.ia_scrollbar.setEnabled(True)
        else:
            # Désactiver la barre de défilement et la réinitialiser
            self.ia_scrollbar.setEnabled(False)
            self.ia_scrollbar.setSliderPosition(0)
    
    def get_scrollbar_value(self):
        # Obtenir la valeur actuelle de la barre de défilement si elle est activée
        if self.ia_scrollbar.isEnabled():
            return self.ia_scrollbar.value()
        else:
            return None
    
    def update_ai_delay(self, value):
        # Mettre à jour le délai de l'IA en fonction de la valeur de la barre de défilement
        self.ai_delay = value


class BoardWidget(QWidget):
    
    """
    Cette classe gère l'interface utilisateur du jeu de dames en utilisant. 
    Elle permet de créer le plateau de jeu, de gérer les déplacements des pions, 
    de détecter le gagnant et de gérer les interactions avec l'utilisateur, y compris 
    le déroulement du jeu et la réinitialisation de la partie.
    """
    
    def __init__(self):
        super().__init__()

        # Signaux personnalisés
        self.square_clicked = pyqtSignal(int, int)

        # Matrice représentant le plateau de jeu
        self.board_matrix = [[0] * 8 for i in range(8)]

        # Plateau de jeu (représentation interne)
        self.board = init_board(8)

        # Joueurs
        self.player1 = None
        self.player2 = None

        # Joueur actuel (nom et numéro)
        self.current_player = ()

        # Délai de l'IA
        self.ai_delai = None

        # Positions valides pour le déplacement
        self.valid_positions = []

        # Anciennes positions possibles
        self.old_possible_moves = []

        # Case de départ sélectionnée
        self.start = None

        # Indique si le plateau de jeu est chargé
        self.charged = False

        # Indique si le jeu est bloqué
        self.block = False

        # Crée et configure le bouton "Commencer"
        self.start_button = self.create_start_button()

        # Conteneur pour le plateau de jeu
        self.board_container1 = QWidget()
        self.board_container1.setFixedSize(750, 420)

        # Configuration de la mise en page
        self.setLayout(QVBoxLayout())
        self.layout().addStretch()
        self.layout().addWidget(self.board_container1, alignment=Qt.AlignCenter)
        self.layout().addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.layout().addStretch()

    def create_plateau(self):
        # Crée et configure le plateau de jeu (grille de cases)

        board_container2 = QWidget()
        board_layout = QGridLayout()
        board_layout.setSpacing(0)
        board_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(8):
            for j in range(8):
                square = QLabel()
                square.setFixedSize(50, 50)

                # Applique une couleur de fond alternée aux cases (noir et orange)
                if (i + j) % 2 == 0:
                    square.setStyleSheet("background-color: rgba(255,165,0,0.4);")
                else:
                    square.setStyleSheet("background-color: rgba(139, 69, 19, 0.78);")

                square.setProperty("contient_pion", False)

                board_layout.addWidget(square, i, j)

                # Associe une fonction de clic personnalisée à chaque case
                square.mousePressEvent = lambda event, row=i, col=j: self.on_square_click(row=row, col=col)

                # Remplit la matrice du plateau
                self.board_matrix[i][j] = square

        board_container2.setLayout(board_layout)

        board_container1_layout = QVBoxLayout()
        board_container1_layout.addWidget(board_container2, alignment=Qt.AlignCenter)
        board_container1_layout.addStretch()

        self.board_container1.setLayout(board_container1_layout)

    def draw_inside_square(self, row, col, color):
        # Dessine un pion à l'intérieur d'une case du plateau

        if 0 <= abs(row) < 8 and 0 <= abs(col) < 8:
            square = self.board_matrix[row][col]
            self.add_pawn(square, color)
            square.update()

    def init_plateau(self):
        # Initialise le plateau de jeu avec les pions des joueurs

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    self.draw_inside_square(i, j, QColor(0, 0, 0))  # Pion du joueur 1 (noir)
                elif self.board[i][j] == 2:
                    self.draw_inside_square(i, j, QColor(255, 255, 255))  # Pion du joueur 2 (blanc)
                else:
                    # Réinitialise les cases sans pions
                    square = self.board_matrix[i][j]
                    if square.property("contient_pion"):
                        square.clear()
                        square.update()

    def remove_square_background(self, positions):
        # Retire l'arrière-plan des cases spécifiées

        for i in range(len(positions)):
            for j in range(len(positions[i])):
                indice = positions[i][j]
                square = self.board_matrix[indice[0]][indice[1]]
                square.setStyleSheet("background-color: transparent;")

    def set_square_background(self, positions):
        # Applique un arrière-plan aux cases spécifiées

        for x in positions:
            for indice in x:
                square = self.board_matrix[indice[0]][indice[1]]
                if (indice[0] + indice[1]) % 2 == 0:
                    square.setStyleSheet("background-color: rgba(255,165,0,0.4);")
                else:
                    square.setStyleSheet("background-color: rgba(139, 69, 19, 0.78);")

    def on_square_click(self, row, col):
        # Gère l'événement de clic sur une case du plateau

        if self.current_player[0][:5:] == "Ordin":
            return

        if self.valid_positions:
            if self.old_possible_moves:
                if (row, col) in self.old_possible_moves:
                    # Effectue le déplacement du pion ici
                    end = (row, col)
                    play_move(self.board, (self.start, end), self.current_player[1])

                    square = self.board_matrix[self.start[0]][self.start[1]]
                    # Efface le pixmap du QLabel pour supprimer le pion
                    square.clear()
                    # Met à jour l'apparence de la case
                    square.update()

                    color = QColor(255, 255, 255) if self.current_player[1] == 2 else QColor(0, 0, 0)

                    square = self.board_matrix[row][col]
                    self.add_pawn(square, color)
                    self.set_square_background(self.valid_positions)

                    self.set_square_background([self.old_possible_moves])
                    self.old_possible_moves = []
                    self.start = None
                    # Force le widget à se redessiner
                    self.update()

                    if winner(self.board):
                        self.show_message('Fin du jeu', f"{self.current_player[0]} a gagné, félicitations.")
                        self.board = []

                        if self.ask_confirmation('Recommencer', 'Voulez-vous recommencer le jeu ?'):
                            self.restart_game()
                        else:
                            self.reload_game()
                        return

                    self.current_player = (self.player1, 1) if self.current_player[1] == 2 else (self.player2, 2)
                    self.play_game()
                    return
                else:
                    self.set_square_background(self.valid_positions)
                    self.set_square_background([self.old_possible_moves])
                    self.old_possible_moves = []

            possible_moves = []
            for valid in self.valid_positions:
                if (row, col) in valid:
                    possible_moves = valid_moves(self.board, (row, col), self.current_player[1])
                    self.remove_square_background([possible_moves])
                    self.old_possible_moves = possible_moves.copy()
                    self.start = (row, col)

    def add_pawn(self, square, color):
        # Ajoute un pion à l'intérieur d'une case du plateau

        square.setProperty("contient_pion", True)
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.transparent)  # Fond transparent pour le pixmap du pion
        square.setPixmap(pixmap)

        painter = QPainter(square.pixmap())
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(color)
        painter.setPen(QColor(Qt.transparent))

        # Dessine le pion ici (par exemple, un cercle)

        # Cercle 1 (Cercle plus petit)
        circle1_radius = 8
        circle1_center = int(pixmap.width() / 2), int(pixmap.height() / 2) - 2  # Ajuste la position verticale de cercle 1
        painter.drawEllipse(
            circle1_center[0] - circle1_radius, circle1_center[1] - circle1_radius, int(circle1_radius * 2),
            int(circle1_radius * 2))  # Dessine le cercle 1

        # Demi-cercle en dessous de cercle 1
        half_circle_radius = 15
        half_circle_center = circle1_center[0], circle1_center[1] + circle1_radius + half_circle_radius - 2
        painter.drawChord(
            half_circle_center[0] - half_circle_radius, half_circle_center[1] - half_circle_radius,
            int(half_circle_radius * 2), int(half_circle_radius * 2), 0, 180 * 16)  # Dessine le demi-cercle

        # Cercle 2 (Cercle plus grand, au-dessus de cercle 1)
        circle2_radius = 5
        circle2_center = circle1_center[0], circle1_center[1] - circle1_radius - circle2_radius + 2
        painter.drawEllipse(
            circle2_center[0] - circle2_radius, circle2_center[1] - circle2_radius, int(circle2_radius * 2),
            int(circle2_radius * 2))  # Dessine le cercle 2

        painter.end()
        square.setAlignment(Qt.AlignCenter)
        square.update()

    def create_start_button(self):
        # Crée et configure le bouton "Commencer"

        start_button = QPushButton("Commencer")
        font2 = QFont()
        font2.setPointSize(17)
        start_button.setFont(font2)
        start_button.setStyleSheet("background-color: rgba(139, 69, 19, 0.78);")
        start_button.setFixedWidth(750)
        start_button.clicked.connect(self.on_start_button_click)
        return start_button

    def on_start_button_click(self):
        # Gestion de l'événement du bouton "Commencer"

        if self.charged:
            if self.start_button.text() == "Commencer":
                self.start_button.setText("Relancer")
                self.play_game()
            else:
                if self.ask_confirmation('Relancer', "Voulez-vous relancer le jeu"):
                    self.restart_game()
                    return
                return
        else:
            self.show_message("Alerte", "Veuillez choisir les deux joueurs et charger le plateau")

    def restart_game(self):
        # Redémarre le jeu

        if self.valid_positions:
            self.set_square_background(self.valid_positions)
        if self.old_possible_moves:
            self.set_square_background([self.old_possible_moves])
        self.board = init_board(8)
        self.init_plateau()
        self.start_button.setText("Commencer")
        self.on_start_button_click()

    def play_game(self):
        # Gère le déroulement du jeu

        if self.current_player[0][:5:] == "Ordin":
            selected_peg = ai_select_peg(self.board, self.current_player[1])
            moved_peg = ai_move(self.board, selected_peg, self.current_player[1])

            # Lance un timer pour simuler le délai de l'IA
            QTimer.singleShot((self.ai_delai + 1) * 1000, lambda: self.continue_game(moved_peg, selected_peg))
        else:
            valid_positions = get_valid_positions(self.board, self.current_player[1])
            self.remove_square_background(valid_positions)
            self.valid_positions = valid_positions

    def continue_game(self, moved_peg, selected_peg):
        # Continue le jeu après le déplacement de l'IA

        play_move(self.board, moved_peg, self.current_player[1])
        row, col = moved_peg[0][0], moved_peg[0][1]
        square = self.board_matrix[selected_peg[0]][selected_peg[1]]
        # Efface le pixmap du QLabel pour supprimer le pion
        square.clear()
        square.update()

        color = QColor(255, 255, 255) if self.current_player[1] == 2 else QColor(0, 0, 0)
        row, col = moved_peg[1][0], moved_peg[1][1]
        square = self.board_matrix[row][col]
        self.add_pawn(square, color)

        if winner(self.board):
            self.show_message('Fin du jeu', f"{self.current_player[0]} a gagné, félicitations.")
            self.board = []

            if self.ask_confirmation('Recommencer', 'Voulez-vous recommencer le jeu ?'):
                self.restart_game()
            else:
                self.reload_game()
            return

        self.current_player = (self.player1, 1) if self.current_player[1] == 2 else (self.player2, 2)
        self.play_game()

    def reload_game(self):
        # Recharge le jeu pour une nouvelle partie

        for widget in self.board_container1.children():
            widget.deleteLater()
            self.charged = False
        self.update()

    def show_message(self, titre, message):
        # Affiche une boîte de dialogue avec un message d'alerte

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(titre)
        msg_box.setText(message)
        msg_box.exec_()

    def ask_confirmation(self, titre, message):
        # Affiche une boîte de dialogue de confirmation avec deux options

        confirmation = QMessageBox()
        confirmation.setWindowTitle(titre)
        confirmation.setText(message)

        # Définit les boutons personnalisés
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Modifie les textes des boutons
        confirmation.button(QMessageBox.Yes).setText("Oui")
        confirmation.button(QMessageBox.No).setText("Non")

        result = confirmation.exec_()
        return result == QMessageBox.Yes

            
# Définir une classe BreakthroughApp qui hérite de QApplication
class BreakthroughApp(QApplication):
    def __init__(self):
        # Appeler le constructeur de la classe parente QApplication
        super().__init__(sys.argv)
        
        # Créer une instance de la fenêtre principale de l'application (BreakthroughMainWindow)
        self.window = BreakthroughMainWindow()
        
        # Afficher la fenêtre principale de l'application
        self.window.show()

# Point d'entrée de l'application
if __name__ == "__main__":
    # Créer une instance de la classe BreakthroughApp, qui initialise l'application
    app = BreakthroughApp()
    
    # Exécuter l'application en entrant dans la boucle principale de l'interface utilisateur
    sys.exit(app.exec_())
