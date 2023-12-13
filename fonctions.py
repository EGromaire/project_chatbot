import os
import math
import random
import time


def tri_selection(liste:list):
    for i in range(len(liste)):
        # Trouver le minimum de la sous-liste
        min = i
        for j in range(i + 1, len(liste)):
            if liste[min] > liste[j]:
                min = j
        # mettre le minimum en première position
        liste[i], liste[min] = liste[min], liste[i]
    return liste


def split_char(string: str, char: str) -> list:
    """
    FONCTION split_char
    :param string: chaine de caractère
    :param char: séparateurs
    :return: listes de chaines de caractères correspondants à la chaine de caractère (string) divisé par un séparateur (char)
    """
    word = ''
    words_list = []
    for letter in string:
        if letter == char or letter == '\n':
            words_list.append(word)
            word = ''
        else:
            word += letter
    return words_list


def replace_char(string: str, char: str, instead: str) -> str:
    """
    FONCTION replace_char
    :param string: str - chaine de caractères dans
    :param char: str
    :param instead: str
    :return new_string
    renvoie une chaine de caractères (string) dans laquelle toutes les occurrences d'une chaine
    de caractères (char) a été remplacé par une autre chaine (instead)
    """
    new_string = ''  # chaine de caractères dans laquelle toutes les occurrences de 'char' sont remplacées par 'instead'
    i_string = 0  # indice associé à la chaine de caractère string
    while i_string < len(string):  # on parcourt la chaine de caractère de
        if string[i_string] != char[0]:  # si le caractère parcouru est différent, on ajoute le caractère à 'new_string'
            new_string += string[i_string]
            i_string += 1  # on incrémente de 1 afin de parcourir chaque caractère de 'string' un à un
        else:
            i_char = 1  # initialisation de l'indice permettant le parcours de la chaine de caractère 'char'

            # boucle vérifiant s'il y a une occurrence de la chaine de caractères 'char'
            # à l'indice de string 'i_string' auquel on se trouve
            while i_char + i_string < len(string) and i_char < len(char) and char[i_char] == string[i_string + i_char]:
                i_char += 1
            if i_char == len(char):  # si la boucle a parcouru entièrement 'char', alors il y a une occurrence de char
                # à l'indice de string auquel on se trouve
                new_string += instead  # on effectue le remplacement en ajoutant 'instead' à new_string
                i_string += len(char)  # on incrémente de la longueur de char
            else:
                new_string += string[i_string]
                i_string += 1  # on incrémente de 1 afin de parcourir chaque caractère de 'string' un à un
    return new_string  # on retourne la chaine de caractère
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def extract_name(file_name: str) -> str:
    """
    FONCTION extract_name
    :param file_name : nom du fichier
    :return name_extracted : nom du president obtenu
    permet d'extraire le nom d'un president d'un nom de fichier (string)
    """
    name_extracted = file_name
    # on retire l'extension du fichier, de la chaine de caractère
    name_extracted = replace_char(name_extracted, ".txt", "")
    # on ne garde que la partie droite, où se trouve le nom du président
    name_extracted = replace_char(name_extracted, "Nomination_", "")
    if name_extracted[-1].isnumeric():
        name_extracted = name_extracted[:-1]
    return name_extracted


def extracted_names_list(files: list) -> list:
    """
    FONCTION extracted_names_list
    :param files : Liste des fichiers
    :return names_list : liste des noms des présidents
    Permet d'extraire les noms des présidents à partir des fichiers des discours des présidents, stockés dans une liste.
    """
    names_list = []
    for name in files:  # on parcourt la liste des fichiers
        if not extract_name(name) in names_list:    # on utilise la fonction 'extract_name' pour chaque fichier
            names_list.append(extract_name(name))
    return names_list


def add_first_name(names: list) -> list:
    """
    FONCTION add_first_name
    :param names : liste 1D contenant les noms
    :return names : liste 1D contenant '{prénom} {nom}'
    permet d'ajouter le prénom aux noms
    """
    dict_names = {"Chirac": "Jacque", "Sarkozy": "Nicolas", "Hollande": "François", "Macron": "Emmanuel",
                  "Mitterrand": "François", "Giscard dEstaing": "Valérie"}
    for i in range(len(names)):
        names[i] = dict_names[names[i]] + " " + names[i]
    return names


