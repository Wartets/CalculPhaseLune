import CalculSurfaceVisible as CSV

print('Ce script permet de savoir quel pourcentage de la surface eclairee de la Lune est visible depuis la Terre.')
print('Attention, les conditions initiales de la simulation ne correspondent pas aux conditions initiales reelles, ainsi les resultats peuvent ne pas concorder avec la realite.\n')

cT_out = 2
while True:
    Continuer = True
    oui = Oui = O = 1
    non = Non = N = 0
    while Continuer == True:
        cT_in = input('Voulez vous que la surface totale de la Terre soit consideree comme observatrice ? (oui/non)  ')
        ListO = [0, '0', "0", non, 'non', "non", Non, 'Non', "Non", N, 'N', "N"] # Liste des operateurs "faux"
        ListI = [1, '1', "1", oui, 'oui', "oui", Oui, 'Oui', "Oui", O, 'O', "O"] # Liste des operateurs "vrai"
        ListAll = ListI + ListO
        if cT_in in ListAll: # Verification des entrees
            Continuer = False
            if cT_in in ListO:
                cT_out = 1
            elif cT_in in ListI:
                cT_out == 0
        else:
            Continuer = True
            print("Vous devez necessairement choisir 'oui/Oui/1/O' ou 'non/Non/0/N'.")
            continue

    R = 20 # Pour permettre a l'utilisateur du programme de choisir l'arrondis, il suffis de communter cette ligne avec les suivantes
    # print('\n')
    # Q = 'bye'
    # R = 'hi'
    # while True:
        # print('Combien de chiffres apres la virgule voulez-vous ? (nombre entier positif de 0 a 15)')
        # Q = input()
        # try:
            # val = float(Q).is_integer()
            # if val == True:
                # break
            # else:
                # continue
        # except ValueError:
            # continue
    # R = int(Q)
    
    if cT_out == 1:
        p = CSV.PrctVisReel(1, float(1))
    else :
        p = CSV.PrctVisReel()
    
    print('Dans la simultion, depuis la Terre, ', round(float(p), int(R)), '% de la Lune est eclairee.\n')
    print('~~\n')