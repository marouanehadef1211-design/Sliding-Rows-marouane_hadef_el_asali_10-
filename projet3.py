# projet 3 : Sliding Rows 
# Marouane HADEF EL ASALI 
# Junior (Ton nom)
# ==============================================================================
from ezCLI import *
from ezTK import *
# ==============================================================================

LIGNES = 6
COLONNES = 7
TAILLE_CASE = 72
HAUTEUR_BARRE = 46
MARGE = 6

VIDE = 0
ROUGE = 1
JAUNE = -1

NOM_JOUEUR = {ROUGE: 'Rouge', JAUNE: 'Jaune'}
COULEUR_JOUEUR = {VIDE: 'white', ROUGE: 'red', JAUNE: 'gold'}
FICHIER_SCORE = 'scores_7x6.txt'

# Dictionnaires utilisés pour éviter global.
jeu = {
    'grille': [],
    'joueur': ROUGE,
    'coups': 0,
    'termine': False,
    'gagnant_manche': VIDE,
    'texte_centre': '',
    'colonne_souris': 0,
    'message': '',
    'mode_special': False,
    'special_utilise': {ROUGE: False, JAUNE: False},
    'points': {ROUGE: 0, JAUNE: 0},
    'scores': [],
    'alignements': []
}

interface = {
    'fenetre': None,
    'plateau': None,
    'info': None,
    'etat': None,
    'bouton_special': None
}

# ------------------------------------------------------------------------------
def main():
    """Lance le jeu."""
    jeu['alignements'] = creer_alignements()
    creer_interface()
    nouvelle_partie()
    interface['fenetre'].loop()

# ------------------------------------------------------------------------------
def creer_alignements():
    """Calcule tous les alignements de 4 cases possibles."""
    alignements = []
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))

    for ligne in range(LIGNES):
        for colonne in range(COLONNES):
            for dl, dc in directions:
                alignement = []

                for etape in range(4):
                    l = ligne + etape * dl
                    c = colonne + etape * dc

                    if 0 <= l < LIGNES and 0 <= c < COLONNES:
                        alignement.append((l, c))

                if len(alignement) == 4:
                    alignements.append(alignement)

    return alignements


# ------------------------------------------------------------------------------
def nouvelle_partie():
    """Remet tout à zéro : grille + points."""
    jeu['points'] = {ROUGE: 0, JAUNE: 0}
    commencer_manche('Nouvelle partie : les points sont remis à zéro.')

# ------------------------------------------------------------------------------
def manche_suivante():
    """Lance une nouvelle manche sans remettre les points à zéro."""
    commencer_manche('Nouvelle manche.')

# ------------------------------------------------------------------------------
def commencer_manche(nouveau_message):
    """Prépare une nouvelle manche."""
    grille = []

    for ligne in range(LIGNES):
        grille.append([VIDE] * COLONNES)

    jeu['grille'] = grille
    jeu['joueur'] = ROUGE
    jeu['coups'] = 0
    jeu['termine'] = False
    jeu['gagnant_manche'] = VIDE
    jeu['texte_centre'] = ''
    jeu['colonne_souris'] = 0
    jeu['message'] = nouveau_message
    jeu['mode_special'] = False
    jeu['special_utilise'] = {ROUGE: False, JAUNE: False}

    dessiner_plateau()
    mettre_a_jour_textes()

# ------------------------------------------------------------------------------
def dessiner_plateau():
    """Dessine la barre du haut, la grille et le message de victoire."""
    plateau = interface['plateau']
    plateau.delete('all')

    plateau.create_rectangle(0, 0, COLONNES * TAILLE_CASE, HAUTEUR_BARRE,
                             fill='gainsboro', outline='gray')

    for colonne in range(COLONNES):
        x1 = colonne * TAILLE_CASE
        x2 = x1 + TAILLE_CASE

        plateau.create_line(x1, 0, x1, HAUTEUR_BARRE, fill='gray')
        plateau.create_text((x1 + x2) // 2, HAUTEUR_BARRE // 2,
                            text=str(colonne + 1), font='Arial 14 bold')

    plateau.create_line(COLONNES * TAILLE_CASE, 0,
                        COLONNES * TAILLE_CASE, HAUTEUR_BARRE, fill='gray')

    if jeu['colonne_souris'] is not None and not jeu['termine']:
        colonne = jeu['colonne_souris']

        hx1 = colonne * TAILLE_CASE + 2
        hx2 = hx1 + TAILLE_CASE - 4
        plateau.create_rectangle(hx1, 2, hx2, HAUTEUR_BARRE - 2,
                                 outline='dodgerblue', width=2)

        px1 = colonne * TAILLE_CASE + 18
        py1 = 8
        px2 = px1 + TAILLE_CASE - 36
        py2 = py1 + TAILLE_CASE - 36

        plateau.create_oval(px1, py1, px2, py2,
                            fill=COULEUR_JOUEUR[jeu['joueur']], outline='gray')

    for ligne in range(LIGNES):
        for colonne in range(COLONNES):
            x1 = colonne * TAILLE_CASE + MARGE
            y1 = HAUTEUR_BARRE + ligne * TAILLE_CASE + MARGE
            x2 = x1 + TAILLE_CASE - 2 * MARGE
            y2 = y1 + TAILLE_CASE - 2 * MARGE

            couleur = COULEUR_JOUEUR[jeu['grille'][ligne][colonne]]

            plateau.create_oval(x1, y1, x2, y2,
                                fill=couleur, outline='gray')

    if jeu['termine'] and jeu['texte_centre']:
        x1 = 55
        y1 = HAUTEUR_BARRE + 120
        x2 = COLONNES * TAILLE_CASE - 55
        y2 = HAUTEUR_BARRE + 250

        plateau.create_rectangle(x1, y1, x2, y2,
                                 fill='white', outline='black', width=3)

        couleur_texte = 'black'
        if jeu['gagnant_manche'] != VIDE:
            couleur_texte = COULEUR_JOUEUR[jeu['gagnant_manche']]

        plateau.create_text((x1 + x2) // 2, y1 + 40,
                            text=jeu['texte_centre'],
                            fill=couleur_texte, font='Arial 20 bold',
                            width=x2 - x1 - 20)

        plateau.create_text((x1 + x2) // 2, y1 + 95,
                            text="Cliquez sur 'Manche suivante' pour continuer",
                            fill='black', font='Arial 12 bold')