def print_names(names: list) -> None:
    """
    FONCTION print_names
    :param names: list
    :return: None
    permet d'afficher les prénoms et noms à partir d'une liste
    """
    display = "Voici les noms des présidents :"
    for name in names:
        display += f"\n\t\t-{name}"  # ajoute à display les noms des présidents contenus dans la liste (names)
    print(display)

def cleaning_files(file_name_list: list):
    if not os.path.exists("cleaned"):
        os.mkdir("cleaned")
    for name in file_name_list:  # parcourir la liste des noms des fichiers, pour les ouvrir
        file = open("speeches/" + name, "r", encoding="UTF8")
        speech_list = file.readlines()
        file.close()
        speech = ''
        for line in speech_list:
            speech += line
        file = open("cleaned/" + "cleaned_" + name, "w", encoding="UTF8")
        file.write(cleaning_string(speech))



def cleaning_string(string: str) -> str:
    cleaned_string = ''
    i = 0
    while i < len(string):  # parcourir les caractères de chaque lignes
        # Si le caractère est un ', un - ou un espace, on le remplace par un espace
        if string[i] in "-_ '" and string[i+1] != " ":
            cleaned_string += " "
        if string[i] == "\n":
            cleaned_string += " "
        if string[i] in "dntjm" and string[i-1] == " " and string[i+1] == "'":
            cleaned_string += string[i] + "e "
            i += 1
        if string[i] in "DNTJM" and string[i+1] == "'":
            cleaned_string += chr(ord(string[i])+32) + "e "
            i += 1
        if string[i] in "lL" and string[i+1] == "'":
            cleaned_string += random.choice(["le ", "la "])
            i += 1
        if string[i] in "qQ" and string[i+1] == "u" and string[i+2] == "'":
            cleaned_string += "que "
            i += 2
        # Si le caractère est une lettre majuscule, on la convertie en minuscule
        elif 65 <= ord(string[i]) <= 90:
            cleaned_string += chr(ord(string[i]) + 32)
        # Si le caractère est une lettre miniscule, on le laisse tel quel
        elif 97 <= ord(string[i]) <= 122:
            cleaned_string += string[i]
        # remplace les accents
        elif string[i] in "éèêëçàâùôïî1234567890":
            cleaned_string += string[i]
        # tous les autres caractères ne sont pas ajoutés
        i += 1
    cleaned_string = replace_char(cleaned_string, "  ", " ")
    return cleaned_string


def occurrence(list_of_words: list, directory: str) -> dict:
    """
    FONCTION occurrence
    :param directory:
    :param list_of_words: list contenant un ensemble de mots
    :return: dict
    Fonctions prenant en paramètre une chaine de caractères, renvoyant un dictionnaire contenant le nombre
    d'occurrences de chaque mot de la chaine de caractères
    """
    return_dict = {}  # initialisations du dictionnaire
    set_of_words = words_of_directory(directory)[0]  # set contenant tous les mots présents dans les fichiers .txt, du répertoire 'directory'
    for word in set_of_words:  # on parcourt la liste
        occurence_count = 0
        for paragraph_word in list_of_words:  # on parcourt le string principal
            if word == paragraph_word:
                occurence_count += 1
        return_dict[
            word] = occurence_count  # on ajoute au dictionnaire le mot en clef et son nombre d'occurence en valeur
    return return_dict


def words_of_directory(directory: str) -> (list, list):
    """
    FONCTION list_words
    :param directory: str
    :return: list
    Fonction prenant pour paramètre un chemin d'accès à un répertoire
    renvoyant une liste contenant tout les mots contenus dans les fichiers
    texte (.txt) de ce répertoire
    """
    l_files = list_of_files(directory, "txt")
    all_words = []
    l_words = []
    for name in l_files:
        list_of_words_in_file = []
        file = open(directory + "/" + name, 'r', encoding='UTF8')
        speech = file.readline()
        words = split_char(speech," ")
        for word in words:
            if word != '':
                list_of_words_in_file.append(word)
                all_words.append(word)
        l_words.append(list_of_words_in_file)
    return tri_selection(list(set(all_words))), l_words


