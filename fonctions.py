import math
import random
from tool_fonctions import *


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
        if string[i] in "-_ '" and len(string) > i+1 and string[i+1] != " ":
            cleaned_string += " "
        # si le caractère est un saut de ligne, on le remplace par un espace
        if string[i] == "\n":
            cleaned_string += " "
        # on transforme d', n', t', j', m', en de, ne, te, je, me
        if i-1 >= 0 and string[i] in "dntjm" and string[i-1] == " " and len(string) > i+1 and string[i+1] == "'":
            cleaned_string += string[i] + "e "
            i += 1
        # la même condition est gérée avec des majuscules
        if string[i] in "DNTJM" and len(string) > i+1 and string[i+1] == "'":
            cleaned_string += chr(ord(string[i])+32) + "e "
            i += 1
        # on transforme l' en le/la
        if string[i] in "lL" and len(string) > i+1 and string[i+1] == "'":
            cleaned_string += random.choice(["le ", "la "])
            i += 1
        # on transforme qu' en que
        if string[i] in "qQ" and len(string) > i+2 and string[i+1] == "u" and string[i+2] == "'":
            cleaned_string += "que "
            i += 2
        # Si le caractère est une lettre majuscule, on la convertie en minuscule
        elif 65 <= ord(string[i]) <= 90:
            cleaned_string += chr(ord(string[i]) + 32)
        # Si le caractère est une lettre miniscule, on le laisse tel quel
        elif 97 <= ord(string[i]) <= 122:
            cleaned_string += string[i]
        # remplace les accents et les chiffres
        elif string[i] in "éèêëçàâùôïî1234567890":
            cleaned_string += string[i]
        # tous les autres caractères ne sont pas ajoutés
        i += 1
    # on remplace les doubles espaces par un simple
    cleaned_string = replace_char(cleaned_string, "  ", " ")
    return cleaned_string


def question_to_list(question: str) -> list:
    return split_char(cleaning_string(question), " ")


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


def first_occurence_sentence(sub_str:str, file_path:str)->str:
    """
    :param sub_str: string - chaine de caractère
    :param file_path: str - chemin d'accès à un fichier .txt
    :return: str - La première phrase dans laquelle apparait la chaine sub_str dans le fichier text
    """
    text = file_to_string(file_path) # on récupère tout le document dans une chaine de caractère
    first_occurence = occurences_index(text, sub_str)[0] # indice de la première occurrence de sub_str dans le texte
    index = -2 # indice de la fin de la phrase
    previous_index = -2 # indice de la fin de phrase précédente
    i = 0
    while i < len(text) - 1 and index < first_occurence: # on parcourt le texte caractère par caractère
        if text[i] in ".?!": # s'il y a un point, alors cela indique une fin de phrase
            previous_index, index = index, i
        i += 1
    if index == -2:
        return ""
    else:
        return text[previous_index + 2:index] # +2 car on veut prendre uniquement le premier caractère de la phrase suivante


def pertinent_file(corpus_tf_idf: list, sentence_tf_idf: list, file_name_list: list) -> str:
    """
    FONCTION pertinent_file
    :param corpus_tf_idf: matrice tf idf contenant les mots avec leur score tf idf dans chaque doc
    :param sentence_tf_idf: matrice contenant le score tf idf de chaque mot dans la question
    :param file_name_list: liste contenant tous les noms des fichiers du corpus
    :return: le nom du fichier le plus pertinent par rapport à la qiestion posée
    """
    most_pertinent_file = ''
    max_cos_similarity = 0
    # on parcourt les fichiers un a un, donc on parcourt d'abord l'indice i
    # à chaque changement d'indice de fichier
    for file in range(1, len(corpus_tf_idf[0])):
        cos_similarity = 0
        # on initialise les listes qu'on utilisera pour la fonction cosine_similarity
        # ces deux listes doivent contenir un mot et son score tf idf pour un fichier
        # elles sont réinitialiséées à chaque changement de fichier
        list_tfidf_per_file = []
        list_tfidf_of_question = []
        for i in range(len(corpus_tf_idf)):
            # on ajoute à ces deux listes les mots avec leur score tf idf pour un fichier spécifique
            list_tfidf_per_file.append(corpus_tf_idf[i][file])
            list_tfidf_of_question.append(sentence_tf_idf[i][file])
        cos_similarity = cosine_similarity(list_tfidf_per_file, list_tfidf_of_question)
        if cos_similarity > max_cos_similarity:
            max_cos_similarity = cos_similarity
            most_pertinent_file = file_name_list[file-1]
    return most_pertinent_file


def refine_answer(question_list: list, answer: str) -> str:
    """
    Fonction refine_answer
    :param question_list: liste contenant les mots de la question non nettoyée
    :param answer: la réponse trouvée par le programme sous forme de chaine de caractères
    :return: la réponse retravaillée
    """
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr ! "
    }
    answer_refined = ''
    # on parcourt le dictionnaire pour trouver le début de phrase adéquate
    for starter in question_starters.keys():
        if question_list[0] == starter:
            answer_refined = question_starters[starter]
    # conditions pour ajouter une majuscule et un point si besoin
    answer_refined += answer
    if 97 <= ord(answer_refined[0]) <= 122:
        answer_refined = chr(ord(answer[0]) - 32) + answer[1:]
    if answer[-1] != '.':
        answer_refined += '.'
    return answer_refined