# ------------------------------------------------------------------------------
def deplacer_souris(event):
    """Déplace l'aperçu du pion dans la barre du haut."""
    if jeu['termine']:
        return

    colonne = event.x // TAILLE_CASE

    if 0 <= colonne < COLONNES and colonne != jeu['colonne_souris']:
        jeu['colonne_souris'] = colonne
        dessiner_plateau()

# ------------------------------------------------------------------------------
def quitter_plateau(event):
    """Cache l'aperçu du pion quand la souris sort du plateau."""
    if jeu['termine']:
        return

    jeu['colonne_souris'] = None
    dessiner_plateau()

# ------------------------------------------------------------------------------
def cliquer_plateau(event):
    """Joue dans la colonne cliquée."""
    if jeu['termine']:
        return

    colonne = event.x // TAILLE_CASE

    if not (0 <= colonne < COLONNES):
        return

    if not jouer_colonne(colonne):
        jeu['message'] = 'Colonne %d pleine.' % (colonne + 1)
        mettre_a_jour_textes()
        return

    jeu['coups'] = jeu['coups'] + 1

    if jeu['mode_special']:
        jeu['special_utilise'][jeu['joueur']] = True
        inverser_grille()
        appliquer_gravite()
        jeu['message'] = 'Coup spécial utilisé par %s.' % NOM_JOUEUR[jeu['joueur']]
        jeu['mode_special'] = False
    else:
        jeu['message'] = '%s a joué en colonne %d.' % (
            NOM_JOUEUR[jeu['joueur']], colonne + 1)

    gagnant = verifier_gagnant()

    if gagnant != VIDE:
        jeu['termine'] = True
        jeu['gagnant_manche'] = gagnant
        jeu['points'][gagnant] = jeu['points'][gagnant] + 1

        sauvegarder_score(gagnant)

        jeu['texte_centre'] = 'Le joueur %s a gagné !' % NOM_JOUEUR[gagnant]
        jeu['message'] = '%s gagne la manche et marque 1 point.' % NOM_JOUEUR[gagnant]

        dessiner_plateau()
        mettre_a_jour_textes()
        return

    if grille_pleine():
        jeu['termine'] = True
        jeu['gagnant_manche'] = VIDE
        jeu['texte_centre'] = 'Match nul !'
        jeu['message'] = 'Match nul : personne ne marque de point.'

        dessiner_plateau()
        mettre_a_jour_textes()
        return

    jeu['joueur'] = -jeu['joueur']
    dessiner_plateau()
    mettre_a_jour_textes()

# ------------------------------------------------------------------------------
def changer_coup_special():
    """Active ou annule le coup spécial du joueur courant."""
    if jeu['termine']:
        return

    joueur = jeu['joueur']

    if jeu['special_utilise'][joueur]:
        jeu['message'] = 'Le joueur %s a déjà utilisé son coup spécial.' % NOM_JOUEUR[joueur]
        jeu['mode_special'] = False
    else:
        jeu['mode_special'] = not jeu['mode_special']

        if jeu['mode_special']:
            jeu['message'] = 'Coup spécial activé pour %s.' % NOM_JOUEUR[joueur]
        else:
            jeu['message'] = 'Coup spécial annulé pour %s.' % NOM_JOUEUR[joueur]

    mettre_a_jour_textes()
    dessiner_plateau()

# ------------------------------------------------------------------------------
def jouer_colonne(colonne):
    """Pose un pion dans une colonne."""
    for ligne in range(LIGNES - 1, -1, -1):
        if jeu['grille'][ligne][colonne] == VIDE:
            jeu['grille'][ligne][colonne] = jeu['joueur']
            return True

    return False

# ------------------------------------------------------------------------------
def inverser_grille():
    """Inverse verticalement la grille."""
    jeu['grille'].reverse()

