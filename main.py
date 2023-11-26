import fonctions
import time

# ************* MENU **************
in_menu = True
# boucle tant que l'on a pas fermé le menu
while in_menu:
    print("\n\n ********* Bonjour, bienvenue dans le menu *********")
    print("\t-Si vous souhaitez fermer le menu entrez 1")
    print("\t-Si vous souhaitez connaitre le nom du premier président à avoir parlé d'écologie, entrez 2")
    print("\t-Si vous souhaitez connaitre le mot le plus répété par un certain président, entrez 3")
    print("\t-Si vous souhaitez connaître le nom du président à avoir le plus répété un certain mot, entrez 4")
    print("\t-Si vous souhaitez le nom du premier président à avoir parlé d'écologie, entrez 5")
    user_input = input("\nSaisissez le numéro de l'action que vous souhaitez exécuter : ")
    time.sleep(2)
    if user_input == '1':
        in_menu = False  # fin de la boucle, fin du menu
    elif user_input == '2':
        pass
    elif user_input == '3':
        word = input("\nSaisissez le mot dont il est question : ")
        resultat = fonctions.word_most_used(word, fonctions.files_name_list, fonctions.tf_score_dict)
        print(f"\n\n-----Le président {resultat}, est le président ayant le plus répété le mot ~{word}~ lors de son discour d'inverstiture-----")
    elif user_input == '4':
        pass
    elif user_input == '5':
        pass
    else:
        print("\t\t*** ERREUR DE SAISIE ***")
        print("La valeur que vous avez saisie n'est pas valide !")
        time.sleep(4)
        print("\nRetour au menu principale.")
        time.sleep(2)