def tf_score(directory: str) -> dict:
    """
    FONCTION tf_score
    :param directory: str
    :return: scores : dict
    Fonction prenant en paramètre une chaine de caractères et renvoie un dictionnaire contenant le nombre d'occurrences
    de chaque mot dans les différents discours des présidents
    """
    # dictionnaire dans lequel on ajoute le score_tf de chaque mot, en fonction du fichier txt
    scores = {}
    # liste dans laquelle on ajoute les dictionnaires contenant le mot en clef et son nb d'occurrences en valeur
    list_dicts = []
    list_of_words = words_of_directory(directory)[1]
    for speech in list_of_words:  # on parcourt la liste des mots des discours des présidents
        list_dicts.append(occurrence(speech, directory))
    for key in list_dicts[0]:
        word_score = []  # initialisation de la liste contenant les scores du mot en fonction du fichier text
        # on fait fusionner tout les dictionnaires afin d'en avoir un seul contenant les score tf de chaque mots en fonction du discours
        for dico in list_dicts: # on parcours chaque dictionnaires
            speech_score = 0
            for items in dico.items():
                if items[0] == key:
                    speech_score = items[1]
            word_score.append(speech_score)
        scores[key] = word_score
    return scores


def idf_score(directory: str) -> dict:
    """
    FONCTION idf_score
    :param directory: str
    :return: return_dict :
    fonction qui assigne à chaque mot son score IDF dans un dictionnaire
    """
    return_dict = {}  # initialisations du dictionnaire
    all_words = words_of_directory(directory)[0]  # set dans lequel se trouve tous les mots sans doublons
    list_of_speeches_string = words_of_directory(directory)[
        1]  # liste à deux dimensions contenant tous les mots, de chaque speech

    for word in all_words:  # on parcourt tous les mots du set
        idf = 0
        for speech in list_of_speeches_string:
            is_in_speech = False
            if word in speech:
                is_in_speech = True
            if is_in_speech:
                idf += 1
        idf = math.log10(idf / len(list_of_speeches_string))  # calcul du score_IDF
        return_dict[word] = idf
    return return_dict


def matrice_TF_IDF(directory: str) -> list:
    """
    FONCTION matrice_TF_IDF
    :param directory: str
    :return tf_idf: liste 2D
    assigne à chaque mot des discours ses scores TF-IDF dans une liste 2D triée dans l'ordre alphabétique
    """
    tf_idf_score = []
    idf = idf_score(directory)
    tf = tf_score(directory)
    all_words = words_of_directory(directory)[0]  # list contenant tous les mots du corpus
    for word in all_words:  # on parcourt la liste
        tf_idf_word = [word]
        for speech_tf_score in tf[word]:
            tf_idf_word.append(speech_tf_score * idf[word])  # calcule du score TF-IDF du mot, et ajout dans la matrice
        tf_idf_score.append(tf_idf_word)
    return tf_idf_score


def useless_word(list_of_tfidf_scores: list) -> bool:
    """
    Fonction useless_word
    :param list_of_tfidf_scores: list
    :return: True or False
    Fonction qui renvoie True si un mot est considéré comme inutile et False sinon
    """
    i = 1
    # on parcourt la liste des scores du mot tant que le score TF-IDF est inférieur ou égal à 0.2
    while i < len(list_of_tfidf_scores) and list_of_tfidf_scores[i] <= 0.2:
        i += 1
    if i == len(list_of_tfidf_scores):
        return True
    return False


def useless_word_list(tfidf_list: list) -> list:
    """
    FONCTION useless_word_list
    :param tfidf_list: liste 2D comprenant les mots et leurs scores TF-IDF
    :return: list_of_useless_words : liste des mots inutiles
    renvoie une liste des mots inutiles en utilisant la fonction 'useless_word'
    """
    list_of_useless_words = []
    for word_scores in tfidf_list:
        if useless_word(word_scores):
            list_of_useless_words.append(word_scores[0])
    return list_of_useless_words


