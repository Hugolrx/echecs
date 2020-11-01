
from tkinter import *
from functools import partial




root = Tk()
root.title("Jeu d'Échecs")
root.iconbitmap("logo.ico")
root.geometry("736x760")
root.resizable(width=False, height=False)

'''
Les couleurs de déplacement sont les suivantes :
- vert : pièce sélectionnée
- orange : roi en échec
- jaune : roi en échec et sélectionné
- rouge : roi en échec et mat
- bleu : roi en pat

- marron (à activer aux lignes 206-207) : pièce sélectionnée sans possibilité de déplacement

'''

class Case() :
    def __init__(self, i, j) :
        self.position = (i,j)

        if i%2 == j%2 :
            self.couleur = "#f8f8f8"
        else :
            self.couleur = "#3a3a3a"

        self.bouton = Button(root, text="", padx=40, pady=30, bg=self.couleur, activebackground=self.couleur, relief=RAISED, bd=3, state=DISABLED)
        self.bouton.grid(row=i, column=j)

        if i < 2 or i > 5 :
            self.occupée = True
        else :
            self.occupée = False

    def update_occupée() :
        for c in d_cases.values() :
            c.occupée = False
            for p in d_pieces.values() :
                if p.position == c.position :
                    c.occupée = True

    def visée(self, couleur) :          # vérifie si la case est visée du pt de vue d'pièce d'une couleur donnée
        for p in d_pieces.values() :
            if couleur == "noir" and p.couleur == "blanc" :
                if self.position in p.vise() :
                    return True
            if couleur == "blanc" and p.couleur == "noir" :
                if self.position in p.vise() :
                    return True
        return False








