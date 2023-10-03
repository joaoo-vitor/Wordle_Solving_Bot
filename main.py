from primary_functions import *


# Initialize variables
line_index = 1

# Initialize the Chrome web driver
driver = webdriver.Chrome()
config = read_configurations()
init_wordle(driver)

current_word = config['firstWordTry']
attempt_word(driver, current_word)

list_classifications = read_word_colors(driver,line_index, config)
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

# update the regex expressions for the letters that weren't found
# if there was one try, say "roads", and only the "r" is yellow and all
# the other letters are wrong, the regex expressions would be:
# ['[^oadsr]', '[^oads]', '[^oads]', '[^oads]', '[^oads]']
for i in range(5):
    # if the current position query isn't just a letter (green letter)
    if not(len(list_letter_queries[i])==1):
        list_letter_queries[i] = f"[^{str(wrong_letters)}{not_possible_letters[i]}]"

print(list_letter_queries)

message_box("Message box", "Finished code")