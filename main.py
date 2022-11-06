from lib2to3.pgen2 import driver
from const import BASE_LINK, FIRST_LINK
from credentials import LOGIN, PASSWORD
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datamanager import DataManager
from speechrecognition import SpeechRecognizer
from sites.antitreningi import Antitreningi
from sites.getcourse import GetCourse

# driver = webdriver.Chrome(ChromeDriverManager().install())

# trainingPlatform = Antitreningi(driver=driver, entry_link=FIRST_LINK, login=LOGIN, password=PASSWORD)
# trainingPlatform.signIn()
# linksArray = trainingPlatform.getLessonLinks()

# dataManager = DataManager()
# dataManager.saveListOfURLsToFile(list = linksArray, fileName = "lesson_links.txt")

# link = "https://antitreningi.ru/student/lessons/lesson?lesson_id=4989236&course_id=118605"
# for link in linksArray:
#     trainingPlatform.downloadVideosIfExists(lesson = link)
# driver.close()

# currentName = trainingPlatform.getLessonName()
# speechRecognizer = SpeechRecognizer()
# speechRecognizer.extractAudio(videoName=currentName, videoFormat=".mp4", audioFormat=".wav")


driver = webdriver.Chrome(ChromeDriverManager().install())

trainingPlatform = GetCourse(
    driver=driver, 
    base_link=BASE_LINK, 
    entry_link=FIRST_LINK, 
    login=LOGIN, 
    password=PASSWORD
)
trainingPlatform.signIn()
linksArray = trainingPlatform.getLessonLinks(lessonLink="https://turkeeva.ru/teach/control/stream/view/id/623763115")

dataManager = DataManager()
dataManager.saveListOfURLsToFile(list = linksArray, fileName = "lesson_links.txt")

numberOfLessons = len(linksArray)
print("Total number of lessons: " + str(numberOfLessons))
for i in range(0, numberOfLessons, 1):
    trainingPlatform.downloadVideosIfExists(lesson = linksArray[i])
    print("Item " + str(i) + " from the list processed successfully")

driver.close()