class Piece() :
    def __init__(self, couleur, i, j) :
        global nb_tour
        self.couleur = couleur
        self.position = (i, j)

        self.pattern_update()
        self.accessible()                 # On appelle .accessible() pour actualiser .vise() et .mangeable

        if i%2 == j%2 :
            self.bg_color = "#f8f8f8"
        else :
            self.bg_color = "#3a3a3a"

        self.bouton = Button(root, image=d_icones[f"ico_{self.piece}_{self.couleur}"], bg = self.bg_color, activebackground = self.bg_color, bd = 0, relief=SUNKEN)

        if self.couleur == "blanc" and nb_tour == 0 :
            self.bouton.configure(command = self.bouger, overrelief=RAISED)
        self.bouton.grid(row=i, column=j)



    def vise(self) :                                  # Liste des cases vues par la pièce (pour se déplacer ou manger)
        temp = self.pattern[:]
        i,j = self.position
        self.mangeable = []

        a,b,c,d,e,f,g,h = (10,-10,10,-10,10,-10,-10,10)     # Cf après

        for k,l in self.pattern :
            if k < 0 or l < 0 or k > 7 or l > 7 :           # On veille à ne pas sortir du plateau
                temp.remove((k,l))
                continue

            if j == l :                                     # Il faut tout d'abord vérifier qu'il n'y a pas d'obstables entre la pièce et la case. Pour les critères, se référer quelques lignes plus loin
                if i-k > a :
                    temp.remove((k,l))
                    continue
                elif i-k < b :
                    temp.remove((k,l))
                    continue
            if i == k :
                if j-l > c :
                    temp.remove((k,l))
                    continue
                if j-l < d:
                    temp.remove((k,l))
                    continue
            if i-k == j-l :
                if j-l > e :
                    temp.remove((k,l))
                    continue
                if j-l < f :
                    temp.remove((k,l))
                    continue
            if i-k == -(j-l) :
                if j-l < g :
                    temp.remove((k,l))
                    continue
                if j-l > h :
                    temp.remove((k,l))
                    continue

            if d_cases[f"c{k}{l}"].occupée :
                for p in d_pieces.values() :
                    if p.position == (k,l) and self.couleur != p.couleur :
                        self.mangeable += [(k,l)]
                if j == l :                                 # obstacle sur la même colone
                    if i-k > 0 :                            # obstacle au dessus
                        a = i-k
                    else :                                  # obstacle en dessous
                        b = i-k

                elif i == k :                               # obstacle sur la même ligne
                    if j-l > 0 :                            # obstacle à gauche
                        c = j-l
                    else:                                   # obstacle à droite
                        d = j-l

                elif i-k == j-l :                           # obstacle sur la diagonale hg-bd
                    if i-k > 0 :                            # obstacle en haut à gauche
                        e = j-l
                    else :                                  # obstacle en bas à droite
                        f = j-l

                elif i-k == -(j-l) :                        # obstacle sur la diagonale bg-hd
                    if i-k > 0 :                            # obstacle en haut à droite
                        g = j-l
                    else :                                  # obstacle en bas à gauche
                        h = j-l

        return temp

    def accessible(self) :                                  # Cases accessibles par self pour le déplacement
        acces = self.vise()
        for (i,j) in self.vise() :
            if d_cases[f"c{i}{j}"].occupée :
                acces.remove((i,j))
        return acces

    def verif(self, list) :                                 # Cf class Roi
        return list



    def bouger(self) :

        Case.update_occupée()                           # Règle des pb d'occupation

        for p in d_pieces.values() :                # On empêche les autres pièces de bouger
            p.bouton.configure(command = 0, overrelief=SUNKEN)

        if self.piece == "roi" and self.bouton.cget("bg") == "orange" :
            self.bouton.configure(bg="yellow", activebackground="yellow", command=self.annuler_bouger, relief = RAISED)
        else :
            self.bouton.configure(bg="#73FF90", activebackground="#73FF90", command=self.annuler_bouger, relief = RAISED)

        self.possible = []                                      # Sert à repérer le mat

        for i in range(8) :                                                     # Soit on se déplace,
            for j in range(8) :
                if d_cases[f"c{i}{j}"].position in self.verif(self.accessible()) :
                    if not(d_pieces[f"roi_{self.couleur}"].test_echec_2(self, d_cases[f"c{i}{j}"])) :   # On vérifie que bouger la pièce n'entrainera pas d'échec contre son propre roi
                        d_cases[f"c{i}{j}"].bouton.configure(state=NORMAL, command=partial(self.update, d_cases[f"c{i}{j}"].position))
                        self.possible += [(i,j)]


        if self.piece == "roi" :                                # Ajoutons la case du roque si possible
            i,j = self.position
            for a in self.test_roque() :
                d_cases[f"c{i}{a}"].bouton.configure(state=NORMAL, command=partial(self.roque, d_cases[f"c{i}{a}"]), text="roque!", padx=18)


        for p in d_pieces.values() :                                            # Soit on mange.
            if p.position in self.verif(self.mangeable) :
                if not(d_pieces[f"roi_{self.couleur}"].test_echec_2(self, p)) :     # On vérifie que le mouvement n'entraine pas d'échec contre son propre camp.
                    p.bouton.configure(command=partial(self.manger, p), overrelief=RAISED)
                    self.possible += [p.position]

        # if self.possible == [] :               # Fond en rouge si la pièce ne peut pas bouger
        #     self.bouton.configure(bg="brown", activebackground="brown")


    def annuler_bouger(self) :
        global nb_tour

        for p in d_pieces.values() :                # On autorise les autres pièces à bouger
            if p.piece == "roi" and p.bouton.cget("bg") == "yellow" :
                p.bouton.configure(bg="orange", activebackground="orange", relief = SUNKEN)
            else :
                p.bouton.configure(bg=p.bg_color, activebackground=p.bg_color, relief = SUNKEN)
            if nb_tour % 2 == 0 :                   # En fonction du tour
                if p.couleur == "blanc" :
                    p.bouton.configure(command = p.bouger, relief = SUNKEN, overrelief=RAISED)
                else :
                    p.bouton.configure(command = 0, relief = SUNKEN, overrelief=SUNKEN)
            else :
                if p.couleur == "noir" :
                    p.bouton.configure(command = p.bouger, relief = SUNKEN, overrelief=RAISED)
                else :
                    p.bouton.configure(command = 0, relief = SUNKEN, overrelief=SUNKEN)


        for i in range(8) :
            for j in range(8) :
                d_cases[f"c{i}{j}"].bouton.configure(state=DISABLED, text="", padx=40)




    def manger(self, mangée) :
        k,l = mangée.position                                     # Nouvelle position
        mangée.bouton.grid_forget()                               # On supprime la pièce

        for key, value in d_pieces.items() :                      # On cherche la clef de la pièce mangée
            if mangée == value:
                nom = key
        d_pieces.pop(nom)                                         # Et on la supprime

        self.update((k,l))



    def bg_update(self) :                       # Actualiser le fond de la pièce quand bouge
        i,j = self.position
        if i%2 == j%2 :
            self.bg_color = "#f8f8f8"
        else :
            self.bg_color = "#3a3a3a"


    def update(self, nvlle_position) :
        global nb_tour
        nb_tour += 1

        i,j = self.position                                  # Ancienne position
        k,l = nvlle_position                                 # Nouvelle position

        self.position = nvlle_position                       # On déplace la pièce
        self.bg_update()
        self.pattern_update()
        self.bouton.grid_configure(row=k, column=l)          # On déplce le bouton

        d_cases[f"c{i}{j}"].occupée = False                  # On change le statut des cases
        d_cases[f"c{k}{l}"].occupée = True


        if self.piece == "pion" or self.piece == "roi" or self.piece == "tour" :       # Pour que le pion/roi ne puisse faire son coup spécial
            self.déplacé = True

        if self.piece == "pion" :                   # Le pion est arrivé à la dernière ligne
            if k == 0 or k == 7 :
                self.promotion()

        self.annuler_bouger()

        if self.couleur == "noir" :
            if Roi.test_echec(d_pieces["roi_blanc"]) :
                d_pieces["roi_blanc"].bouton.configure(bg='orange')

                if Roi.test_mat(d_pieces["roi_blanc"]) :
                    d_pieces["roi_blanc"].bouton.configure(bg='red')
                    fin_de_partie("mat", "noirs")
                    return
                d_pieces["roi_blanc"].bouton.configure(bg='orange')

            elif Roi.test_mat(d_pieces["roi_blanc"]) :
                d_pieces["roi_blanc"].bouton.configure(bg='blue')
                fin_de_partie("pat", 0)

        else :
            if Roi.test_echec(d_pieces["roi_noir"]) :
                d_pieces["roi_noir"].bouton.configure(bg='orange')

                if Roi.test_mat(d_pieces["roi_noir"]) :
                    d_pieces["roi_noir"].bouton.configure(bg='red')
                    fin_de_partie("mat", "blancs")
                    return
                d_pieces["roi_noir"].bouton.configure(bg='orange')

            elif Roi.test_mat(d_pieces["roi_noir"]) :
                d_pieces["roi_noir"].bouton.configure(bg='blue')
                fin_de_partie("pat", 0)

        Case.update_occupée()                       # Règle des problèmes de vision d'occupation de cases










