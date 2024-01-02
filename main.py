from flask import Flask, request, render_template, redirect, url_for 
import math 
import re
from PIL import Image, ImageDraw

#Initialisation du serveur
app = Flask('app')

#Initialisation d'un message d'erreur
#Il n'y a pas d'erreur donc le message est vide
erreur = ""

#Pour l'instant, on affiche pas l'image
afficherImg = False

@app.route("/")
def initialisation():
    """
    Initialisation de la page HTML index.html
    Cette fonction permet de renvoyer cette page à l’utilisateur
    """
    return render_template("index.html", erreur=erreur)

@app.route('/traitement/', methods=["POST"])
def verification():
    """
    Cette fonction vérifie si les données reçues du
    formulaire sont correctes
    Si oui, elle renvoie la page HTML sans erreur
    Si non, elle renvoie la page HTML avec une erreur
    """
    #Récupération des données du formulaire
    forme = request.form["forme"]
    rayure = request.form["rayure"]
    nbCouleur = request.form["nbCouleur"]
    longueur = request.form["longueur"]
    hauteur = request.form["hauteur"]
    couleur1 = request.form["couleur1"]
    couleur2 = request.form["couleur2"]
    couleur3 = request.form["couleur3"]
    objet = request.form["objet"]
    couleurObjet = request.form["couleurObjet"]

    #On suppose qu'on affiche pas l'image
    #Tant que tous les tests ne sont pas fait
    afficherImg = False

    #Erreur dans la saisie de la forme
    if not forme :
        erreur = "Entrez une forme valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la rayure
    if not rayure and forme == "cercle":
        erreur = "Vous avez choisi un cercle, mais avec ou sans rayure ?"
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie du nombre de couleur
    if not nbCouleur:
        erreur = "Entrez un nombre de couleur valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la longueur
    if not longueur:
        erreur = "Entrez une longueur valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la hauteur
    if not hauteur:
        erreur = "Entrez une hauteur valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de l'objet
    if not objet:
        erreur = "Entrez un objet valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la couleur de l'objet
    if not couleurObjet and objet != "rien":
        erreur = "Entrez une couleur valide pour l'objet."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la couleur1
    if not couleur1:
        erreur = "Entrez une couleur 1 valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la couleur2
    if not couleur2 and (nbCouleur == "nb2" or nbCouleur == "nb3"):
        erreur = "Entrez une couleur 2 valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Erreur dans la saisie de la couleur1
    if not couleur2 and nbCouleur == "nb3":
        erreur = "Entrez une couleur 3 valide."
        return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    #Vérification si la/les couleurs transmises sont valides
    if nbCouleur == "nb1":
        if not is_valid_color(couleur1):
            erreur = "Entrez une couleur 1 valide."
            return render_template("index.html", erreur=erreur, afficherImg=afficherImg)
    elif nbCouleur == "nb2":
        if not is_valid_color(couleur1) or not is_valid_color(couleur2):
            erreur = "Entrez une couleur 1 et une couleur 2 valides."
            return render_template("index.html", erreur=erreur, afficherImg=afficherImg)
    else:
        if not is_valid_color(couleur1) or not is_valid_color(couleur2) \
        or not is_valid_color(couleur3):
            erreur = "Entrez une couleur 1, une couleur 2 et une couleur 3 valides."
            return render_template("index.html", erreur=erreur, afficherImg=afficherImg)

    erreur = ""
    afficherImg = True
    creation()
    return render_template('index.html', erreur=erreur, afficherImg=afficherImg)

def is_valid_color(color):
    """
    Cette fonction vérifie si la couleur en
    hexadécimal est correct
    Si c’est vrai, elle renvoie vraie
    Sinon, elle renvoie faux
    """
    # Utilise une expression régulière pour valider la couleur (format hexadécimal)
    color_regex = "^#[0-9A-Fa-f]{6}$"
    return re.match(color_regex, color)

def hex_to_rgb(hex_color):
    """
    Fonction qui convertit une couleur
    en code hexadécimal en code RGB sous la forme
    d'un tuple.
    La fonction est récursif en utilisant 
    convert_hex_to_rgb.
    """
    #On retire le caractère # dans la chaîne de caractères
    hex_color = hex_color.lstrip('#')

    #On vérifie si la couleur n'a que 3 caractères
    #Si oui, on ajoute le même chiffre à côté, A --> AA
    if len(hex_color) == 3:
        hex_color = ''.join([char * 2 for char in hex_color])

    #Utilisation d'une fonction récursif pour convertir le code
    def convert_hex_to_rgb(hex_value):
        #Si la chaîne est vide, on renvoie le tuple
        if not hex_value:
            return ()
        #Sinon, on convertie les 2 premiers bits puis on les retire
        #en réutilisant la même fonction
        else:
            return (int(hex_value[0:2], 16),) + convert_hex_to_rgb(hex_value[2:])

    rgb_color = convert_hex_to_rgb(hex_color)

    return rgb_color

