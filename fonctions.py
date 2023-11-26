import os
import math
import time


def replace_char(string:str, char:str, instead:str) -> str:
    '''
    Fonctions replace_char renvoyant une chaine de caractère (string) dans laquelle toutes les occurences d'une chaine de caractère (char)
    a été remplacé par une autre chaine (instead)
    :param string: str - chaine de caractère dans
    :param char: str
    :param instead: str
    :return: new_string
    '''
    new_string = ''  # initialisation de la chaine de caractère dans laquelle on remplace toute les occures de 'char' sont remplacé par 'instead'
    i_string = 0  # indice associé à la chaine de caractère string
    while i_string < len(string):  # on parcours la chaine de caractère de
        if string[i_string] != char[0]:  # si le caractère parcouru est différent de la
            new_string += string[i_string]  # on ajoute le caractère à 'new_string'
            i_string += 1  # on incrémente de 1 afin de parcourir chaque caractère de 'string' un à un
        else:
            i_char = 1 # initialisation de l'indice permettant le parcours de la chaine de caractère 'char'

            # boucle vérifiant si il y a une occurence de la chaine de caractère 'char' à l'indice de string 'i_string' auquel on se trouve
            while i_char + i_string < len(string) and i_char < len(char) and char[i_char] == string[i_string + i_char]:
                i_char += 1
            if i_char == len(char):  # si la boucle a parcouru entièrement 'char', alors il y a une occurence de char à l'indice de string auquel on se trouve
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


def extract_name(file_name:str) -> str :
    '''
    Fonction permettant d'extraire le nom d'un présdent d'un nom de fichier
    :param file_name
    :return: name_extracted
    '''
    name_extracted = file_name
    name_extracted = replace_char(name_extracted, ".txt", "")  # on retire l'extension du fichier, de la chaine de caractère
    name_extracted = replace_char(name_extracted, "Nomination", "")  # on ne garde que la partie droite, où se trouve le nom du président
    if name_extracted[-1].isnumeric():
        name_extracted = name_extracted[:-1]
    return name_extracted


def extracted_names_list(files:list) -> list:
    '''
    Fonction permettant d'extraire les noms des présidents
    à partir des fichiers des discours des présidents, stockés dans une liste.
    Return : liste des noms des présidents
    :param files:
    :return:
    '''
    names_list = []

    for name in files:
        if not extract_name(name) in names_list:
            names_list.append(extract_name(name))
    return names_list


def add_first_name(names):
    dict_names = {"Chirac":"Jacque", "Sarkozy":"Nicolas", "Hollande":"François", "Macron":"Emmanuel", "Mitterrand":"François", "Giscard dEstaing":"Valérie"}
    for i in range(len(names)):
        names[i] = dict_names[names[i]] + " " + names[i]
    return names


def print_names(names:list) -> None:
    '''
    FONCTION print_names
    :param names: list
    :return: None
    Affiche les noms des présidents
    '''
    display = "Voici les noms des présidents :"
    for name in names:
        display += f"\n\t\t-{name}" # ajoute à display les noms des présidents contenus dans la liste (names)
    print(display)


def cleaning_files(files_name_list:list) -> None:
    '''
    FONCTION cleaning_files
    :param files_name_list: list
    :return: None

    Fonctions prenant en entrée la liste des noms des fichiers des discours des présidents,
    Créer un répertoire "cleaned" et ajoute à ce répertoire les fichiers des discours des
    présidents tout en minuscule,sans les caractères spéciaux
    '''
    if not os.path.exists("cleaned"):
        os.mkdir("cleaned")
    for name in files_name_list: # parcourir la liste des noms des fichiers, pour les ouvrir
        file = open("speeches/"+name, "r", encoding="UTF8")
        speech = file.readlines()
        cleaned_speech = ""
        for line in speech: # parcourir les lignes de chaque fichiers
            for letter in line:  # parcourir les caractères de chaque lignes
                # Si le caractère est une lettre majuscule, on la convertie en minuscule
                if 65 <= ord(letter) <= 90:
                    cleaned_speech += chr(ord(letter) + 32)
                # Si le caractère est un ', un - ou un espace, on le remplace par un espace
                elif letter == "'" or letter == "-" or letter == " ":
                    cleaned_speech += " "
                # Si le caractère est une lettre miniscule, on le laisse tel quel
                elif 97 <= ord(letter) <=  122:
                    cleaned_speech += letter
                # remplace les accents
                elif letter in "éèêëçàâùôïî":
                    cleaned_speech += letter
                # si le caractère est un saut de ligne, on le laisse tel quel
                elif letter == "\n":
                    cleaned_speech += " "
                # tous les autres caractères ne sont pas ajoutés

        cleaned_speech = replace_char(cleaned_speech, " d ", " de ")
        cleaned_speech = replace_char(cleaned_speech, "  ", " ")
        file.close()
        new_file = open("cleaned/cleaned_" + name, "w", encoding='UTF8')
        new_file.write(cleaned_speech)
        new_file.close()


def occurence(string:str, directory:str) -> dict:
    '''
    FONCTION occurence
    :param string: str
    :return: dict

    Fonctions prenant en paramètre une chaines de caractères,
    renvoyant un dictionnaire contenant le nombre d'occurence
    de chaque mots de la chaines de caractères
    '''
    return_dict = {}  # initialisations du dictionnaire
    list_of_words = string.split(" ") # on met tout les mots dans une liste
    set_of_words = words_of_directory(directory)[0]  # set contenant tout les mots présent dans les fichiers .txt, du répertoire 'directory'
    for word in set_of_words:  # on parcourt le set
        occurence_count = 0
        for paragraph_word in list_of_words:  # on parcourt le string principal
            if word == paragraph_word:
                occurence_count += 1
        return_dict[word] = occurence_count  # on ajoute au dictionnaire le mot en clef et son nombre d'occurence en valeur
    return return_dict


