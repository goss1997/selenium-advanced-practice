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


# 엘리먼트가 스크린 안에 있는지 확인하는 함수
# return Bool [ True, False ]
def is_element_in_screen_bound(driver, element_selector="", element=None):
    cur_window = driver.get_window_size()

    screen_height = int(cur_window['height'])
    cur_scrollY = driver.execute_script("return window.scrollY")
    if element == None:
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
    element_y = int(element.location['y'])
    element_height = int(element.size['height'])

    # print(f"cur_scrollY : {cur_scrollY} , element_y : {element_y}, element_height : {element_height}")

    if cur_scrollY + screen_height < element_y + element_height + 150:
        return False
    if cur_scrollY > element_y - 120:
        return False
    return True


# 랜덤 패턴 가지고오기
def get_random_pattern(isMobile=True):
    ret_pattern = []
    if isMobile:
        with open("./mobile_scroll.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                ret_pattern.append(line.rstrip())

        selected_pattern = random.choice(ret_pattern)
        _, sx, sy, delay = selected_pattern.split("#")
        if abs(int(sy)) < 15 or float(delay) < 0.25:  # 너무 적은 값
            return get_random_pattern(isMobile)
        return int(sx), int(sy), float(delay)
    else:  # PC 패턴
        with open("./pc_scroll.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                ret_pattern.append(line.rstrip())
        pc_scroll_px = 114  # 100, 114
        selected_pattern = random.choice(ret_pattern)
        _, dx, dy, delay = selected_pattern.split("#")
        if float(delay) < 0.25:
            return get_random_pattern(isMobile)
        return int(dx), int(pc_scroll_px), float(delay)


# 스크롤 하는 함수
def random_move(driver, direction="down", count=1, isMobile=True):
    for _ in range(count):
        # [O] 사람패턴 ~ 사람이 얼마나 스크롤을 움직였는지
        # randY = random.randrange(200,300)
        randX, randY, _delay = get_random_pattern(isMobile)
        sx = random.randrange(100, 270)
        sy = random.randrange(250, 500)

        if direction == "up":
            randY = -randY

        if random.random() > 0.9:  # 10%의 확률로
            randY = -randY

        print(f"Scroll 한다 {randY}")
        ActionChains(driver).scroll_by_amount(0, randY).perform()

        # [O] 사람패턴 ~ 스크롤 하는 텀
        prob = random.random()
        if prob < 0.5:
            dt = random.uniform(_delay * 0.1, _delay * 0.3)
        elif prob < 0.8:
            dt = random.uniform(_delay * 0.2, _delay * 0.6)
        else:
            dt = random.uniform(_delay * 0.5, _delay * 1.2)

        time.sleep(dt)
        time.sleep(0.5)


# 스크린 화면 안으로 Element를 위치하는 함수
def scroll_to_element(driver, element_selector="", element=None):
    if element == None:
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
    element_y = int(element.location['y'])
    element_height = int(element.size['height'])

    while not is_element_in_screen_bound(driver, element_selector, element):
        cur_window = driver.get_window_size()
        screen_height = int(cur_window['height'])
        cur_scrollY = int(driver.execute_script('return window.scrollY'))

        if cur_scrollY + screen_height < element_y + element_height + 150:
            random_move(driver, direction="up")
        elif cur_scrollY > element_y - 120:
            random_move(driver, direction="down")


# 네이버에서 존윅 검색
driver.get("https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=%EC%A1%B4%EC%9C%85")
time.sleep(3)
title_selector = 'a[href="https://namu.wiki/w/%EC%A1%B4%20%EC%9C%85"]'

# 스크롤
scroll_to_element(driver, title_selector)

# 랜텀 클릭
random_click(driver, title_selector)
input()
