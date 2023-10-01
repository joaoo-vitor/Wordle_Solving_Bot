from primary_functions import *

# Initialize the Chrome web driver
driver = webdriver.Chrome()
config = read_configurations()
init_wordle(driver)
attempt_word(driver, config['firstWordTry'])

message_box("Message box", "Finished code")
