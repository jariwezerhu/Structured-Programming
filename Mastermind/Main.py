import random


def FullList():  # Alle mogelijke combinaties gesorteerd
    lst = []
    for a in range(1, 7):
        for b in range(1, 7):
            for c in range(1, 7):
                for d in range(1, 7):
                    lst.append(list(str(a) + str(b) + str(c) + str(d)))
    return lst


def PossibleFeedback():  # Maakt alle mogelijke feedback combinaties
    lst = []
    for a in range(0, 5):
        for b in range(0, 5):
            if not a + b > 4:
                lst.append((a, b))
    lst.remove((3, 1))
    return lst

def FeedbackDict():
    combs = {}
    for f in possible_feedback:
        combs[f] = 0
    return combs

all_combinations = FullList()
possible_feedback = PossibleFeedback()
empty_feedbackDict = FeedbackDict()


def keywithmaxval(d):   #gestolen van https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def GenerateCode(lst):  # Computer genereert een 4-cijferige code
    return random.choice(lst)


def CodeMaker():  # Gebruiker kiest een code die de computer gaat raden
    code = input("Kies een vier-cijferige code met de nummers 1-6. Typ deze als xxxx.\nVoer uw code in:")
    code_list = []
    if not TestCode(code):
        CodeMaker()
    print("Uw code is", code)


def MethodChoice():  # Gebruiker kiest methode
    choice = input("Kies 1 voor de simpele methode. Kies 2 voor de Knuth methode.\nKeuze:")
    if choice == '1':
        print("U heeft gekozen voor de simpele methode.")
        SimpleStrategy()
    elif choice == '2':
        print("U heeft gekozen voor de Knuth methode.")
        KnuthStrategy()
    else:
        print("Probeer het nog eens. Typ 1 of 2.")
        MethodChoice()


def ComputerFeedback(computer_code, user_code):  # Geautomatiseerde feedback op de gebruiker's code
    correct_location = 0
    correct_number = 0
    feedback = []
    comp_copy = computer_code.copy()
    user_copy = user_code.copy()
    """De ints worden eerst tegen elkaar's locatie getest en als deze overeenkomen veranderd
    in een x om duplicates te voorkomen. Vervolgens wordt in de tweede for-loop getest of 
    getal voorkomt in de code."""

    for i in range(0, len(user_code)):
        if user_copy[i] == comp_copy[i]:
            correct_location += 1
            user_copy[i], comp_copy[i] = 'x', 'y'
    for i in range(0, len(user_code)):
        if user_copy[i] in comp_copy:
            correct_number += 1
            user_copy[i], comp_copy[i] = 'x', 'y'

    feedback.append(correct_location)
    feedback.append(correct_number)

    return feedback


def CodeBreaker():  # Gebruiker raadt
    computer_code = GenerateCode(all_combinations)
    print("De computer heeft een code bedacht. U heeft 10 pogingen.")
    tries = 10

    """Stukje code om de code in een string te veranderen omdat het mooier is"""
    string_code = "".join(computer_code)

    while tries > 0:
        user_code = UserGuess()
        if user_code == computer_code:
            return print("U heeft gewonnen! De juiste code was inderdaad", string_code)
        else:
            feedback = ComputerFeedback(computer_code, user_code)

            print("Er staan", feedback[0], "nummers op de juiste locatie.\nEr staan", feedback[1],
                  "nummers op de verkeerde locatie.")

            tries -= 1
            if tries > 2:
                print("U heeft", tries, "pogingen over")
            else:
                print("U heeft", tries, "poging over")
    print("U heeft verloren. De code was", string_code + ". Helaas!")


def TestCode(code):  # Test of de code valide is
    valid = [1, 2, 3, 4, 5, 6]
    for i in code:
        if not int(i) in valid:
            print("Er is iets mis met je code. Probeer het opnieuw")
            return False
    return True