class Roi(Piece) :
    def pattern_update(self) :
        i,j = self.position
        self.pattern = []
        self.pattern = [(i+1,j+1), (i+1,j), (i+1,j-1), (i,j+1), (i,j-1), (i-1,j+1), (i-1,j), (i-1,j-1)]

    def __init__(self, couleur, i, j) :
        self.piece = "roi"
        super().__init__(couleur, i, j)

        self.déplacé = False                         # Le roi n'a pas encore été déplacé (pour le roque)

    def accessible(self) :                                  # Cases accessibles par self pour le déplacement
        acces = self.vise()
        for (i,j) in self.vise() :
            if d_cases[f"c{i}{j}"].occupée :
                acces.remove((i,j))
        return acces

    def verif(self, list) :                         # Le roi ne peut avancer sur une case visée (ie se mettre en échec
        temp = list[:]
        i,j = self.position
        d_cases[f"c{i}{j}"].occupée = False   # On fait comme si le roi était invisible pour bloquer les cases derrière lui
        for k, l in list :
            if d_cases[f"c{k}{l}"].visée(self.couleur) :
                temp.remove((k,l))
        d_cases[f"c{i}{j}"].occupée = True
        return temp


    def test_echec(self) :
        for p in d_pieces.values() :
            if self.couleur != p.couleur and self.position in p.vise() :
                return True
        return False

    def test_echec_2(self, pièce, nouveau) :                        # Test lors d'un déplacement d'une pièce alliée : on fait un coup virtuel, puis on regarde si le roi est en échec ; puis on revient en arrière
        if isinstance(nouveau, Case) :
            i,j = pièce.position                                # Ancienne position
            k,l = nouveau.position                              # Nouvelle position

            pièce.position = (k,l)                              # On déplace la pièce
            pièce.pattern_update()

            d_cases[f"c{i}{j}"].occupée = False                 # On change le statut des cases
            d_cases[f"c{k}{l}"].occupée = True

            if self.test_echec() :
                test = True
            else :
                test = False

            pièce.position = (i,j)                              # On redéplace la pièce
            pièce.pattern_update()

            d_cases[f"c{i}{j}"].occupée = True                  # On rechange le statut des cases
            d_cases[f"c{k}{l}"].occupée = False

            return test
        else :                                                  # Si c'est un mangement, on mange virtuellement
            i,j = pièce.position                                # Ancienne position
            k,l = nouveau.position                              # Nouvelle position

            nouveau.position = (17,9)
            nouveau.pattern_update()                            # On éloigne la pièce virtuellement mangée afin qu'elle n'interfère pas avec le plateau

            pièce.position = (k,l)                              # On déplace la pièce
            pièce.pattern_update()

            d_cases[f"c{i}{j}"].occupée = False                 # On change le statut des cases
            d_cases[f"c{k}{l}"].occupée = True

            if self.test_echec() :
                test = True
            else :
                test = False

            nouveau.position = (k,l)
            nouveau.pattern_update()

            pièce.position = (i,j)                              # On redéplace la pièce
            pièce.pattern_update()

            d_cases[f"c{i}{j}"].occupée = True                  # On rechange le statut des cases
            d_cases[f"c{k}{l}"].occupée = False

            return test




    def test_roque(self) :                         # test si le roques est faisable à gauche
        i,_ = self.position
        if self.déplacé or self.test_echec() :
            return []

        temp = []
        if f"tour_{self.couleur}_1" in d_pieces :                   # Au cas où la tour a été mangée
            if not(d_pieces[f"tour_{self.couleur}_1"].déplacé) :
                if not(d_cases[f"c{i}1"].occupée) and not(d_cases[f"c{i}2"].occupée) and not(d_cases[f"c{i}3"].occupée) :
                    if self.verif([(i, 1), (i, 2), (i, 3)]) == [(i, 1), (i, 2), (i, 3)] :
                        temp.append(1)
        if f"tour_{self.couleur}_2" in d_pieces :                   # Au cas où la tour a été mangée
            if not(d_pieces[f"tour_{self.couleur}_2"].déplacé) :
                if not(d_cases[f"c{i}5"].occupée) and not(d_cases[f"c{i}6"].occupée) :
                    if self.verif([(i, 5), (i, 6)]) == [(i, 5), (i, 6)] :
                        temp.append(6)
        return temp

    def roque(self, nvlle_case) :
        global nb_tour

        self.update(nvlle_case.position)
        i,j = nvlle_case.position
        if j == 1 :
            nb_tour -= 1
            d_pieces[f"tour_{self.couleur}_1"].update(d_cases[f"c{i}2"].position)
        if j == 6 :
            nb_tour -= 1
            d_pieces[f"tour_{self.couleur}_2"].update(d_cases[f"c{i}5"].position)



    def test_mat(self) :
        for p in d_pieces.values() :
            if p.couleur == self.couleur :
                p.bouger()                                  # Appel des fonctions pour actualiser self.possible
                p.annuler_bouger()
                if p.possible != [] :
                    return False
        return True






