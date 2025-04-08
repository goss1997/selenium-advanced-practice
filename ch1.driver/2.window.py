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
options.add_argument(f'--user-agent={UA}')
options.add_argument(f'--window-size={width},{height}')
driver = webdriver.Chrome(options=options)
driver.get('https:www.google.com/')
# driver.set_window_position(500,500)
input()

