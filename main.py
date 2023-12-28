from flask import Flask, request, render_template, redirect, url_for
import math
from PIL import Image, ImageDraw



@app.route("/")
def home():
    return render_template("isfates.html")


@app.route("/", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)

def verifier_formulaire():
    if request.method == 'POST':
        couleur1 = request.form['couleur1']
        couleur2 = request.form['couleur2']
        couleur3 = request.form['couleur3']
        forme = request.form['forme']

        # Validation de la couleur1
        if not is_valid_color(couleur1):
            return "Entrez une couleur valide pour Couleur 1."

        # Validation de la couleur2
        if not is_valid_color(couleur2):
            return "Entrez une couleur valide pour Couleur 2."

        # Validation de la couleur3
        if not is_valid_color(couleur3):
            return "Entrez une couleur valide pour Couleur 3."

        # Validation de la forme
        formes_drapeau = ["carré", "cercle", "triangle"]
        if forme not in formes_drapeau:
            return "Sélectionnez une forme valide."

    return render_template('isfates.html')

def is_valid_color(color):
    # Utilise une expression régulière pour valider la couleur (format hexadécimal)
    color_regex = "^#[0-9A-Fa-f]{6}$"
    return re.match(color_regex, color)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')

    if len(hex_color) == 3:
        hex_color = ''.join([char * 2 for char in hex_color])

    def convert_hex_to_rgb(hex_value):
        if not hex_value:
            return ()
        else:
            return (int(hex_value[0:2], 16),) + convert_hex_to_rgb(hex_value[2:])

    rgb_color = convert_hex_to_rgb(hex_color)

    return rgb_color


# Exemple d'utilisation
hex_color = '#1a2b3c'
rgb_color = hex_to_rgb(hex_color)

print(f"Couleur hexadécimale : {hex_color}")
print(f"Couleur RGB : {rgb_color}")


class Drapeau:
    def __init__(self, longueur, hauteur, listColor, poly = None, name="drapeau"):
        self.name = name
        self.longueur = longueur
        self.hauteur = hauteur
        self.listColor = listColor
        self.poly = poly
        self.image = Image.new('RGB',(longueur,hauteur))

    def __repr__(self):
        self.image.save(self.name + ".png")
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
    

#Le png est sauvegardé dans les fichiers à gauche
#Je vais prochainement modifier mes fonctions, pour quelles soient plus personnalisable,
#Plus optimisé, en utilisant lambda, et aussi utiliser la récursivité
print("Veuillez patienter...")
color1 = (0, 0, 0) #noir
color2 = (255, 0, 0) #rouge
color3 = (255, 204, 0) #jaune-doré
MonDrapeau = Drapeau(500, 300, [color2], (500/2, 300/2))
MonDrapeau.genererDrapeauVertical()
MonDrapeau.genererDrapeauEtoile(color3)
print(MonDrapeau)
print("Drapeau crée")
