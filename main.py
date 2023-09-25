import praw
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from moviepy.editor import *


voiceoverDirectory = "Voiceovers"
screenshotDir = "Screenshots"

driver = webdriver.Firefox()
driver.get(submission.url)

reddit = praw.Reddit(
    client_id="6BTa-Zg0LzSof23gsNnmCw",
    client_secret="dWPGy38FvVtaYZIZnMlq5BMb_c5v7w",
    user_agent="chrome:com.myredditapp:v1.0 (by u/Zone-Embarrassed)",
)

existingPostIds = [] # when save submission Ids when posting videos

submissions = reddit.subreddit("askreddit").top(time_filter="day", limit="3")

for submission in submissions:
    if (submission.id in existingPostIds or submission.over_18):
        continue

def getContentFromPost(submission):
    for comment in submission.comments:
        if (len(comment.body.split()) > 100):
            continue
        addComment(comment)

def addComment(comment):
    id = comment.id
    text = comment.body

def createVoiceOver(id, text):
    engine = pyttsx3.init()
    filePath = f"{voiceoverDirectory}/comment-{id}.mp3"
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath

def takeTitleScreenshot(driver, wait):
    handle = By.CLASS_NAME
    className = "Post"
    search = wait.until(EC.presence_of_element_located(handle, className))

    screenshotName = f"{screenshotDir}/{handle}.png"
    file = open(screenshotName, "wb")
    file.write(search.screenshot_as_png)
    file.close()

    return screenshotName


def takeCommentScreenshot(driver, wait, commentId):
    handle = By.ID
    id = f"t1_{commentId}"
    search = wait.until(EC.presence_of_element_located(handle, id))

    screenshotName = f"{screenshotDir}/{handle}.png"
    file = open(screenshotName, "wb")
    file.write(search.screenshot_as_png)
    file.close()
    
    return screenshotName


def createClip(screenshotFile, voiceOverFile):
    imageClip = ImageClip(screenshotFile)
    audioClip = audioClip(voiceOverFile)
    videoClip = imageClip.set_audio(audioClip)
    return videoClip


def generateClips():
    clips = []

    titleClip = createClip(title.screenshot, title.voiceover)
    clips.append(titleClip)
    for comment in script.comments:
        videoClip = createClip(comment.screenshot, comment.voiceover)
        clips.append(videoClip)

    titleAndCommentsClip = concatenate_videoClips(clips)