def creation():
    """
    Cette fonction permet de créer un fichier image
    en fonction des données saisies par l'utilisateur
    """
    #Récupération des données du formulaire
    forme = request.form["forme"]
    rayure = request.form["rayure"]
    nbCouleur = request.form["nbCouleur"]
    longueur = request.form["longueur"]
    hauteur = request.form["hauteur"]
    couleur1 = request.form["couleur1"]
    couleur2 = request.form["couleur2"]
    couleur3 = request.form["couleur3"]
    objet = request.form["objet"]
    couleurObjet = request.form["couleurObjet"]

    #Création de la liste de couleurs
    if nbCouleur == "nb1" and forme != "cercle":
        listColor = [hex_to_rgb(couleur1)]
    elif nbCouleur == "nb2" or forme == "cercle":
        listColor = [hex_to_rgb(couleur1), hex_to_rgb(couleur2)]
    else:
        listColor = [hex_to_rgb(couleur1), hex_to_rgb(couleur2), hex_to_rgb(couleur3)]
        
    #Utilisation de la classe Drapeau pour créer l'image
    monDrapeau = Drapeau(int(longueur), int(hauteur),\
                         listColor, (int(longueur)/2, int(hauteur)/2))

    #Drapeau vertical
    if forme == "vertical":
        monDrapeau.genererDrapeauVertical()
    #Drapeau horizontal
    elif forme == "horizontal":
        monDrapeau.genererDrapeauHorizontal()
    #Drapeau avec un cercle
    else:
        if rayure == "avec":
            rayure = True
        else:
            rayure = False
        monDrapeau.genererDrapeauCercle(rayure)

    #Drapeau avec un objet
    couleurObjet = hex_to_rgb(couleurObjet)
    #Ajout d'une étoile
    if objet == "etoile":
        monDrapeau.genererDrapeauEtoile(couleurObjet)
    #Ajout d'un croissant
    elif objet == "croissant":
        monDrapeau.genererDrapeauCroissant(couleurObjet)
    #Ajout d'un triangle
    elif objet == "triangle":
        monDrapeau.genererDrapeauTriangle(couleurObjet)

    #Génération de l'image
    print(monDrapeau)

