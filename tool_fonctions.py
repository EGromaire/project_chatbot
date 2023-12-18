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
    return new_string  # on retourne la chaine de

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
    """Fonction sommant une liste de chaines de caractère dans une unique chaine de caractère"""
    string = ""
    for ligne in table:
        string += ligne
    return string


def file_to_string(file_path:str)->str:
    """ Fonction retournant une chaine de caractère contenant le texte du fichier sans les \n de fin de ligne"""
    file = open(file_path, "r", encoding='UTF8')
    return replace_char(list_to_string(file.readlines()), "\n", " ")


def remove_sublist_from_matrice(matrice_tfidf: list, sublist: list) -> (list, list):
    """
    Fonction remove_sublist_from_matrice_matrice
    :param matrice_tfidf: matrice contenant le score tf idf de chaque mot dans le corpus
    :param sublist: liste des mots jugés inutiles d'après la fonction useless_words
    :return: deux listes : une liste 1d comprenant tous les mots du corpus excepté les mots inutiles
    et une matrice 2d contenant le score tf idf des mots du corpus excepté les mots inutiles
    """
    copy_of_matrice = []
    all_words = []
    for i in range(len(matrice_tfidf)):
        if matrice_tfidf[i][0] not in sublist:
            copy_of_matrice.append(matrice_tfidf[i])
            all_words.append(matrice_tfidf[i][0])
    return (copy_of_matrice, all_words)