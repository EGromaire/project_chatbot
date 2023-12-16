def index_occurences(string:str, list_of_strings:list[str]) -> list:
    """Fonction renvoyant les indices de chaque occurence d'une liste de chaine de caractère (string) dans une liste de
    chaines de caractères (list_of_strings)"""
    index_list = []
    for i in range(len(list_of_strings)):
        assert len(string) <= len(list_of_strings[i])  # on vérifie que string aie bien une longueur 
        current_word = ""

        for j in range(len(list_of_strings[i])): # on parcourt la chaine caractère par caractère
            if list_of_strings[i][j] == string[0]:
                k = j # on copie la valeur j dans k, pour parcourir la suite de la chaine de caractère
                current_word += list_of_strings[i][k]
                while string[k - j] == list_of_strings[i][k] and k - j < len(string) - 1:
                    k += 1
                    print(k, j)
                if string == list_of_strings[i][j:k+1]: # on vérifie si les deux chaines de caractères sont bien les mêmes
                    index_list.append([i, j])
            current_word = ""

    return index_list


print(index_occurences("les", ["En conclusion, remercions ceux qui ont contribué à notre parcours jusqu'à présent, célébrons nos réussites collectives et engageons-nous résolument envers un avenir où l'unité, la compréhension et le respect mutuel guideront nos actions.", "Ainsi, je vous invite à prendre part à cette aventure collective, à partager vos idées, à inspirer et à être inspirés. Que notre collaboration soit le catalyseur d'un changement positif, propulsant nos sociétés vers un avenir où chacun a la possibilité de s'épanouir.", "En tant que membres de cette communauté, nous avons la responsabilité de cultiver la bienveillance, le respect et l'empathie. C'est en travaillant ensemble, en écoutant les uns les autres, que nous pourrons surmonter les défis qui se dressent devant nous.", "L'histoire nous enseigne que les grandes réalisations sont le fruit d'efforts collectifs. Chacun de nous, dans son rôle unique, contribue à l'édification d'un monde plus juste, plus équitable et plus durable. Que ce soit dans les domaines de la science, de la technologie, de l'éducation, de l'art ou de l'entreprise, nos actions individuelles ont un impact qui va bien au-delà de notre cercle immédiat."]))