from primary_functions import *
from database import *

# Initialize variables
try_index = 0
count_greens = 0
wrong_letters = ''
yellow_letters = ''
list_letter_queries = ['','','','',''] # this will have the regex expressions 
                         # for each letter to the word we are looking for
# OBS: the query for each letter will be:
# it isn't in the list of of wrong letters nor possible letters
# until the letter is found, then it will be just the found letter

not_possible_letters = ['','','','',''] # this will have all the words that can't be 
                          # in this position, information given when the letter
                          # is yellow

# Initialize the Chrome web driver
driver = webdriver.Chrome()
config = read_configurations()

# Initialize the word database
word_database = WordDatabase()
word_database.read_database(config['paths']['words'])

# MAIN CODE 

# Initialize wordle website (close popups and set default screen)
init_wordle(driver)

# attempt first word (defined by config)
current_word = config['firstWordTry']
attempt_word(driver, current_word)
try_index+=1

while True:
    # read the classifications of the word
    list_classifications = read_word_colors(driver,try_index, config)

    # to each word, populate list with the informations
    for i in range(5):
        if list_classifications[i] == config['lettersStates']['right']:
            # the right (green) letter is used for the query
            list_letter_queries[i] = current_word[i]
        elif list_classifications[i] == config['lettersStates']['almost']:
            # if the word was found previously as a wrong letter,
            # but now was found as a present letter, remove it from
            # the wrong list (this can happen when the letter is used twice
            # on the word)
            if current_word[i] in wrong_letters:
                wrong_letters.replace(current_word[i],"")
            yellow_letters+=(current_word[i])

            # add the current letter as a not possible letter for the current position
            not_possible_letters[i]+= current_word[i]
        elif list_classifications[i] == config['lettersStates']['wrong']:
            # if it isn't a yellow letter, add to the wrong letters list
            # (wrong letters will be removed from all positions' queries)
            if not(current_word[i] in yellow_letters):
                wrong_letters+=current_word[i]
        else:
            raise Exception("The 'data-state' attribute of the letter wasn't one of the three expected values.")

    # sees if the game still on (if it does, then it updates the word)

    # if  won game, end code
    if count_greens==5:
        message_box("Message box", "Won  game!")
        break

    # if lost game, end code
    if try_index>=6:
        message_box("Message box", "Lost game =(")
        break

    # update the regex expressions for the letters that weren't found
    # if there was one try, say "roads", and only the "r" is yellow and all
    # the other letters are wrong, the regex expressions would be:
    # ['[^oadsr]', '[^oads]', '[^oads]', '[^oads]', '[^oads]']
    for i in range(5):
        # if the current position isn't a green letter
        if not(list_classifications[i]==config['lettersStates']['right']):
            list_letter_queries[i] = f"[^{str(wrong_letters)}{not_possible_letters[i]}]"
        else:
            count_greens+=1
        
    print(f"The query for the word after the {config['ordinalNumbers'][str(try_index)]} try is: {list_letter_queries}")

    # filter the words inside the database
    word_database.update_database_by_query(''.join(list_letter_queries))
    current_word = word_database.get_most_relevant_word()

    # attempt current word of the try
    # if the attempt return false (wasn't accepted), remove it and try again
    while not(attempt_word(driver, current_word)):
        erase_attempt(driver)
        word_database.remove_fist_word()
        current_word = word_database.get_most_relevant_word()

    try_index+=1
