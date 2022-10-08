from webdriver_manager.core.driver import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.request

class Antitreningi:
    def __init__(self, driver: Driver, entry_link: str, login: str, password: str, base_link = "https://antitreningi.ru"):
        self._driver = driver
        self._timeout = entry_link
        self._login = login
        self._password = password
        self._base_link = base_link
        self._entry_point = base_link + entry_link

    def signIn(self):
        self._driver.get(self._entry_point)
        wait = WebDriverWait(self._driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))).send_keys(self._login)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(self._password)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
        # sign in successfull and entry point URL opened successfully: 
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='block noflex courseinfoblock']")))

    def getLessonLinks(self) -> list:
        soup = BeautifulSoup(self._driver.page_source, "html.parser")
        menu = soup.find_all("div", class_="rmenu")
        menuItems = menu[1].find_all(class_=["rmenu__item", "right-icon"])

        linksArray = []
        for item in menuItems:
            linksArray.append(self._base_link + item['href'])
        return linksArray

    def downloadVideosIfExists(self, lesson: str):
        try:
            print("Trying to open link" + lesson)
            self._driver.get(lesson)
            wait = WebDriverWait(self._driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='lesson_name_container']")))
            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            lessonName = soup.find("h3", class_ = "lesson_name").text.strip() + ".mp4"
            video = soup.find("video", class_="js-player")

            if video != None:
                initialVideoUrl = str(video['src'])

                self._driver.get(initialVideoUrl)
                wait = WebDriverWait(self._driver, 10)
                wait.until(EC.visibility_of_element_located((By.XPATH, "//video[@name='media']")))

                soup = BeautifulSoup(self._driver.page_source, "html.parser")
                targetVideoUrl = soup.find("source")['src']
                urllib.request.urlretrieve(url = targetVideoUrl, filename = lessonName) 
                print("Link " + lesson + " have been saved successfully") 
            else:
                print("Video file " + lesson + " does not exist in the lesson") 
        except:
            print("Something got wrong with " + lesson)