def UserFeedback(code):  # De gebruiker's feedback op de gok van de computer
    total = 4
    feedback = []
    print("De computer raadt", code)
    feedback_location = input("Hoeveel nummers heeft de computer op de juiste plek?")

    """Test de feedback_location input. Het getal moet immers tussen de 0 en 4 zitten. Als dit het geval is
    dan wordt dit van het totaal afgehaald. Dit wordt gebruikt voor de volgende test. Er kunnen niet twee
    getallen op de juiste plek staan, en drie getallen op de verkeerde plek."""

    if 0 > int(feedback_location) > 4:
        print("Maximaal 4 en minimaal 0 nummers kunnen op de juiste plek staan. Probeer het nog eens.")
        UserFeedback(code)
    else:
        total -= int(feedback_location)

        feedback.append(int(feedback_location))

    feedback_number = input("Hoeveel nummers heeft de computer op de verkeerde plek?")

    """Vrijwel dezelfde test, alleen wordt hier ook getest of het totaal boven nul is."""

    if 0 > int(feedback_number) > 4:
        print("Maximaal 4 en minimaal 0 nummers kunnen in de code voorkomen. Probeer het nog eens.")
        UserFeedback(code)
    else:
        total -= int(feedback_number)
        if total < 0:
            print("Er is iets fout gegaan. Probeer het nog eens.")
            UserFeedback(code)

        feedback.append(int(feedback_number))

    return feedback


def UserGuess():  # De gebruiker's gok
    user_guess = input("Voer een 4-cijferige code in (1-6):")
    if not TestCode(user_guess):
        UserGuess()
    user_code = list(user_guess)
    return user_code


def SimpleStrategy():
    possible_combs = []
    turn = 10
    first_guess = GenerateCode(all_combinations)
    while turn > 0:
        if turn == 10:
            user_feedback = UserFeedback(first_guess)

            if user_feedback[0] == 4:
                return print("De computer heeft uw code geraden!")

            possible_combs = PossibleCodes(all_combinations, first_guess, user_feedback)
            if first_guess in possible_combs:
                possible_combs.remove(first_guess)
        else:
            next_guess = possible_combs[0]
            possible_combs.remove(next_guess)
            user_feedback = UserFeedback(next_guess)

            if user_feedback[0] == 4:
                return print("De computer heeft uw code geraden!")

            possible_combs = PossibleCodes(possible_combs, next_guess, user_feedback)
        turn -= 1


def PossibleCodes(lst, code, feedback):
    possible_combs = []
    for i in lst:
        if feedback == ComputerFeedback(i, code):
            possible_combs.append(i)
    return possible_combs


def KnuthStrategy():
    turn = 10
    possible_combs = []
    first_guess = [1, 1, 2, 2]
    while turn > 0:
        if turn == 10:
            user_feedback = UserFeedback(first_guess)

            if user_feedback[0] == 4:
                return print("De computer heeft uw code geraden!")

            possible_combs = PossibleCodes(all_combinations, first_guess, user_feedback)
            if first_guess in possible_combs:
                possible_combs.remove(first_guess)
        else:
            next_guess = WorstCase(possible_combs)
            possible_combs.remove(next_guess)
            user_feedback = UserFeedback(next_guess)

            if user_feedback[0] == 4:
                return print("De computer heeft uw code geraden!")

            possible_combs = PossibleCodes(possible_combs, next_guess, user_feedback)
        turn -= 1


def WorstCase(lst):
    code = []
    min_value = 1296
    for a in lst:
        feedback_dict = empty_feedbackDict
        for b in feedback_dict.keys():
            feedback_dict[b] = len(PossibleCodes(lst, a, list(b)))
        max_value = max(feedback_dict.values())
        if min_value > max_value:
            min_value = max_value
            code = a
    return code


def Game():  # Gebruiker kiest zelf raden of computer laten raden
    print("Welkom bij Mastermind. Have fun!")
    choice = input("Typ 1 om te raden. Typ 2 om de computer te laten raden.\nKeuze:")
    if choice == '1':
        print("U heeft gekozen om te raden.")
        CodeBreaker()
    elif choice == '2':
        print("U heeft gekozen om de computer te laten raden.")
        CodeMaker()
        MethodChoice()
    else:
        print("Probeer het nog eens. Typ 1 of 2.")
        Game()


Game()
