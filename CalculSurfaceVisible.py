from numpy import *
from math import *
import GetTime as T


print('Date:',T.temps(4),'(en annee)\n')

# Definition des valeurs
pi = 3.14159265359 #rad
G = 6.67384 * 10**(-11) #m**3 * kg**(-1) * s**(-2)
# Soleil constantes
MagnitudeApparenteSoleil = - 26.832
DiametreMoySoleil = 1392684 #km
RayonEquiSoleil = 696342 #km
AplatissementSoleil = 9 * 10**(- 6)
RayonMoySoleil = RayonEquiSoleil - AplatissementSoleil * RayonEquiSoleil / 2
MasseSoleil = 1.9885 * 10**12 #kg
# Terre constantes
DemiGrandAxeTerre = 149597887.5 #km
ExcentriciteTerre = 0.01671022
PeriodeRevolutionTerre = 365.256363009 #day
InclinaisonTerre = 0 #degre
NoeudAscendantTerre = 174.873 #degre
ArgumentPerihelieTerre = 0 #288.064 #degre
RayonEquiTerre = 6378.137 #km
RayonPolaiTerre = 6356.742 #km
RayonMoyTerre = (RayonEquiTerre + RayonPolaiTerre) / 2
AplatissementTerre = (RayonPolaiTerre - RayonEquiTerre) / RayonPolaiTerre
AlbedoGeoTerre = 0.367
MasseTerre = 5.9736 * 10**24 #kg
DernierPerihelieTerre = 2022.005 * PeriodeRevolutionTerre * 25 * 60 *60 #sec
# Lune constantes
DemiGrandAxeLune = 384399 #km
ExcentriciteLune = 0.05490
PeriodeRevolutionLune = 27.321582 #day
InclinaisonLune = 5.145396 #degre
NoeudAscendantLune = 291.682547 #degre
ArgumentPerihelieLune = 0 #83.35324299 #degre
RayonEquiLune = 1737.4 #km
RayonPolaiLune = 1735.97 #km
RayonMoyLune = (RayonEquiLune + RayonPolaiLune) / 2
AplatissementLune = (RayonPolaiLune - RayonEquiLune) / RayonPolaiLune
AlbedoGeoLune = 0.136
MasseLune = 7.3477 * 10**22 #kg
DernierPerihelieLune = 2022.918 * PeriodeRevolutionTerre * 25 * 60 *60 #sec


# a:demi grand axe
# e:excentricite
# j:ratio periode orbitale (seulemnt pour les satellites)
# psi:sens de rotation (0:sens horraire et 1:sens contraire)
# OMEG:(OMEGA MAJUSCULE) noeud ascendant
# i: inclinaison
# omega:(omega minususcule) argument du periaste
# t:variable temporel 

def ua(km):
    return km / 149597870.7

def ua2(km2):
    return km2 / 149597870.7**2

def km(ua):
    return ua * 149597870.7

def km2(ua2):
    return ua2 * 149597870.7**2

def X(a, e, j, psi, t): # Position en x de l objet sans les rotations
    return - a * (e + sin(pi * psi / 2 + t)) / (1 + e * sin(pi * psi / 2 + j * t)) - a * e

def Y(a, e, j, psi, t): # Position en y de l objet sans les rotations
    return - a * (e + cos(j * t - pi * psi / 2)) / (1 + e * sin(pi * psi / 2 + j * t))    

def Z(): # Position en z de l objet sans les rotations (un peu inutile)
    return 0


def Xrotated(a, e, j, psi, OMEG, i, omega, t): # position en x de l objet apres les rotations
    return cos(OMEG) *  cos(i) * X(a, e, j, psi, t) - sin(OMEG) * cos(omega) * Y(a, e, j, psi, t) + cos(OMEG) * sin(i) * sin(omega) * Y(a, e, j, psi, t)

def Yrotated(a, e, j, psi, OMEG, i, omega, t): # position en y de l objet apres les rotations
    return sin(OMEG) * cos(i) * X(a, e, j, psi, t) + cos(OMEG) * cos(omega) * Y(a, e, j, psi, t) + sin(OMEG) * sin(i) * sin(omega) * Y(a, e, j, psi, t) 

def Zrotated(a, e, j, psi, OMEG, i, omega, t): # position en z de l objet apres les rotations
    return - sin(i) * X(a, e, j, psi, t) + cos(i) * sin(omega) * Y(a, e, j, psi, t)

def CorTemps(DernierPerihelie, Periode, temps = T.day()):
    return (temps - DernierPerihelie) / Periode - pi / 2

def ThetaCalc(x_a, y_a, z_a, x_b, y_b, z_b): # Determination de la valeur de l angle entre les deux calottes selon les coordonnees des deux points observateurs a et b
    return acos((x_a*x_b + y_a * y_b + z_a * z_b) / sqrt((x_a**2 + y_a**2 + z_a**2) * (x_b**2 + y_b**2 + z_b**2)))


