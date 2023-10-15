from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from secondary_functions import *
import json
import time


# read config file
def read_configurations(config_file_path = 'Config.json'):
    print('Reading config file...')
    f = open(config_file_path)
    return json.load(f)

    

def init_wordle(driver):
    # Open the Wordle game URL
    driver.get('https://www.nytimes.com/games/wordle')

    # Wait for the page to load (you might need to adjust the wait time)
    driver.implicitly_wait(10)  # Wait for up to 10 seconds

    # See if "We've updated our terms" message appears
    if element_exists(driver, "//p[@class='purr-blocker-card__heading']", 2):
        print("The \"We've updated our terms\" message has appeared, closing it...")
        driver.find_element(By.XPATH, "//button[@class='purr-blocker-card__button']").click()
        print("Clicked successfully on the terms 'Continue' button.")

    # See if the cookies message appears
    if element_exists(driver, "//h3[@class='banner-title' and text()='Your tracker settings']", 2):
        print("The cookies pop message has appeared, accepting on it...")
        driver.find_element(By.XPATH, "//button[@id='pz-gdpr-btn-accept']").click()
        print("Clicked successfully on the cookies 'Accept' button.")

    # Locate the play button and click it text "Play"
    driver.find_element(By.XPATH,"//button[text()='Play']").click()

    # See if the 'how to play' message appears
    if element_exists(driver, 
                        "//h2[contains(@class,\"Modal-module_heading\") and text()=\"How To Play\"]",
                    5):
        print("The how to play tutorial appeared, accepting it...")
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        if element_exists(driver, 
                        "//h2[contains(@class,\"Modal-module_heading\") and text()=\"How To Play\"]",
                    5):
            raise Exception("Could not close the how to play tutorial")
        print("Closed successfully the how to play tutorial.")
    
    # maximize window
    driver.maximize_window()

    # scroll to show the keyboard
    keyboard_enter_element = driver.\
        find_element(By.XPATH, 
                     "//button[contains(@class, 'Key-module_key__kchQI') and text()='enter']")
    ActionChains(driver)\
        .scroll_to_element(keyboard_enter_element)\
        .perform()

    print("Wordle game was initialized successfully.")



def attempt_word(driver, word):
    # send word keys and enter to the game page
    print("Attempting word {}...".format(word))
    time.sleep(0.25)
    app_container_element = driver.find_element(By.XPATH, 
                        "/html")
    app_container_element.send_keys(word)
    app_container_element.send_keys(Keys.ENTER)

    # if the wrong doesn't belong to the game, return false
    # (warn Not in the word list)
    if element_exists(driver, 
                      "//div[@class='Toast-module_toast__iiVsN' and contains(text(),'word list')]",
                       2):
        print('Word not accepted, trying another one...')
        return False
    return True


def erase_attempt(driver):
    # send backscape 5 times
    for _ in range(5):
        ActionChains(driver).send_keys(Keys.BACK_SPACE).perform()

    

def read_word_colors(driver, index, config):
    # given the word index, get the classification of the letters
    classification_list = []
    for i  in range(1,6):
        classification_list.append(
            # the letter is found by the aria label of a parent element
            # which corresponds to the row (should be 'Row 1', for instance)
            # and its own aria label attribute (it should contain 1st letter, 
            # for instance)
            driver.find_element(By.XPATH,
                                f"//div[@aria-label='Row {index}']/div/"
                                    "div[@class='Tile-module_tile__UWEHN'"
                                         "and contains(@aria-label,'"
                                            f"{config['ordinalNumbers'][str(i)]} letter')]")\
                                                .get_attribute(config['attributes']['wordClass'])
        )
    return classification_list

