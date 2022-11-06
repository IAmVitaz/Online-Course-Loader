from webdriver_manager.core.driver import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from bs4 import Tag
from time import sleep
import m3u8_To_MP4

class GetCourse:
    def __init__(self, driver: Driver, base_link: str, entry_link: str, login: str, password: str):
        self._driver = driver
        self._entry_link = entry_link
        self._login = login
        self._password = password
        self._base_link = base_link
        self._current_lesson_name = ""
        self._course_name = None

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

        #Update course name from the initial link:
        if not self._course_name:
            courseNameTag = soup.find("div", class_="page-header")
            self._course_name = courseNameTag.find("h1").text.strip()

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
        video = None
        try:
            print("Trying to open link" + lesson)
            self._driver.get(lesson)
            wait = WebDriverWait(self._driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='standard-page-content']")))
            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            
            moduleNameTag = soup.find("div", class_ = "page-header")
            lessonNameTag = soup.find("div", class_ = "header-view")
            self._current_lesson_name = self.__generateLessonName(moduleNameTag=moduleNameTag, lessonNameTag=lessonNameTag)
            videoTag = soup.find("div", class_ = "lite-page")
            videos = videoTag.find_all("iframe")
        except:
            return print("We did not find video frames for " + lesson)

        try:
            if videos != None:
                videoOnThePage = 1
                for video in videos:
                    initialVideoUrl = str(video['src'])
                    self._driver.get(initialVideoUrl)
                    wait = WebDriverWait(self._driver, 10)
                    wait.until(EC.visibility_of_element_located((By.XPATH, "//video[@class='vvd-video']")))
                    sleep(3)

                    m3u8Link = self.__findm3u8InNetworkRequests()
                    if not m3u8Link:
                        return print("We did not find m3u8 link for " + lesson)

                    fileName = self._current_lesson_name
                    if videoOnThePage != 1:
                        fileName += "(" + str(videoOnThePage) + ")"
                    loadDir = "/" + self._course_name + "/"
                    m3u8_To_MP4.multithread_download(m3u8_uri=m3u8Link, mp4_file_name=fileName, mp4_file_dir=loadDir)

                    videoOnThePage += 1
                    print("Link " + lesson + " have been saved successfully") 
            else:
                print("Video file " + lesson + " does not exist in the lesson") 
        except:
            print("Something got wrong with " + lesson)

    def __findm3u8InNetworkRequests(self) -> str:
        JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
        network_requests = self._driver.execute_script(JS_get_network_requests)
        for n in network_requests:
            if "master.m3u8" in n["name"]: 
                resultLink = n["name"].split("?")[0]
                return resultLink
        return None


    def __generateLessonName(self, moduleNameTag: Tag, lessonNameTag: Tag) -> str:
        moduleName = moduleNameTag.find("a").text.strip() 
        lessonName = lessonNameTag.find("h2", class_="lesson-title-value").text.strip()
        outputName = moduleName + ". " + lessonName
        return (outputName)

    def getLessonName(self) -> str:
        return self._current_lesson_name