def best_tfidf(tfidf_list: list) -> list:
    """
    FONCTION best_tfidf
    :param tfidf_list: liste 2D comprenant les mots et leurs scores TF-IDF
    :return: top_20 : liste des 20 mots avec le score TF-IDF le plus haut
    """
    average_matrice = []
    top_20 = []
    for tfidf_word in tfidf_list:
        average = 0
        for value in tfidf_word[1:len(tfidf_list)]:
            average += value
        average /= (len(tfidf_word) - 1)
        average_matrice.append((tfidf_word[0], average))
    # ***** Tri par sélection *****
    for i in range(len(average_matrice)):
        mini = i
        for j in range(i, len(average_matrice)):
            if average_matrice[j][1] < average_matrice[mini][1]:
                mini = j
        average_matrice[i], average_matrice[mini] = average_matrice[mini], average_matrice[i]
    for i in range(1, 21):
        top_20.append(average_matrice[-i][0])
    return top_20


def word_used(word: str, file_name_list: list, tf_score: dict) -> list:
    """
    FONCTION word_used
    :param word: mot que l'on recherche
    :param file_name_list: liste des noms des fichiers
    :param tf_score: dictionnaire contenant tous les mots avec leurs scores tf
    :return: liste des présidents ayant utilisé le mot
    Fonction renvoyant le nom de présidents ayant utilisé le mot 'word'
    """
    occurence_of_word = tf_score[word]
    presidents_use_word = []
    for i in range(len(occurence_of_word)):
        if occurence_of_word[i] >= 1:
            presidents_use_word.append(file_name_list[i])
    return presidents_use_word


def word_most_used(word: str, file_name_list: list, tf_score: dict) -> str:
    """
    FONCTION word_most_used
    :param word: mot que l'on recherche
    :param file_name_list: liste des noms des fichiers
    :param tf_score: dictionnaire contenant tous les mots avec leurs scores tf
    :return: nom du président ayant utilisé le mot
    """
    occurrence_of_word = tf_score[word]
    maxi = occurrence_of_word[0]
    president_max = ''
    for i in range(len(occurrence_of_word)):    # on parcourt la liste d'occurrences du mot
        if president_max == extract_name(file_name_list[i]):
            maxi += occurrence_of_word[i]    # on regroupe les occurrences entre deux discours du même président
        if occurrence_of_word[i] > maxi:
            maxi = occurrence_of_word[i]
            president_max = extract_name(file_name_list[i])
    return president_max


def most_used_words_by_president(president_name: str, file_name_list: list, tf_score: dict) -> list:
    """
    FONCTION list_of_most_used_words_by_president
    :param president_name: nom du président
    :param file_name_list: liste contenant les noms des fichiers
    :param tf_score: dictionnaire contenant les mots avec leurs scores tf
    :return: liste des 20 mots les plus utilisés par le président demandé
    """
    files_to_search = []
    list_of_most_used_words = ['' in range(20)]    # on initialise une liste de 20 éléments
    for i in range((len(file_name_list))):    # si le président a fait plusieurs discours, on les prend tous en compte
        if extract_name(file_name_list[i]) == president_name:
            files_to_search.append(i)    # on indique dans une liste tous les indices des discours à prendre en compte
    for j in range(20):    # on ajoute à la liste les mots les plus utilisés, avec le score TF le plus élevé
        maxi = 0
        for word in tf_score.keys():    # on parcourt donc tous les mots du/des discours
            score = 0
            for i in range(len(files_to_search)):
                score += tf_score[word][i]
            if word not in list_of_most_used_words and score > maxi:
                list_of_most_used_words[j] = word
                maxi = score
    return list_of_most_used_words


def words_used_by_all_presidents(tf_score: dict, list_of_useless_words: list) -> list:
    """
    Fonction words_used_by_all_presidents
    :param tf_score:
    :param list_of_useless_words:
    :return: liste des mots utilisés par tous les présidents
    """
    list_of_words_used_by_all_presidents = []
    for word in tf_score.keys():    # on parcourt tous les mots des discours
        i = 0
        # on vérifie que le mot soit au moins une fois dans chaque texte
        while i < len(tf_score[word]) and tf_score[word][i] != 0:
            i += 1
        # si le mot est bien dans chaque texte et qu'il n'est pas dans la liste des mots inutiles alors, on l'ajoute
        if word not in list_of_useless_words and i == len(tf_score[word]):
            list_of_words_used_by_all_presidents.append(word)
    return list_of_words_used_by_all_presidents


