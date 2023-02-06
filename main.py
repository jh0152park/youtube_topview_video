# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


video_information = {}
url = "https://www.youtube.com/@infishin/videos"


def compute_view(view):
    return float(view.split("만회")[0]) * 10000 if "만회" in view else\
            float(view.split("천회")[0]) * 1000 if "천회" in view else\
            int(view.split("회")[0])

print("execute chrome driver")
driver = webdriver.Chrome()
print("get youtube link")
driver.get(url)
print("wait till upload done")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="text"]')))
print("wait more 5 sec")
time.sleep(5)

do = 1
previous = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    print(f"scroll down {do} times.")
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
    time.sleep(5)
    current = driver.execute_script("return document.documentElement.scrollHeight")
    do += 1
    if current == previous:
        break
    previous = current
print("scroll done !!")

soup = BeautifulSoup(driver.page_source, "lxml")
videos = soup.find_all("ytd-rich-item-renderer", attrs={"class": "style-scope ytd-rich-grid-row"})
for video in videos:
    link = video.find("a", attrs={"id": "video-title-link"})['href']
    title = video.find("yt-formatted-string", attrs={"id": "video-title"}).get_text()
    runtime = video.find("span", attrs={"class": "style-scope ytd-thumbnail-overlay-time-status-renderer"})\
        .get_text().strip()
    sub_info = video.find_all("span", attrs={"class": "inline-metadata-item style-scope ytd-video-meta-block"})
    viewer = sub_info[0].get_text().split()[-1]
    upload = sub_info[1].get_text()

    if title not in video_information.keys():
        video_information[title] = {}
    video_information[title] = {
        "runtime": runtime,
        "viewer": compute_view(viewer),
        "upload": upload,
        "link": "https://www.youtube.com" + link
    }

print(f"전체 {len(video_information)}영상 중 100만 조회수 이상의 영상 목록")
cnt = 0
for v in video_information.keys():
    if video_information[v]["viewer"] >= 1000000:
        cnt += 1

        title = v
        runtime = video_information[v]["runtime"]
        viewer = format(video_information[v]["viewer"], ",")
        upload = video_information[v]["upload"]
        link = video_information[v]["link"]
        print(f"{title}_{runtime}({viewer} / {upload})\n{link}")
        print("-" * 50 + "\n")
print(f"전체 {len(video_information)}영상 중 100만 조회수 이상인 영상은 {cnt}개")

while True:
    pass