class Reine(Piece) :
    def pattern_update(self) :
        i,j = self.position
        self.pattern = []
        for a in range(1,8) :
            self.pattern += [(i,j-a), (i-a, j-a), (i-a, j), (i-a, j+a), (i, j+a), (i+a, j+a), (i+a, j), (i+a, j-a)]

    def __init__(self, couleur, i, j) :
        self.piece = "reine"
        super().__init__(couleur, i, j)




class Fou(Piece) :
    def pattern_update(self) :
        i,j = self.position
        self.pattern = []
        for a in range(1,8) :
            self.pattern += [(i-a, j-a), (i-a, j+a), (i+a, j+a), (i+a, j-a)]

    def __init__(self, couleur, i, j) :
        self.piece = "fou"
        super().__init__(couleur, i, j)




class Cavalier(Piece) :
    def pattern_update(self) :
        i,j = self.position
        self.pattern = []
        self.pattern = [(i-2, j-1), (i-2, j+1), (i-1, j-2), (i-1, j+2), (i+1, j-2), (i+1, j+2), (i+2, j-1), (i+2, j+1)]

    def __init__(self, couleur, i, j) :
        self.piece = "cavalier"
        super().__init__(couleur, i, j)




class Tour(Piece) :
    def pattern_update(self) :
        i,j = self.position
        self.pattern = []
        for a in range(1,8) :
            self.pattern += [(i-a, j), (i, j+a), (i+a, j), (i, j-a)]

    def __init__(self, couleur, i, j) :
        self.piece = "tour"
        super().__init__(couleur, i, j)

        self.déplacé = False                 # La tour n'a pas encore été déplacé (pour le roque)