def words_of_directory(directory:str) -> (list, set):
    '''
    FONCTION list_words
    :param directory: str
    :return: list

    Fonction prenant pour paramètre un chemin d'accès à un répertoire
    renvoyant une liste contenant tout les mots contenus dans les fichiers
    texte (.txt) de ce répertoire
    '''
    l_files = list_of_files(directory, "txt")
    set_words = []
    l_words=[]
    for name in l_files:
        list_of_words_in_file = []
        file = open(directory+"/"+name, 'r', encoding='UTF8')
        speech = file.readline()
        words = speech.split(" ")
        for word in words:
            if word != '':
                list_of_words_in_file.append(word)
                set_words.append(word)
        l_words.append(list_of_words_in_file)
    return set(set_words), l_words


def tf_score(directory:str) -> dict:
    '''Fonctions prenant en paramètre une chaines de caractères,
    renvoyant un dictionnaire contenant le nombre d'occurence de chaque mots dans les différents discours des présidents'''
    scores = {} # initialisation d'un dictionnaire dans laquelle on ajoute le score_tf de chaque mot, en fonction du fichier text
    list_dicts = [] # initialisation d'une liste dans laquelle on ajoute les dictionaires ayant en clef le mot, et son nombre d'occurence en valeure
    list_of_words = words_of_directory(directory)[1]
    for speech in list_of_words: # on parcourt la liste des mots des discours des présidents
        speech_string = ""
        for word in speech:
            speech_string += word + " "
        list_dicts.append(occurence(speech_string, directory))
    for key in list_dicts[0]:
        word_score = []  # initialisation de la liste contenant les scores du mot en fonction du fichier text
        for dict in list_dicts:
            speech_score = 0
            for items in dict.items():
                if items[0] == key:
                    speech_score = items[1]
            word_score.append(speech_score)
        scores[key] = word_score
    return scores


def idf_score(directory):
    return_dict = {}  # initialisations du dictionnaire
    set_of_words = words_of_directory(directory)[0] # set dans lequel se trouve tout les mots sans doublons
    list_of_speeches_string = words_of_directory(directory)[1]  # liste à deux dimensions contenant tout les mots, de chaque speech

    for word in set_of_words:  # on parcourt tout les mots du set
        idf = 0
        for speech in list_of_speeches_string:
            is_in_speech = False
            if word in speech:
                is_in_speech = True
            if is_in_speech:
                idf += 1
        idf = math.log(idf/len(list_of_speeches_string) + 1)  # calcule du score_IDF
        return_dict[word] = idf
    return return_dict


def matrice_TF_IDF(directory:str) -> list:
    '''
    :param directory: chaine de caractère contenant un chemin d'accès à un répertoire
    :return tf_idf: liste 2D, composé de listes contenant un mot des discours et ses scores tf-idf pour chaque discours dans l'ordre alphabétique
    '''
    tf_idf_score = []
    idf = idf_score(directory)
    tf = tf_score(directory)
    set_of_words = words_of_directory(directory)[0] # set contenant tout les mots des discowurs des présidents
    for word in set_of_words: # on parcourt le set
        tf_idf_word = [word]
        for speech_tf_score in tf[word]:
            tf_idf_word.append(speech_tf_score * idf[word]) # calcule du score tf-idf du mot, et ajout dans la matrice
        tf_idf_score.append(tf_idf_word)
    return tf_idf_score


def useless_words(score_tf_list):

    useless_words_list = []
    for word in score_tf_list:
        useless = False
        for i in range(1,8):
            if word[i] == 0:
                useless = True
        if useless:
            useless_words_list.append(word[0])
    return useless_words_list


def best_tfidf(tfidf_list):
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


def word_used(word:str, file_name_list:list, tf_score:dict)-> list:
    '''
    Fonction renvoyant le nom de présdents ayant utilisé le mot 'word'
    :param word: mot que l'on recherche
    :param file_name_list: liste des noms des fichiers
    :param tf_score: dictionnaire contenant tous les mots avec leurs scores tf
    :return: liste des présidents ayant utilisé le mot
    '''
    occurence_of_word =  tf_score[word]
    presidents_use_word = []
    for i in range(len(occurence_of_word)):
        if occurence_of_word[i] >= 1:
            presidents_use_word.append(file_name_list[i])
    return presidents_use_word


def word_most_used(word:str, file_name_list:list, tf_score:dict)-> str:
    '''
    Fonction renvoyant le nom de présdents ayant utilisé le mot 'word'
    :param word: mot que l'on recherche
    :param file_name_list: liste des noms des fichiers
    :param tf_score: dictionnaire contenant tous les mots avec leurs scores tf
    :return: nom du président ayant utilisé le mot
    '''
    occurence_of_word = tf_score[word]
    max = occurence_of_word[0]
    president_max = ''
    for i in range(len(occurence_of_word)):
        if president_max == extract_name(file_name_list[i]):
            max += occurence_of_word[i]
        if occurence_of_word[i] > max:
            max = occurence_of_word[i]
            president_max = extract_name(file_name_list[i])
    return president_max



# Call of the function
directory = "./speeches"
cleaned_directory = "./cleaned"
files_name_list = list_of_files(directory, "txt")
presidents_names = extracted_names_list(files_name_list)
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
    elif user_input == '3':
    elif user_input == '4':
    elif user_input == '5':
    else:
        print("\t\t*** ERREUR DE SAISIE ***")
        print("La valeur que vous avez saisie n'est pas valide !")
        time.sleep(4)
        print("\nRetour au menu principale.")
        time.sleep(2)


