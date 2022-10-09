from lib2to3.pgen2 import driver
from const import BASE_LINK, FIRST_LINK
from credentials import LOGIN, PASSWORD
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datamanager import DataManager
from sites.antitreningi import Antitreningi

driver = webdriver.Chrome(ChromeDriverManager().install())

trainingPlatform = Antitreningi(driver=driver, entry_link=FIRST_LINK, login=LOGIN, password=PASSWORD)
trainingPlatform.signIn()
linksArray = trainingPlatform.getLessonLinks()

dataManager = DataManager()
dataManager.saveListOfURLsToFile(list = linksArray, fileName = "lesson_links.txt")

link = "https://antitreningi.ru/student/lessons/lesson?lesson_id=4989236&course_id=118605"
trainingPlatform.downloadVideosIfExists(lesson = link)

driver.close()