class Drapeau:
    def __init__(self, longueur, hauteur, listColor, poly = None, name="drapeau"):
        self.name = name
        self.longueur = longueur
        self.hauteur = hauteur
        self.listColor = listColor
        self.poly = poly
        self.image = Image.new('RGB',(longueur,hauteur))

    def __repr__(self):
        self.image.save("static/" + self.name + ".png")
        return "<" + str(self.longueur) + "*" + str(self.hauteur) + " with colors" \
        + str(self.listColor) + ">"


    def genererDrapeauVertical(self):
        """
        Fonction qui créer un drapeau de taille longueur X hauteur,
        avec une liste de couleurs sous forme de tuple en RGB.
        Les couleurs seront en verticales comme sur le drapeau français.
        """
        assert len(self.listColor) >= 1
        nombreRayure = len(self.listColor)
        for x in range(self.longueur):
            for y in range(self.hauteur):
    
                a = (x/self.longueur)*nombreRayure
                indice = int(a) % nombreRayure   
                self.image.putpixel((x,y),self.listColor[indice])


    def genererDrapeauHorizontal(self):
        """
        Fonction qui créer un drapeau de taille longueur X hauteur,
        avec une liste de couleurs sous forme de tuple en RGB.
        Les couleurs seront en horizontales comme sur le drapeau allemand.
        """
        assert len(self.listColor) >= 1
        nombreRayure = len(self.listColor)
        for x in range(self.longueur):
            for y in range(self.hauteur):
    
                a = (y/self.hauteur)*nombreRayure
                indice = int(a) % nombreRayure   
                self.image.putpixel((x,y),self.listColor[indice])

    def genererDrapeauCercle(self, rayureAutour):
        """
        Fonction qui créer un drapeau de taille longueur X hauteur,
        avec avec 2 couleurs sous forme de tuple en RGB.
        La première couleur sera le cercle et la deuxième couleur le fond, 
        comme sur le drapeau japonais.
        Si on met à vrai rayureAutour, alors il y aura 30 rayures autour du cercle
        """
        assert len(self.listColor) >= 2
        color1 = self.listColor[0]
        color2 = self.listColor[1]
        centreO = (self.longueur/2, self.hauteur/2)
        rayon = self.longueur/10
    
        for x in range(self.longueur):
            for y in range(self.hauteur):
                point = (x-centreO[0],y-centreO[1])
                d2 = point[0]**2 + point[1]**2
    
                if d2 <= rayon**2:
                    self.image.putpixel((x,y),color1)
                else:
                    if not rayureAutour:
                        self.image.putpixel((x,y),color2)
                    else:
                        # -pi <= theta < pi
                        theta = math.atan2(point[0],point[1])
                        #Nous voulons 30 rayures autour du cercle
                        # 0 <= ((theta/pi + 1)/2)*30 < 30
                        theta = (((theta/math.pi) + 1)/2)*30
                        if int(theta) % 2 == 0:
                            self.image.putpixel((x,y),color1)
                        else:
                            self.image.putpixel((x,y),color2)

    #Je vais modifier cette fonction plus tard
    #Elle comporte de nombreux problèmes
    def genererDrapeauTriangle(self, colorPoly):
        """
        Fonction qui créer un drapeau de taille longueur X hauteur,
        avec 1 couleur colorPoly sous forme de tuple en RGB.
        La fonction crée un triangle sur le côté gauche.
        """
        assert len(self.listColor) >= 1
        draw = ImageDraw.Draw(self.image)
        listCoorPoly = [(0, 0), (self.longueur / 2, self.hauteur/2), (0, self.hauteur)]
    
        # Remplir le triangle avec la couleur
        draw.polygon(listCoorPoly, fill=colorPoly)

    def genererDrapeauEtoile(self, colorPoly):
        """
        Fonction qui créer un drapeau de taille longueur X hauteur,
        avec 1 couleur colorPoly sous forme de tuple en RGB.
        La fonction crée une étoile à 5 branches en la
        plaçant au milieu.
        Cette fonction est récursive en utilisant
        genererDrapeauEtoileRec.
        Cette fonction va être répéter 5 fois pour faire
        les 5 branches.
        """
        assert self.poly != None
        draw = ImageDraw.Draw(self.image)
    
        # Dessiner l'étoile
        radius_outer = min(self.longueur, self.hauteur) // 4
        radius_inner = radius_outer // 2
        def genererDrapeauEtoileRec(self, colorPoly, radius_outer, radius_inner, i=0):
            if i == 5:
                return None
            else:
                angle1 = math.radians(90 + i * 360 / 5)
                angle2 = math.radians(90 + (i + 2) * 360 / 5)
                x1_outer = self.poly[0] + radius_outer * math.cos(angle1)
                y1_outer = self.poly[1] - radius_outer * math.sin(angle1)
                x2_outer = self.poly[0] + radius_outer * math.cos(angle2)
                y2_outer = self.poly[1] - radius_outer * math.sin(angle2)
    
                angle3 = math.radians(90 + (i + 1) * 360 / 5)
                angle4 = math.radians(90 + (i + 3) * 360 / 5)
                x1_inner = self.poly[0] + 0.6 * radius_inner * math.cos(angle3)
                y1_inner = self.poly[1] - 0.6 * radius_inner * math.sin(angle3)
                x2_inner = self.poly[0] + 0.6 * radius_inner * math.cos(angle4)
                y2_inner = self.poly[1] - 0.6 * radius_inner * math.sin(angle4)
    
                draw.polygon([(self.poly[0], self.poly[1]), \
                              (x1_outer, y1_outer), (x1_inner, y1_inner), \
                              (x2_outer, y2_outer), \
                              (x2_inner, y2_inner)], fill=colorPoly)
                return genererDrapeauEtoileRec(self, colorPoly, \
                                        radius_outer, radius_inner, i+1)
    
        genererDrapeauEtoileRec(self, colorPoly, radius_outer, radius_inner)

    def genererDrapeauCroissant(self, colorPoly):
        """
        Fonction qui créer un drapeau de taille longueur X hauteur,
        avec 1 couleur colorPoly sous forme de tuple en RGB.
        La fonction crée un croissant en la
        plaçant au milieu.
        Nous utiliserons la fonction appartientCercle qui renvoie
        vrai si un point appartient à un cercle, faux sinon.
        Nous utiliserons aussi la fonction appartientCroissant qui
        renvoie vrai si un point appartient à un croissant, faux sinon.
        """
        
        def appartientCercle(xP, yP, xC, yC, r):
            #Nous réutiliserons la formule si un P appartient à un cercle
            #sous la forme d'une fonction arithmétique
            formule = lambda x1, y1, x2, y2: (x2 - x1) ** 2 + (y2 - y1) ** 2
            return formule(xP, yP, xC, yC) <= r ** 2

        def appartientCroissant(xP, yP, xC1, yC1, xC2, yC2, r):
            #On détermine si le point P appartient au croissant
            cercle1 = appartientCercle(xP, yP, xC1, yC1, r)
            cercle2 = appartientCercle(xP, yP, xC2, yC2, r)
            #Si le point appartient au premier cercle et pas au deuxième cercle
            #alors le point P appartient au croissant
            if cercle1 and not cercle2:
                return True
            else:
                return False

        #Nous allons déterminer les coordonnées de 2 cercles avec un rayon longueur/11
        rayon = self.longueur/11
        x1 = self.longueur/2
        y1 = self.hauteur/2
        x2 = self.longueur/2 + math.sin(math.pi/2)*(rayon-30)
        y2 = self.hauteur/2 + math.cos(math.pi/2)*(rayon-30)
        #Puis on vérifie chaques pixels pour savoir si ils appartiennent à un croissant
        for x in range(self.longueur):
            for y in range(self.hauteur):
                if appartientCroissant(x, y, x1, y1, x2, y2, rayon):
                    self.image.putpixel((x, y), colorPoly)
    
#Configuration du port pour le localhost
app.run(host='0.0.0.0', port=8080)
