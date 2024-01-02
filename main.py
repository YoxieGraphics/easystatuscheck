from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')
link = os.environ.get('LINK')

print(email)
print(password)
print(link)

profile = webdriver.FirefoxProfile()
options = Options()
options.profile = profile
options.add_argument('--width=800')
options.add_argument('--height=1200')
options.add_argument('--headless')
fOptions = webdriver.FirefoxOptions()
fOptions.set_preference("permissions.default.image", 2)
print(profile.path)
driver = webdriver.Firefox(options=options)
driver.get(link)
driver.find_element("name","login[username]").send_keys(email)
driver.find_element("name","login[password]").send_keys(password)
driver.find_element("name", "send").click()

elem = WebDriverWait(driver, 30).until(
EC.presence_of_element_located((By.CLASS_NAME, "order-status")) #This is a dummy element
)
status = driver.find_element(By.CLASS_NAME, "order-status").text
while True:
    driver.refresh()
    elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "order-status")) #This is a dummy element
    )
    tempStatus = (driver.find_element(By.CLASS_NAME, "order-status").text)
    if tempStatus != status:
        status = tempStatus
        # BEGIN: be15d9bcejpp
        print(status)
        # Make a POST request
        payload = {
            "verify": open("verify.txt", "r").read(),
            "status": status
        }
        print(payload)
        response = requests.post("https://somekindaapi-YoxieGraphics.replit.app", json=payload)
        print(response.text)
        # END: be15d9bcejpp
        
    print(status)
    time.sleep(20)
    