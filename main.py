from lib2to3.pgen2 import driver
from const import BASE_LINK, FIRST_LINK
from credentials import LOGIN, PASSWORD
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.drivers.chrome import ChromeDriver
import urllib.request

def signInAntitreningi(driver: ChromeDriver, url: str):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))).send_keys(LOGIN)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(PASSWORD)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='block noflex courseinfoblock']")))

def getLessonLinks(driver: ChromeDriver, baseUrl: str) -> list:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    menu = soup.find_all("div", class_="rmenu")
    menuItems = menu[1].find_all(class_=["rmenu__item", "right-icon"])

    linksArray = []
    for item in menuItems:
        linksArray.append(baseUrl + item['href'])
    return linksArray

def saveListOfURLsToFile(list: list, baseURL: str, fileName: str):
    with open(fileName, "w") as file:
        for item in list:
            file.write(item + "\n")

def downloadVideosIfExists(driver: ChromeDriver, lesson: str):
    try:
        print("Trying to open link" + lesson)
        driver.get(lesson)
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
            print("Link " + lesson + " have been saved successfully") 
        else:
            print("Video file " + lesson + " does not exist in the lesson") 
    except:
        print("Something got wrong with " + lesson)

# Sign in
driver = webdriver.Chrome(ChromeDriverManager().install())
startingPointURL = BASE_LINK + FIRST_LINK
signInAntitreningi(driver = driver, url = startingPointURL)

# Retrieve lessons links
linksArray = getLessonLinks(driver = driver, baseUrl = BASE_LINK)

saveListOfURLsToFile(list = linksArray, baseURL = BASE_LINK, fileName = "lesson_links.txt")

link = linksArray[0]
# Open each link and search for video
downloadVideosIfExists(driver = driver, lesson = link)

driver.close()
