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


def question_to_list(question: str) -> list:
    return split_char(cleaning_string(question), " ")


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
        occurrence_count = 0
        for paragraph_word in list_of_words:  # on parcourt le string principal
            if word == paragraph_word:
                occurrence_count += 1
        return_dict[
            word] = occurrence_count  # on ajoute au dictionnaire le mot en clef et son nombre d'occurrence en valeur
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
    list_of_speeches_string = words_of_directory(directory)[1]  # liste à deux dimensions contenant tous les mots, de chaque speech

    for word in all_words:  # on parcourt tous les mots du set
        idf = 0
        for speech in list_of_speeches_string:
            is_in_speech = False
            if word in speech:
                is_in_speech = True
            if is_in_speech:
                idf += 1
        idf = math.log10(len(list_of_speeches_string) / idf)  # calcul du score_IDF
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
    while i < len(list_of_tfidf_scores) and list_of_tfidf_scores[i] == 0:
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
    occurrence_of_word = tf_score[word]
    presidents_use_word = []
    for i in range(len(occurrence_of_word)):
        if occurrence_of_word[i] >= 1:
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


def tf_list(sentence_words:list, all_words:list, n_docs:int) -> list:
    """
    :param sentence_words: list - liste de tout les mots de la phrase entré par l'utilisateur
    :param all_words: list - liste contenant tout les mots du corpus
    :param n_docs: int - nombre de documents dans le corpus
    :return: list - liste contenant les scores tf de chaques mots de la phrase
    """
    return_list = [] # initialisation de la liste contenant les scores tf
    for i in range(len(all_words)):
        sub_list = [all_words[i]] # on met le mot en première deposition de la sous-liste
        score = 0
        if all_words[i] in sentence_words: # si le mot du corpus se trouve dans la phrase de l'utilisateur
            for sentence_w in sentence_words:
                if sentence_w == all_words[i]:
                    score += 1 # on ajoute 1 pour chaque occurrence du mot
        for j in range(n_docs): # on ajoute ça valeur tf autant de fois qu'il y a de documents dans le corpus
            sub_list.append(score)
        return_list.append(sub_list) # on ajoute la sous-liste à la liste
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
        word_tf_idf = [all_words[i]]
        for j in range(len(tf_sentence[i]) - 1):
            word_tf_idf.append(idf_dict[all_words[i]] * tf_sentence[i][j + 1]) # on ajoute à la matrice tf_idf multiplie les tf_scores par les idf_scores
        tf_idf.append(word_tf_idf)
    return tf_idf


def scalar_product(vector_1:list, vector_2:list) -> float:
    """
    :param vector_1: liste de nombres
    :param vector_2: liste de nombres
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
    return scalar_product(vector_1, vector_2) / (vector_magnitude(vector_1) * vector_magnitude(vector_2))


def name_of_max_score_in_index_2(table:list[list]) -> str:
    """
    :param table: liste 2D contenant pour chaque sous liste, une chaine de caractère et
    :return: str : 1er élément de la sous-liste ayant la plus grande valeur en 2ème position
    """
    max_index = 0
    for i in range(1, len(table)):
        if table[i][1] > table[max_index][1]:
            max_index = i
    return table[max_index][0]


def best_sentence_tfidf(sentence_tfidf_list):
    return name_of_max_score_in_index_2(sentence_tfidf_list)


def occurences_index(string:str, sub_str:str)->list:
    """Fonction renvoyant les indices des premiers caractères de chaque occurrence d'une chaine de caractère (sub_str)
    dans une chaine de caractères (string)"""
    print("text", sub_str, string)
    index_list = [] # initialisation de la liste que l'on retourne
    for i in range(len(string)): # on parcourt la chaine de caractèer (string) caractère par caractère
        if string[i] == sub_str[0]: # si le premier caractère des deux chaines sont les mêmes alors on vérifie s'il y a une occurence de sub_string à cet endroit
            j = i  # on copie la valeur i dans j, pour parcourir la suite de la chaine et la comparer à sub_str
            while sub_str[j - i] == string[j] and j - i < len(sub_str) - 1:
                j += 1 # on incrémente j de la longueur de (sub_string) en vérifiant qu'on ne déborde pas de la chaine (string)
            if sub_str == string[i:j + 1]:  # on vérifie si les deux chaines de caractères sont bien les mêmes
                index_list.append(j) # on ajoute l'indice du premier caractère à la liste que l'on retourne
    if index_list == []:
        return [-1]
    return index_list


def list_to_string(table:list)->str:
    string = ""
    for ligne in table:
        string += ligne
    return string


def file_to_string(file_path:str)->str:
    """ Fonction retournant une chaine de caractère contenant le texte du fichier sans les \n de fin de ligne"""
    file = open(file_path, "r", encoding='UTF8')
    return replace_char(list_to_string(file.readlines()), "\n", " ")


def first_occurence_sentence(sub_str, file_path:str):
    text = file_to_string(file_path) # on récupère tout le document dans une chaine de caractère
    first_occurence = occurences_index(text, sub_str)[0] # indice de la première occurrence de sub_str dans le texte
    index = -2
    previous_index = -2
    i = 0
    while i < len(text) - 1 and index < first_occurence: # on parcourt le texte caractère par caractère
        if text[i] in ".?!":
            previous_index, index = index, i
        i += 1
    if index == -2:
        return ""
    else:
        return text[previous_index + 2:index]



