from fonctions import *


# ***** PREREQUIS *****
directory = "./speeches"
cleaned_directory = directory+"_cleaned"
files_name_list = list_of_files(directory, "txt")
tfidf_list = matrice_TF_IDF(cleaned_directory)
tf_score_dict = tf_score(cleaned_directory)

# ***** APPEL DES FONCTIONS *****

# >>>> FONCTIONNALITE 1
list_of_useless_words = useless_word_list(tfidf_list)
# cette fonction retourne la liste des mots inutiles du corpus (les mots avec un tfidf nul),
# c'est à dire les mots qui apparaissent dans tous les documents.

# >>>> FONCTIONNALITE 2
list_of_best_tfidf = best_tfidf(tfidf_list)
# cette fonction donne la liste des 20 mots avec le tfidf le plus élevé

# >>>> FONCTIONNALITE 3
list_of_most_used_words = most_used_words_by_president("Chirac", files_name_list, tf_score_dict)
# cette fonction renvoie la liste des mots les plus répétés par un président

# >>>> FONCTIONNALITE 4
president_used_most = word_most_used("nation", files_name_list, tf_score_dict)
# fonction qui renvoie le président ayant utilisé le plus de fois un mot choisi
president_used_most_list = word_used("nation", files_name_list, tf_score_dict)
# fonction qui renvoie la liste des présidents ayant utilisé le plus de fois un mot choisi

# >>>> FONCTIONNALITE 5
president_green = green_president(files_name_list, tf_score_dict)
# fonction qui renvoie le premier président ayant parlé d'écologie


# ***** AFFICHAGE DES FONCTIONNALITES *****

print("\n===== TEST DES FONCTIONS =====")
print("\n> voici la liste des mots inutiles dans le corpus :")
print(list_of_useless_words, "\n")
print("\n> voici la liste des mots les plus récurrents du corpus (meilleur tf score) :")
print(list_of_best_tfidf)
print("\n> voici la liste des mots les plus répétés par un président :")
print(list_of_most_used_words)
print("\n> voici le président ayant le plus répèté le mot 'nation', puis la liste des présidents qui ont utilisé le mot")
print(president_used_most)
print(president_used_most_list)
print("\n> le premier président ayant parlé de climat et d'écologie :")
print(president_green)