def DistPts(x_a, y_a, z_a, x_b, y_b, z_b): # Determination de la distance entre deux points de l espace selon leurs coordonnees
    return sqrt((x_b - x_a)**2 + (y_b - y_a)**2 + (z_b - z_a)**2)

def SurfaceTotale(r):
    return 4 * pi * r**2

def DistanceVisuelle(d, r_1, r_2): # Determination de la distance visuelle qui permet de considerer l observateur comme une sphere de rayon r (r_1 et r_2 sont les rayons des deux sphere et d la distance qui les separes)
    if r_1 < r_2:
        return (d* r_2 + 2 * r_1**2) / (r_2 - r_1)
    else:
        return (d* r_1 + 2 * r_2**2) / (r_1 - r_2)


def RayonCalotteCalc(d, r = 1): # Calcul du rayon de la calote selon la distance d et le rayon r
    phi = 2 * atan(r / (d + r))
    return sqrt(r * (1 - (cos(phi))**2 + r**2 - r))


def SurfaceVisible(a1, a2, r, theta): # Calcul geometrique de la surface visible (formule trop lourde donc decomposee)
    a = asin(a1 / r)
    b = asin(a2 / r)
    c = theta
    s = (a + b + c) / 2
    k = sqrt((sin(s - a) * sin(s - b) * sin(s - c) / sin(s)))
    A = 2 * atan(k / sin(s - a))
    B = 2 * atan(k / sin(s - b))
    C = 2 * atan(k / sin(s - c))
    T1 = r**2 * (A + B + C - pi)
    T2 = T1
    S1 = 2 * B * r**2 * (1 - cos(a))
    S2 = 2 * A * r**2 * (1 - cos(b))
    return S1 + S2 - (T1 + T2)

def TovchigrechkoAndVakser(a1, a2, r, theta):
# Calcul triginometrique de la surface visible
# Methode de l'article de Tovchigrechko et Vakser
# Modifiee pour pouvoir avoir un rayon r different de 1
#a_1 et a_2 sont les rayons des deux cercles de la base des deux calottes et theta est l'angle entre les droite passant par le sommets des calottes et le centre de la sphere de rayon r
    def csc(t):
        return 1 / sin(t)
    def cot(t):
        return 1 / tan(t)
    return r**2 * 2 * (pi 
    - acos(cos(theta) * csc(a1) * csc(a2) - cot(a1) * cot(a2))
    - acos(cos(a2) * csc(theta) * csc(a1) - cot(theta) * cot(a1)) * cos(a1)
    - acos(cos(a1) * csc(theta) * csc(a2) - cot(theta) * cot(a2)) * cos(a2))


# Definition initiale des positions S:Soleil T:Terre L:Lune
xS = 1 # Position en x du Soleil, si cette valeur est changee, le systeme complet sera deplace en fonction
yS = 1 # Position en y du Soleil, si cette valeur est changee, le systeme complet sera deplace en fonction
zS = 1 # Position en z du Soleil, si cette valeur est changee, le systeme complet sera deplace en fonction
xT = 0 # Valeur arbitraire
yT = 0 # Valeur arbitraire
zT = 0 # Valeur arbitraire
xL = 0 # Valeur arbitraire
yL = 0 # Valeur arbitraire
zL = 0 # Valeur arbitraire

# Calcul des positions des objets selon t
# r correspond à l'arrondi des mesures
def PositionTerre(mesure = km, r = 10, retour = 0):
    global xT
    global yT
    global zT
    if mesure == km:
        x = round(Xrotated(DemiGrandAxeTerre, ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day())), r)
        y = round(Yrotated(DemiGrandAxeTerre, ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day())), r)
        z = round(Zrotated(DemiGrandAxeTerre, ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day())), r)
        xT = x + xS
        yT = y + yS
        zT = z + zS
    elif mesure == ua:
        x = round(Xrotated(ua(DemiGrandAxeTerre), ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day())), r +10)
        y = round(Yrotated(ua(DemiGrandAxeTerre), ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day())), r+ 10)
        z = round(Zrotated(ua(DemiGrandAxeTerre), ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day())), r +10)
        xT = x + xS
        yT = y + yS
        zT = z + zS
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")
    if retour == 1:
        print(xT, yT, zT)

