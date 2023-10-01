from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ctypes
import time

def element_exists(driver, xpath, timeout=None):
    if timeout:
         old_implicitly_wait = driver.timeouts.implicit_wait
         driver.implicitly_wait(timeout)
    try:
        element = driver.find_element(By.XPATH, xpath)
        # if found element, return true
        if element:
            driver.implicitly_wait(old_implicitly_wait)
            return True
    except:
            driver.implicitly_wait(old_implicitly_wait)
            return False
    
    

def message_box(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 1)