def green_president(files_names:list, tf_score:dict)->str:
    '''
    :param files_names: nom des fichiers texte du répertoire
    :param tf_score: dictionnaire contenant les scores TF de chaque mots
    :return: name, nom du président ayant été le premier à avoir parlé d'écologie ou de climat
    '''
    president_ecologie = extracted_names_list(word_used('écologique', files_names, tf_score))
    president_climat = extracted_names_list(word_used('climat', files_names, tf_score))
    print(president_climat)
    print(president_ecologie)
    presidents = ["Giscard dEstaing", "Mitterrand", "Chirac", "Sarkozy", "Hollande","Macron"]  # la liste des présidents trier dans l'ordre croissant en dur par rapport à leur date d'investiture
    # on parcours les noms des présidents dans l'ordre de leurs investitures
    for name in presidents:
        if name in president_ecologie or name in president_climat:
                return name


def common_words(set_one:set, set_two:set) -> set:
    """
    :param set_one: un set
    :param set_two: un set
    :return: set contenant l'intersection des deux sets
    """
    return set_one|set_two


def tf_list(sentence_words:list, all_words:list, idf_score:list)->list:
    return_list = []
    for i in range(len(all_words)):
        return_list.append(word[i])
        score = 0
        if all_words[i] in sentence_words:
            for sentence_w in sentence_words:
                if sentence_w == all_words[i]:
                    score += 1
        for j in range(len(idf_score[0])):
            return_list.append(score)
    return return_list


def sentence_tf_idf(tf_sentence:list, all_words:list, idf_dict:dict):
    """
    :param tf_sentence: liste de tout les mots de la question de l'utilisateur
    :param all_words: liste de tout les mots du corpus
    :param idf_dict: dictionnaire des scores idf de tout les mots du corpus
    :return: list : matrice tf_idf de la question de l'utilisateur
    """
    tf_idf = [] # initialisation de la matrice tf_idf
    for i in range(len(all_words)): # on parcours tout les mots du corpus
        assert all_words[i] == tf_sentence[i][0] # on vérifie que tf_sentence est bien trié dans le même ordre que la liste all_words
        word_tf_idf = [all_words[i]]
        for j in range(len(tf_sentence[i])):
            word_tf_idf.append(idf_dict[j] * tf_sentence[i][j]) # on ajoute à la matrice tf_idf multiplie les tf_scores par les idf_scores
    return tf_idf


def scalar_product(vector_1:list, vector_2:list) -> float:
    """
    :param vector_1: liste d'entiers
    :param vecteur_2: liste d'entiers
    :return: somme des produit des entiers de même indice
    """
    assert len(vector_1) == len(vector_2) # on vérifie que les deux listes soient bien de même longueur
    product = 0 # initialisation du produit scalaire
    for i in range(len(vector_1)): # on parcourt les vecteurs
        product += vector_1[i] * vector_2[i] # on ajoute le produit des valeurs de même indice
    return product


def vector_magnitude(vector):
    return math.sqrt(scalar_product(vector, vector))


def cosine_similarity(vector_1:list, vector_2:list) -> float:
    return  scalar_product(vector_1, vector_2) / (vector_magnitude(vector_1) * vector_magnitude(vector_2))

# Call of the function
directory = "./speeches"
cleaned_directory = "./cleaned"
files_name_list = list_of_files(directory, "txt")
presidents_names = extracted_names_list(files_name_list)
print(presidents_names)
presidents_names = add_first_name(presidents_names)
tf_score_dict = tf_score(cleaned_directory)
idf_score_dict = idf_score(cleaned_directory)
print_names(presidents_names)
cleaning_files(files_name_list)

print(tf_score_dict)
print(idf_score_dict)

tfidf_list = matrice_TF_IDF(cleaned_directory)
print(best_tfidf(tfidf_list))

print_names(extracted_names_list(word_used('nation', files_name_list, tf_score_dict)))
print(word_most_used('nation', files_name_list, tf_score_dict))

#print(useless_words(tf_score(cleaned_directory)))

#print((words_of_directory(cleaned_directory)))


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
        print(f"{green_president(files_name_list, tf_score_dict)} est le tout premier président à avoir parlé d'écologie et de climat.")
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