def PositionLune(mesure = km, r = 10, retour = 0):
    q = PeriodeRevolutionLune / PeriodeRevolutionTerre
    j = 1 / q
    global xL
    global yL
    global zL
    if mesure == km:
        x = round(Xrotated(DemiGrandAxeTerre, ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day()))
        + Xrotated(DemiGrandAxeLune, ExcentriciteLune, j, 0, InclinaisonLune, NoeudAscendantLune, ArgumentPerihelieLune, CorTemps(DernierPerihelieLune, PeriodeRevolutionTerre, T.day())), r)
        y = round(Yrotated(DemiGrandAxeTerre, ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day()))
        + Yrotated(DemiGrandAxeLune, ExcentriciteLune, j, 0, InclinaisonLune, NoeudAscendantLune, ArgumentPerihelieLune, CorTemps(DernierPerihelieLune, PeriodeRevolutionTerre, T.day())), r)
        z = round(Zrotated(DemiGrandAxeTerre, ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day()))
        + Zrotated(DemiGrandAxeLune, ExcentriciteLune, j, 0, InclinaisonLune, NoeudAscendantLune, ArgumentPerihelieLune, CorTemps(DernierPerihelieLune, PeriodeRevolutionTerre, T.day())), r)
        xL = x + xS
        yL = y + yS
        zL = z + zS
    elif mesure == ua:
        x = round(Xrotated(ua(DemiGrandAxeTerre), ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day()))
        + Xrotated(ua(DemiGrandAxeLune), ExcentriciteLune, j, 0, InclinaisonLune, NoeudAscendantLune, ArgumentPerihelieLune, CorTemps(DernierPerihelieLune, PeriodeRevolutionTerre, T.day())), r + 10)
        y = round(Yrotated(ua(DemiGrandAxeTerre), ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day()))
        + Yrotated(ua(DemiGrandAxeLune), ExcentriciteLune, j, 0, InclinaisonLune, NoeudAscendantLune, ArgumentPerihelieLune, CorTemps(DernierPerihelieLune, PeriodeRevolutionTerre, T.day())), r + 10)
        z = round(Zrotated(ua(DemiGrandAxeTerre), ExcentriciteTerre, 1, 0, InclinaisonTerre, NoeudAscendantTerre, ArgumentPerihelieTerre, CorTemps(DernierPerihelieTerre, PeriodeRevolutionTerre, T.day()))
        + Zrotated(ua(DemiGrandAxeLune), ExcentriciteLune, j, 0, InclinaisonLune, NoeudAscendantLune, ArgumentPerihelieLune, CorTemps(DernierPerihelieLune, PeriodeRevolutionTerre, T.day())), r + 10)
        xL = x + xS
        yL = y + yS
        zL = z + zS
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")
    if retour == 1:
        print(xL, yL, zL)

def PositionSoleil(mesure = km, r = 0, retour = 0):
    if retour == 1:
        return (xS, yS, zS)

# Calcul des distances entre les objets
def DistanceTL(mesure = km, r = 40, retour = 0):
    PositionTerre(mesure, r, retour)
    PositionLune(mesure, r, retour)
    return DistPts(xT, yT, zT, xL, yL, zL)

def DistanceSL(mesure = km, r = 40, retour = 0):
    PositionSoleil(mesure, r, retour)
    PositionLune(mesure, r, retour)
    return DistPts(xS, yS, zS, xL, yL, zL)

def DistanceST(mesure = km, r = 40, retour = 0):
    PositionSoleil(mesure, r, retour)
    PositionTerre(mesure, r, retour)
    return DistPts(xS, yS, zS, xT, yT, zT)

# Calcul des distances visuelles entre les objets
def DistVisTL(mesure = km, r = 40, retour = 0): # distance visuelle Terre-Lune
    if mesure == km:
        d = DistanceTL(mesure, r, retour)
        return DistanceVisuelle(d, RayonMoyLune, RayonMoyTerre)
    elif mesure == ua:
        d = DistanceST(mesure, r, retour)
        return DistanceVisuelle(d, ua(RayonMoyLune), ua(RayonMoyTerre))
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")

def DistVisSL(mesure = km, r = 40, retour = 0): # distance visuelle Soleil-Lune
    if mesure == km:
        d = DistanceSL(mesure, r, retour)
        return DistanceVisuelle(d, RayonMoySoleil, RayonMoyLune)
    elif mesure == ua:
        d = DistanceSL(mesure, r, retour)
        return DistanceVisuelle(d, ua(RayonMoySoleil), ua(RayonMoyLune))
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")

def DistVisST(mesure = km, r = 40, retour = 0): # distance visuelle Soleil-Terre
    if mesure == km:
        d = DistanceST(mesure, r, retour)
        return DistanceVisuelle(d, RayonMoySoleil, RayonMoyTerre)
    elif mesure == ua:
        d = DistanceST(mesure, r, retour)
        return DistanceVisuelle(d, ua(RayonMoySoleil), ua(RayonMoyTerre))
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")

