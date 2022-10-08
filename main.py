# import urllib.request

# url_link = "https://filestorage.1iu.ru/api/file/f423dc30-951e-479b-a41c-381f547e7766/normalize/get?download=no&public=no&default=original"
# file_name = "Тема1. Вводная часть.mp4"

# urllib.request.urlretrieve(url_link, file_name) 

from lib2to3.pgen2 import driver
from const import BASE_LINK, FIRST_LINK
from credentials import LOGIN, PASSWORD
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.request


import time

def signIn():
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))).send_keys(LOGIN)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(PASSWORD)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='block noflex courseinfoblock']")))

def getLessonLinks() -> list:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    menu = soup.find_all("div", class_="rmenu")
    menuItems = menu[1].find_all(class_=["rmenu__item", "right-icon"])

    linksArray = []
    for item in menuItems:
        linksArray.append(item['href'])
    return linksArray

# Sign in
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(BASE_LINK + FIRST_LINK)

signIn()

# Retrieve lessons links
linksArray = getLessonLinks()


with open("lesson_links.txt", "w") as file:
    for line in linksArray:
        file.write(BASE_LINK + line + "\n")


# Open each link and search for video
for link in linksArray:
    try:
        print("Trying to open link" + link)
        driver.get(BASE_LINK + link)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='lesson_name_container']")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        lessonName = soup.find("h3", class_ = "lesson_name").text.strip() + ".mp4"
        video = soup.find("video", class_="js-player")

        if video != None:
            initialVideoUrl = str(video['src'])

            driver.get(initialVideoUrl)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//video[@name='media']")))

            soup = BeautifulSoup(driver.page_source, "html.parser")
            targetVideoUrl = soup.find("source")['src']
            urllib.request.urlretrieve(url = targetVideoUrl, filename = lessonName) 
            print("Link " + link + " have been saved successfully") 
        else:
            print("Video file " + link + " does not exist in the lesson") 


    except:
        print("Something got wrong with " + link)

driver.close()
