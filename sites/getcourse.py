from webdriver_manager.core.driver import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from bs4 import Tag
import urllib.request

class GetCourse:
    def __init__(self, driver: Driver, base_link: str, entry_link: str, login: str, password: str):
        self._driver = driver
        self._entry_link = entry_link
        self._login = login
        self._password = password
        self._base_link = base_link
        # self._entry_point = base_link + entry_link
        self._current_lesson_name = ""

    def signIn(self):
        self._driver.get(self._base_link)
        wait = WebDriverWait(self._driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))).send_keys(self._login)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(self._password)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='xdget-block xdget-button btn btn-success']"))).click()
        # sign in successfull and entry point URL opened successfully: 
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='page-header']")))

    def getLessonLinks(self, lessonLink: str) -> list:
        linksArray = []
        self._driver.get(lessonLink)
        wait = WebDriverWait(self._driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='page-header']")))
        soup = BeautifulSoup(self._driver.page_source, "html.parser")

        # Check if contains list of modules:
        moduleMenu = soup.find_all("table", class_="stream-table")
        if len(moduleMenu) > 0:
            moduleLinkArray = []
            menuItems = moduleMenu[0].find_all("tr")
            for item in menuItems:
                link = item.find("a")
                moduleLinkArray.append(self._base_link + link['href'])
            
            for moduleLink in moduleLinkArray:
                linksArray.extend(self.getLessonLinks(lessonLink=moduleLink))
            
            return linksArray
        
        # We are on the page with lessons, so can get a lessons list:
        lessonList = soup.find("ul", class_="lesson-list")
        lessons = lessonList.find_all("div", class_=["link","title"])

        for lesson in lessons:
            linksArray.append(self._base_link + lesson['href'])
        return linksArray

    def downloadVideosIfExists(self, lesson: str):
        try:
            print("Trying to open link" + lesson)
            self._driver.get(lesson)
            wait = WebDriverWait(self._driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='lesson_name_container']")))
            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            
            headerTag = soup.find("div", class_ = "lesson_head")
            self._current_lesson_name = self.__generateLessonName(headerTag = headerTag)
            video = soup.find("video", class_="js-player")

            if video != None:
                initialVideoUrl = str(video['src'])

                self._driver.get(initialVideoUrl)
                wait = WebDriverWait(self._driver, 10)
                wait.until(EC.visibility_of_element_located((By.XPATH, "//video[@name='media']")))

                soup = BeautifulSoup(self._driver.page_source, "html.parser")
                targetVideoUrl = soup.find("source")['src']
                urllib.request.urlretrieve(url = targetVideoUrl, filename = self._current_lesson_name + ".mp4") 
                print("Link " + lesson + " have been saved successfully") 
            else:

                print("Video file " + lesson + " does not exist in the lesson") 
        except:
            print("Something got wrong with " + lesson)

    def __generateLessonName(self, headerTag: Tag) -> str:
        theme = headerTag.find("a", class_="theme_name").text.strip().split('.')[0]
        themeNumber = ''.join(i for i in theme if i.isdigit())
        lessonNameComposit = headerTag.find("h3", class_="lesson_name").text.strip().split('.')
        lesson = lessonNameComposit[0]
        lessonNumber = ''.join(i for i in lesson if i.isdigit())
        lessonNameComposit.pop(0)
        lessonName = ".".join(lessonNameComposit)
        lessonName =  " ".join(lessonName.split())
        outputName = themeNumber + "." + lessonNumber + ". " + lessonName
        return (outputName)

    def getLessonName(self) -> str:
        return self._current_lesson_name