class Pion(Piece) :
    def pattern_update(self) :
        pass

    def __init__(self, couleur, i, j) :
        global nb_promo                                         # cf def promotion()
        self.piece = "pion"
        self.déplacé = False                                    # Le pion a-t-il été déplacé (pour avancer de 2 cases)
        super().__init__(couleur, i, j)
        nb_promo = 0



    def accessible(self):                                       # Le pion a des restrictions pour avancer
        i,j = self.position
        acces = []
        if not(d_cases[f"c{i+1 if self.couleur == 'noir' else i-1}{j}"].occupée) :
            acces = [(i+1, j) if self.couleur == "noir" else (i-1, j)]
            if not(self.déplacé) :
                if not(d_cases[f"c{i+2 if self.couleur == 'noir' else i-2}{j}"].occupée) :
                    acces += [(i+2, j) if self.couleur == "noir" else (i-2, j)]

        self.vise()                              # Pour qu'il soit actualisé lors de l'initialisation

        return acces

    def vise(self) :                                        # Le pion a des restrictions pour manger
        i,j = self.position
        viseur = []
        for a in [-1, 1]:
            viseur += [(i+1, j+a) if self.couleur == "noir" else (i-1, j+a)]

        temp = viseur[:]
        for k,l in viseur :
            if k < 0 or l < 0 or k > 7 or l > 7 :           # On veille à ne pas sortir du plateau
                temp.remove((k,l))

        self.mangeable = []
        for k,l in temp :
            if d_cases[f"c{k}{l}"].occupée :
                for p in d_pieces.values() :
                    if p.position == (k,l) and self.couleur != p.couleur :
                        self.mangeable += [(k,l)]
        return temp

    def promotion(self) :
        global nb_promo, choix, d_promotion
        nb_promo += 1
        root.geometry("886x760")
        choix = Label(root, text="Choisir une pièce :", font=("Courier", 11), wraplength=140, padx=10)
        choix.grid(row=1, column=8)
        d_promotion = {}
        for i, p in enumerate(["reine", "fou", "cavalier", "tour"]) :
            d_promotion[f"{p}"] = Button(root, image=d_icones[f"ico_{p}_{self.couleur}"], command=partial(self.transformation, p))
            d_promotion[f"{p}"].grid(row=i+2, column = 8)

    def transformation(self, piece) :
        global nb_promo, choix, d_promotion, nb_tour
        i,j = self.position
        if piece == "reine" :
            d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"] = Reine(self.couleur, i, j)
        elif piece == "tour" :
            d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"] = Tour(self.couleur, i, j)
        elif piece == "cavalier" :
            d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"] = Cavalier(self.couleur, i, j)
        else :
            d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"] = Fou(self.couleur, i, j)

        nb_tour -= 1
        d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"].manger(self)
        d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"].bouton.configure(command = 0, overrelief=SUNKEN, activebackground = d_pieces[f"{piece}_{self.couleur}_{nb_promo+2}"].bg_color)

        root.geometry("736x760")
        choix.grid_forget()
        for p in ["reine", "fou", "cavalier", "tour"] :
            d_promotion[f"{p}"].grid_forget()






