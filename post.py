import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

engine = pyttsx3.init()

voiceoverDirectory = "Voiceovers"
screenshotDir = "Screenshots"

class Post:
    def __init__(self, submission):
        self.submission = submission
        print('created new post object for ' + self.submission.title)
        self.comments = []
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get(submission.url)
        self.content = self.getContentFromPost(self.submission)

    def getContentFromPost(self, submission):
        for comment in submission.comments:
            if (len(comment.body.split()) > 500):
                continue
            self.comments.append(Comment(comment, self.wait))

class Comment:
    def __init__(self, comment, wait):
        self.id = comment.id
        self.text = comment.body
        self.voiceOver = self.createVoiceOver()
        self.screenshot = self.takeCommentScreenshot(wait, self.id)
    
    def createVoiceOver(self):
        filePath = f"{voiceoverDirectory}/comment-{self.id}.mp3"
        engine.save_to_file(self.text, filePath)
        engine.runAndWait()
        return filePath
    
    def takeCommentScreenshot(self, wait, commentId):
        print("taking screenshot of comment " + commentId)
        try:
            handle = (By.ID, f"t1_{commentId}")
            search = wait.until(EC.presence_of_element_located(handle))

            screenshotName = f"{screenshotDir}/{commentId}.png"
            search.screenshot(screenshotName)

            return screenshotName
        except TimeoutException:
            print("Timeout waiting for comment element to appear.")
        except NoSuchElementException:
            print("Comment element not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # screenshotName = f"{screenshotDir}/{handle}.png"
        # file = open(screenshotName, "wb")
        # file.write(search.screenshot_as_png)
        # file.close()