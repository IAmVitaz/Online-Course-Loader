from lib2to3.pgen2 import driver
from const import BASE_LINK, FIRST_LINK
from credentials import LOGIN, PASSWORD
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from sites.antitreningi import Antitreningi

def saveListOfURLsToFile(list: list, baseURL: str, fileName: str):
    with open(fileName, "w") as file:
        for item in list:
            file.write(item + "\n")

driver = webdriver.Chrome(ChromeDriverManager().install())

trainingPlatform = Antitreningi(driver=driver, entry_link=FIRST_LINK, login=LOGIN, password=PASSWORD)
trainingPlatform.signIn()
linksArray = trainingPlatform.getLessonLinks()

saveListOfURLsToFile(list = linksArray, baseURL = BASE_LINK, fileName = "lesson_links.txt")

link = linksArray[0]
trainingPlatform.downloadVideosIfExists(lesson = link)

driver.close()