# Calcul de l angle theta Terre-Lune-Soleil
def ThetaTLS(mesure = km, r = 40, retour = 0):
    PositionTerre(mesure, r, retour)
    PositionLune(mesure, r, retour)
    return ThetaCalc(xT, yT, zT, xS, yS, zS)

# Calcul de l angle theta Lune-Soleil-Terre
def ThetaLST(mesure = km, r = 40, retour = 0):
    PositionTerre(mesure, r, retour)
    PositionLune(mesure, r, retour)
    return ThetaCalc(xT, yT, zT, xL, yL, zL)

# Calcul de l angle theta Lune-Terre-Soleil
def ThetaLTS(mesure = km, r = 40, retour = 0):
    PositionTerre(mesure, r, retour)
    PositionLune(mesure, r, retour)
    return ThetaCalc(xL, yL, zL, xS, yS, zS)


dq = 0
# Calcul des rayons de calote Terre-Lune et Soleil-Lune
def RayonCalotteTL(complet = 1, mesure = km, r = 40, retour = 0):
    global dq
    if complet == 1:  # Terre(complete)-Lune
        dq = float(DistVisTL(km, r, retour))
    else :  # Terre(non-complete)-Lune
        dq = float(DistanceTL(km, r, retour))
    # else:
        # print("Erreur: Vous devez choisir '1' ou '0'")
    
    if mesure == km:
        return RayonCalotteCalc(dq, RayonMoyLune)
    elif mesure == ua:
        return ua(RayonCalotteCalc(dq, RayonMoyLune))
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.") 

def RayonCalotteSL(complet = 1, mesure = km, r = 40, retour = 0):
    global dq
    if complet == 1:  # Soleil(complete)-Lune
        dq = float(DistVisSL(km, r, retour))
    elif complet == 0 :  # Soleil(non-complete)-Lune
        dq = float(DistanceSL(km, r, retour))
    else:
        print("Erreur: Vous devez choisir '1' ou '0'")
    
    if mesure == km:
        return RayonCalotteCalc(dq, RayonMoyLune)
    elif mesure == ua:
        return ua(RayonCalotteCalc(dq, RayonMoyLune))
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.") 

def TAV_Lune(completTerre = 0, completSoleil = 1, mesure = km, r = 40, retour = 0):
    theta = ThetaTLS(km, r, retour)
    a1 = RayonCalotteSL(completSoleil, km, r, retour)
    a2 = RayonCalotteTL(completTerre, km, r, retour)
    r = RayonMoyLune
    if mesure == km:
        return TovchigrechkoAndVakser(a1, a2, r, theta) # km**2
    elif mesure == ua:
        return ua2(TovchigrechkoAndVakser(a1, a2, r, theta)) # ua**2
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")

def SV_Lune(completTerre = 0, completSoleil = 1, mesure = km, r = 40, retour = 0):
    theta = ThetaTLS(km, r, retour)
    a1 = RayonCalotteSL(completSoleil, km, r, retour)
    a2 = RayonCalotteTL(completTerre, km, r, retour)
    r = RayonMoyLune
    if mesure == km:
        return SurfaceVisible(a1, a2, r, theta) # km**2
    elif mesure == ua:
        return ua2(SurfaceVisible(a1, a2, r, theta)) # ua**2
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")

def SurfaceTotaleLune(mesure = km):
    if mesure == km:
        return SurfaceTotale(RayonMoyLune) # km**2
    elif mesure == ua:
        return ua2(SurfaceTotale(RayonMoyLune)) # ua**2
    else:
        print("Erreur: Vous devez choisir l'unite de mesure, 'ua' ou 'km'.")

def PrctVisTotal(completTerre = 0, completSoleil = 1, mesure = km, r = 40, retour = 0):
    return 1 - TAV_Lune(completTerre, completSoleil, km, r, retour) / SurfaceTotaleLune(km)

def SurfaceVisbleDeA(d, r_a, r_b, complet): # r_a le rayon de la sphere observee
    if complet == 1:
        return 2 * pi * r_a**2 * (d + 2 * r_b) / (d + r_a + r_b)
    elif complet == 0:
        return 2 * pi * d * r_a**2 / (d + r_a)
    else:
        print('erreur')

def PrctVisReel(completTerre = 0, completSoleil = 1):
    dtl = float(DistanceTL(km, 40, 0))
    return 100 * float((SurfaceVisbleDeA(dtl, RayonMoyLune, RayonMoyTerre, completTerre)) / float(TAV_Lune(completTerre, completSoleil, km, 40, 0)))

def PrctVisReelSV(completTerre = 0, completSoleil = 1):
    dtl = float(DistanceTL(km, 40, 0))
    return 100 * float((SurfaceVisbleDeA(dtl, RayonMoyLune, RayonMoyTerre, completTerre)) / float(SV_Lune(completTerre, completSoleil, km, 40, 0)))