# ------------------------------------------------------------------------------
def appliquer_gravite():
    """Fait retomber les pions vers le bas après le coup spécial."""
    for colonne in range(COLONNES):
        pions = []

        for ligne in range(LIGNES - 1, -1, -1):
            if jeu['grille'][ligne][colonne] != VIDE:
                pions.append(jeu['grille'][ligne][colonne])

        for ligne in range(LIGNES):
            jeu['grille'][ligne][colonne] = VIDE

        ligne = LIGNES - 1

        for pion in pions:
            jeu['grille'][ligne][colonne] = pion
            ligne = ligne - 1

# ------------------------------------------------------------------------------
def compter_alignements(couleur):
    """Compte les alignements de 4 pour une couleur."""
    compteur = 0

    for alignement in jeu['alignements']:
        correct = True

        for ligne, colonne in alignement:
            if jeu['grille'][ligne][colonne] != couleur:
                correct = False
                break

        if correct:
            compteur = compteur + 1

    return compteur

# ------------------------------------------------------------------------------
def verifier_gagnant():
    """Renvoie le gagnant si un joueur a au moins 2 alignements."""
    lignes_rouges = compter_alignements(ROUGE)
    lignes_jaunes = compter_alignements(JAUNE)

    if lignes_rouges >= 2 and lignes_jaunes >= 2:
        return jeu['joueur']
    if lignes_rouges >= 2:
        return ROUGE
    if lignes_jaunes >= 2:
        return JAUNE

    return VIDE

# ------------------------------------------------------------------------------
def grille_pleine():
    """Vérifie si la grille est pleine."""
    for colonne in range(COLONNES):
        if jeu['grille'][0][colonne] == VIDE:
            return False

    return True

# ------------------------------------------------------------------------------
def lire_scores():
    """Affiche les meilleurs scores de la partie actuelle."""
    if len(jeu['scores']) == 0:
        return 'aucun'

    return ' ; '.join(jeu['scores'][:3])

# ------------------------------------------------------------------------------
def sauvegarder_score(gagnant):
    """Sauvegarde les meilleurs scores de la partie actuelle."""
    nouvelle_ligne = '%03d coups - %s' % (jeu['coups'], NOM_JOUEUR[gagnant])

    jeu['scores'].append(nouvelle_ligne)
    jeu['scores'].sort()

    if len(jeu['scores']) > 10:
        del jeu['scores'][10:]

    write_txt(FICHIER_SCORE, '\n'.join(jeu['scores']))

# ------------------------------------------------------------------------------
def mettre_a_jour_textes():
    """Met à jour les textes de l'interface."""
    lignes_rouges = compter_alignements(ROUGE)
    lignes_jaunes = compter_alignements(JAUNE)

    if jeu['termine']:
        texte_tour = 'Manche terminée'
    else:
        texte_tour = 'Tour : %s' % NOM_JOUEUR[jeu['joueur']]

    if jeu['termine']:
        texte_special = 'spécial bloqué'
    elif jeu['special_utilise'][jeu['joueur']]:
        texte_special = 'spécial déjà utilisé'
    elif jeu['mode_special']:
        texte_special = 'spécial ACTIVÉ'
    else:
        texte_special = 'spécial disponible'

    interface['info']['text'] = '%s | %s | Alignements R:%d J:%d | Points R:%d J:%d' % (
        texte_tour, texte_special, lignes_rouges, lignes_jaunes,
        jeu['points'][ROUGE], jeu['points'][JAUNE])

    if jeu['mode_special']:
        interface['bouton_special']['text'] = 'Coup spécial : ON'
    else:
        interface['bouton_special']['text'] = 'Coup spécial : OFF'

    interface['etat']['text'] = '%s | Meilleurs scores : %s' % (
        jeu['message'], lire_scores())

# ------------------------------------------------------------------------------
def creer_interface():
    """Crée la fenêtre et les widgets."""
    interface['fenetre'] = Win(title='SlidingRows - Projet 3', bg='white', op=4)

    haut = Frame(interface['fenetre'], grow=False, flow='E')
    Button(haut, grow=False, text='Nouvelle partie', command=nouvelle_partie)
    Button(haut, grow=False, text='Manche suivante', command=manche_suivante)

    interface['bouton_special'] = Button(haut, grow=False, text='Coup spécial : OFF',
                                         command=changer_coup_special)

    ligne_info = Frame(interface['fenetre'], grow=False, flow='E')
    interface['info'] = Label(ligne_info, grow=False, text='')

    interface['plateau'] = Canvas(interface['fenetre'], grow=False,
                                  width=COLONNES * TAILLE_CASE,
                                  height=HAUTEUR_BARRE + LIGNES * TAILLE_CASE,
                                  bg='lightblue', border=0,
                                  highlightthickness=0)

    interface['plateau'].bind('<Button-1>', cliquer_plateau)
    interface['plateau'].bind('<Motion>', deplacer_souris)
    interface['plateau'].bind('<Leave>', quitter_plateau)

    bas = Frame(interface['fenetre'], grow=False, flow='E')
    interface['etat'] = Label(bas, grow=False, anchor='W', text='')

# ==============================================================================
if __name__ == '__main__':
    main()
# ==============================================================================
