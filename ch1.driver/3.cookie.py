import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
pc_device = ["1920,1440","1920,1200","1920,1080","1600,1200","1600,900",
                 "1536,864", "1440,1080","1440,900","1360,768"
        ]

mo_device = [
            "360,640", "360,740", "375,667", "375,812", "412,732", "412,846",
            "412,869", "412,892", "412,915"
        ]

width,height = random.choice(pc_device).split(",")
print(width,height)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
options = Options()

# 랜덤쿠키 생성하기
# 1, 100의 숫자이름 폴더 밑에 쿠키를 생성해서 저장하겠다.
rand_user_folder = random.randrange(1,100)
userCookieDir = os.path.abspath(f"./cookies/{rand_user_folder}")
if os.path.exists(userCookieDir) == False:
        print('폴더가 없어서 생성함')
        os.mkdir(userCookieDir)
options.add_argument(f"--user-data-dir={userCookieDir}")
options.add_argument(f'--user-agent={UA}')
options.add_argument(f'--window-size={width},{height}')
driver = webdriver.Chrome(options=options)
driver.get('https:www.google.com/')
# driver.set_window_position(500,500)
input()

