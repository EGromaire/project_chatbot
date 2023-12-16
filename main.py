
from fonctions import *
import time


####################################################################################################################
# *************************************** Call of the function ****************************************************#

# *****
directory = "./speeches"
cleaned_directory = "./cleaned"
files_name_list = list_of_files(directory, "txt")
presidents_names = extracted_names_list(files_name_list)

# ***** Nettoyage des fichiers *****
cleaning_files(files_name_list)


presidents_names = add_first_name(presidents_names)
print_names(presidents_names)


# ***** ajout de tout les mots du corpus dans une liste *****
words = words_of_directory(cleaned_directory)
all_words_list = words[0]
presidents_words_list = words[1]

# ***** calcule de la matrice TF-IDF *****
idf_score = idf_score(cleaned_directory)
tf_score = tf_score(cleaned_directory)
tfidf_list = matrice_TF_IDF(cleaned_directory)

tf_score_dict = tf_score(cleaned_directory)
idf_score_dict = idf_score(cleaned_directory)

lists_without_useless_words = remove_useless_words_from_matrice(tfidf_list, useless_word_list(tfidf_list))
tfidf_list_without_useless_words = lists_without_useless_words[0]
all_words_list_without_useless_words = lists_without_useless_words[1]
print("Voici la matrice TF-IDF", tfidf_list)
#print("Voici les mots ayants les meilleurs TF-IDF :", best_tfidf(tfidf_list))


# ***** Fonctionnalités suplémentaires *****
#print_names(extracted_names_list(word_used('nation', files_name_list, tf_score_dict)))
#print(word_most_used('nation', files_name_list, tf_score_dict))
#print(useless_word_list(tfidf_list))


# ***************** Traitement de la phrase entré par l'utilisateur *************************
sentence = question_to_list("école droits pacte nation")
print(sentence)
sentence_tf = tf_list(sentence, all_words_list_without_useless_words, len(files_name_list))
sentence_tfidf =sentence_tf_idf(sentence_tf, all_words_list_without_useless_words, idf_score)
print(sentence_tf)
print("Voici le tf idf de la phrase", sentence_tfidf)
print(pertinent_file(tfidf_list_without_useless_words, sentence_tfidf, files_name_list))
print(refine_answer())

# ************* MENU **************
in_menu = True
# boucle tant que l'on a pas fermé le menu
while in_menu:
    print("\n\n\t\t\t ********* Bonjour, bienvenue dans le menu *********")
    print("\t-Si vous souhaitez fermer le menu entrez 1")
    print("\t-Si vous souhaitez accéder aux fonctionnalités de base entrez 2")
    print("\t-Si vous souhaitez accéder au chatbot entrez 3")
    user_input = input("\nSaisissez le numéro de l'action que vous souhaitez exécuter : ")
    if user_input == '1':
        in_menu = False  # fin de la boucle, fin du menu

    # ***** fonctionnalités de base *****
    elif user_input == 1:
        print("\t-Si vous souhaitez connaitre le nom du premier président à avoir parlé d'écologie, entrez 1")
        print("\t-Si vous souhaitez connaitre les mots les plus répétés par un certain président, entrez 2")
        print("\t-Si vous souhaitez connaître le nom du président à avoir le plus répété un certain mot, entrez 3")
        user_input = input("\nSaisissez le numéro de l'action que vous souhaitez exécuter : ")
        time.sleep(2)
        if user_input == '1':
            print(f"{green_president(files_name_list, tf_score_dict)} est le tout premier président à avoir parlé d'écologie et de climat.")
        elif user_input == '2':
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
        elif user_input == '3':
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

