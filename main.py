from fonctions import *
import time


####################################################################################################################
# *************************************** Call of the function ****************************************************#
directory = "./speeches"
cleaned_directory = "./cleaned"
files_name_list = list_of_files(directory, "txt")
presidents_names = extracted_names_list(files_name_list)
#print(presidents_names)
presidents_names = add_first_name(presidents_names)
tf_score_dict = tf_score(cleaned_directory)
idf_score_dict = idf_score(cleaned_directory)
print_names(presidents_names)

# **** Nettoyage des fichiers *****
cleaning_files(files_name_list)

# ***** ajout de tout les mots du corpus dans une liste *****
words = words_of_directory(cleaned_directory)
all_words_list = words[0]
presidents_words_list = words[1]

# ***** calcule de la matrice TF-IDF *****
tfidf_list = matrice_TF_IDF(cleaned_directory)
print("Voici la matrice TF-IDF", tfidf_list)
#print("Voici les mots ayants les meilleurs TF-IDF :", best_tfidf(tfidf_list))


# ***** Fonctionnalités suplémentaires *****
#print_names(extracted_names_list(word_used('nation', files_name_list, tf_score_dict)))
#print(word_most_used('nation', files_name_list, tf_score_dict))
#print(useless_word_list(tfidf_list))


# test fonctions

sentence = question_to_list("Bonjour, j'aimerais savoir, quel était le président qui c'est le plus interressé à l'écologie ?")
print(sentence)


# ************* MENU **************
in_menu = True
# boucle tant que l'on a pas fermé le menu
while in_menu:
    print("\n\n\t\t\t ********* Bonjour, bienvenue dans le menu *********")
    print("\t-Si vous souhaitez fermer le menu entrez 1")
    print("\t-Si vous souhaitez connaitre le nom du premier président à avoir parlé d'écologie, entrez 2")
    print("\t-Si vous souhaitez connaitre les mots les plus répétés par un certain président, entrez 3")
    print("\t-Si vous souhaitez connaître le nom du président à avoir le plus répété un certain mot, entrez 4")
    user_input = input("\nSaisissez le numéro de l'action que vous souhaitez exécuter : ")
    time.sleep(2)
    if user_input == '1':
        in_menu = False  # fin de la boucle, fin du menu
    elif user_input == '2':
        print(f"{f.green_president(files_name_list, tf_score_dict)} est le tout premier président à avoir parlé d'écologie et de climat.")
    elif user_input == '3':
        print("\nExemple de saisie possible : Chirac")
        president = input("Saisissez le nom de famille du président dont il est question : ")
        if president in presidents_names:
            result_words = most_used_words_by_president(president, files_name_list, tf_score_dict)
            print(f"Voici les 10 mots les plus employé par la président {president} : ")
            for word in result_words:
                print(f"\t\t-{word}")
        else:
            print("\t\t*** ERREUR DE SAISIE ***")
            print("Aucune information relative au président que vous avez saisi.")
    elif user_input == '4':
        word = input("\nSaisissez le mot dont il est question : ")
        if word in tf_score_dict.keys():
            resultat = word_most_used(word, files_name_list, tf_score_dict)
            print(f"\n\n-----Le président {resultat}, est le président ayant le plus répwété le mot ~{word}~ lors de son discour d'inverstiture-----")
        else:
            print("Ce mot n'a jamais été employé par aucun président")
    else:
        print("\t\t*** ERREUR DE SAISIE ***")
        print("La valeur que vous avez saisie n'est pas valide !")

    if in_menu:
        time.sleep(3)
        print("\nRetour au menu principale.")
        time.sleep(2.5)