def generation_plateau() :
    global d_cases
    d_cases = {}
    for i in range(8) :
        for j in range(8) :
            d_cases[f"c{i}{j}"] = Case(i,j)


def fin_de_partie(cause, gagnant) :
    for p in d_pieces.values() :                                                # On fige tout
        p.bouton.configure(command = 0, relief=SUNKEN, overrelief=SUNKEN)
    for c in d_cases.values() :
        c.bouton.configure(state=DISABLED, text="", padx=40)

    message1 = Label(root, text="", font=('Helvetica', '25'))
    message2 = Label(root, text="", font=('Helvetica', '15'))
    if cause == "mat" :
        root.geometry("1060x760")
        message1.configure(text="Échec et mat !", padx=20)
        message2.configure(text=f"Les {gagnant} ont gagné !")
    else :
        root.geometry("910x760")
        message1.configure(text="Pat !")
        message2.configure(text="Égalité !", padx=40)

    message1.grid(row=2, column=8)
    message2.grid(row=3, column=8)



nb_tour = 0
generation_plateau()                    # Création du plateau

d_icones = {}                           # Création du dictionnaire contenant les icones
for i in ["blanc", "noir"] :
    for k in ["roi", "reine", "fou", "cavalier", "tour", "pion"] :
        d_icones[f"ico_{k}_{i}"] = PhotoImage(file=f"{k}_{i}.png")


d_pieces = {}                           # Création du dictionnaire contenant les pièces
for i, k in enumerate(["noir", "blanc"]) :
    d_pieces[f"roi_{k}"] = Roi(k, i*7, 4)
    d_pieces[f"reine_{k}"] = Reine(k, i*7, 3)
    d_pieces[f"fou_{k}_1"] = Fou(k, i*7,2)
    d_pieces[f"fou_{k}_2"] = Fou(k, i*7,5)
    d_pieces[f"cavalier_{k}_1"] = Cavalier(k, i*7, 1)
    d_pieces[f"cavalier_{k}_2"] = Cavalier(k, i*7, 6)
    d_pieces[f"tour_{k}_1"] = Tour(k, i*7, 0)
    d_pieces[f"tour_{k}_2"] = Tour(k, i*7, 7)
    for j in range(1, 9) :
        d_pieces[f"pion_{k}_{j}"] = Pion(k, (i*5)+1, j-1)




root.mainloop()














