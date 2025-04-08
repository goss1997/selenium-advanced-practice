import random
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from user_agents import parse


def make_user_agent(ua, is_mobile):
    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"
    print(platform)
    if is_mobile:
        platform_info = "Linux armv8l"
        architecture = ""
    else:  # Window
        platform_info = "Win32"
        model = ""
    RET_USER_AGENT = {
        "appVersion": ua.replace("Mozilla/", ""),
        "userAgent": ua,
        "platform": f"{platform_info}",
        "acceptLanguage": "ko-KR, kr, en-US, en",
        "userAgentMetadata": {
            "brands": [
                {"brand": "Google Chrome", "version": f"{version}"},
                {"brand": "Chromium", "version": f"{version}"},
                {"brand": "Not A;Brand", "version": "99"},
            ],
            "fullVersionList": [
                {"brand": "Google Chrome", "version": f"{version}"},
                {"brand": "Chromium", "version": f"{version}"},
                {"brand": "Not A;Brand", "version": "99"},
            ],
            "fullVersion": f"{ua_full_version}",
            "platform": platform,
            "platformVersion": platform_version,
            "architecture": architecture,
            "model": model,
            "mobile": is_mobile  # True, False
        }
    }
    return RET_USER_AGENT


pc_device = ["1920,1440", "1920,1200", "1920,1080", "1600,1200", "1600,900",
             "1536,864", "1440,1080", "1440,900", "1360,768"
             ]

mo_device = [
    "360,640", "360,740", "375,667", "375,812", "412,732", "412,846",
    "412,869", "412,892", "412,915"
]

width, height = random.choice(mo_device).split(",")
print(width, height)
UA = "Mozilla/5.0 (Linux; Android 10; SM-G986U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
options = Options()
# User Agent Data 변경
UA_DATA = make_user_agent(UA, True)

# user agent 설정
options.add_argument(f'--user-agent={UA}')
# window size 설정
options.add_argument(f'--window-size={width},{height}')
# webdriver 인식 false로 설정
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

driver.execute_cdp_cmd("Network.setUserAgentOverride", UA_DATA)

# Max Touch Point 변경
Mobile = {"enabled": True, "maxTouchPoints": random.choice([1, 5])}
driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", Mobile)


# 위치 정보(Geo Location) 변경
def generate_random_geolocation():
    ltop_lat = 37.75415601640249
    ltop_long = 126.86767642302573
    rbottom_lat = 37.593829172663945
    rbottom_long = 127.15276051439332

    targetLat = random.uniform(rbottom_lat, ltop_lat)
    targetLong = random.uniform(ltop_long, rbottom_long)
    return {"latitude": targetLat, "longitude": targetLong, "accuracy": 100}


GEO_DATA = generate_random_geolocation()
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", GEO_DATA)

# 뭐든지 다 속이는 툴
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator,"appName",{
            get: () => 'dragonball'
        });
        Object.defineProperty(navigator,"doNotTrack",{
            get: () => '4'
        });
        Object.defineProperty(navigator,"hardwareConcurrency",{
            get: () => '점심시간이다'
        });
    """
})


# Element.click()의 비밀
# 1. UI의 정 가운데 부분을 클릭함
# 2. 현재 화면에 안 보이는 요소도 클릭할수있음.

def random_click(driver, css_selector):
    element = driver.find_element(By.CSS_SELECTOR, css_selector)

    el_width, el_height = element.size['width'], element.size['height']
    targetX = random.randint(-int(el_width * 0.4), int(el_width * 0.4))
    targetY = random.randint(-int(el_height * 0.4), int(el_height * 0.4))

    ActionChains(driver).move_to_element(element).pause(2).move_by_offset(targetX, targetY).click().perform()


# 네이버에서 존윅 검색
driver.get("https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=%EC%A1%B4%EC%9C%85")
time.sleep(3)
title_selector = 'a[href="https://namu.wiki/w/%EC%A1%B4%20%EC%9C%85"]'

# 랜텀 클릭
random_click(driver, title_selector)
input()
