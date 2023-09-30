from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ctypes

def element_exists(driver, xpath, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath)
                                       )
        )
        return True
    except:
        return False
    

def message_box(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 1)