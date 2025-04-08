import random, time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import pyperclip
import mdata
def random_wait():
    t = random.uniform(1,3)
    time.sleep(t)
def element_typer(driver, selector,sentence):
    element = driver.find_element(By.CSS_SELECTOR,selector)
    for i in range(len(sentence)):
        element.send_keys(sentence[i])
        t = random.uniform(0.15,0.25)
        time.sleep(t)

# 1. UI의 정 가운데 부분을 클릭함
# 2. 현재 화면에 안 보이는 요소도 클릭할수있음.
def element_random_click(driver,element):
    el_width, el_height = element.size['width'], element.size['height']
    targetX = random.randint( -int(el_width * 0.4), int(el_width*0.4) )
    targetY = random.randint( -int(el_height *0.4), int(el_height*0.4))

    ActionChains(driver).move_to_element(element).pause(2).move_by_offset(targetX,targetY).click().perform()

def random_click(driver, css_selector):
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
     
    el_width, el_height = element.size['width'], element.size['height']
    targetX = random.randint( -int(el_width * 0.4), int(el_width*0.4) )
    targetY = random.randint( -int(el_height *0.4), int(el_height*0.4))

    ActionChains(driver).move_to_element(element).pause(2).move_by_offset(targetX,targetY).click().perform()


# 엘리먼트가 스크린 안에 있는지 확인하는 함수 
# return Bool [ True, False ] 

def is_element_in_screen_bound(driver, element_selector="",element=None):

    cur_window = driver.get_window_size()
    
    screen_height = int(cur_window['height'])
    cur_scrollY = driver.execute_script("return window.scrollY")
    if element == None:
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
    element_y = int(element.location['y'])
    element_height= int(element.size['height'])

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
        with open("./mobile_scroll.txt","r") as f :
            while True:
                line = f.readline()
                if not line:
                    break
                ret_pattern.append(line.rstrip())

        selected_pattern = random.choice(ret_pattern)
        _,sx,sy,delay = selected_pattern.split("#")
        if abs(int(sy)) < 15 or float(delay) < 0.25: #너무 적은 값
            return get_random_pattern(isMobile)
        return int(sx), int(sy), float(delay)
    else: # PC 패턴 
        with open("./pc_scroll.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                ret_pattern.append(line.rstrip())
        pc_scroll_px = 114 # 100, 114    
        selected_pattern = random.choice(ret_pattern)
        _,dx,dy,delay = selected_pattern.split("#")
        if float(delay) < 0.25:
            return get_random_pattern(isMobile)
        return int(dx),int(pc_scroll_px), float(delay)
# 스크린 화면 안으로 Element를 위치시키는 함수
def move_to_bottom(driver):
    sx = random.randrange(100,270)
    sy = random.randrange(250,500)
    randY = random.randrange(13000,15000)
    ActionChains(driver).scroll_by_amount(0, randY).perform()
def random_move(driver,direction="down",count=1,isMobile=True):
    for _ in range(count):
        # [O] 사람패턴 ~ 사람이 얼마나 스크롤을 움직였는지
        # randY = random.randrange(200,300)
        randX,randY,_delay = get_random_pattern(isMobile)
        sx = random.randrange(100,270)
        sy = random.randrange(250,500)

        if direction == "up":
            randY = -randY

        if random.random()  > 0.9 : #10%의 확률로
            randY = -randY

        print(f"Scroll 한다 {randY}")
        ActionChains(driver).scroll_by_amount(0, randY).perform()

        # [O] 사람패턴 ~ 스크롤 하는 텀
        prob = random.random()
        if prob < 0.5:
            dt  = random.uniform(_delay*0.1, _delay*0.3)
        elif prob < 0.8:
            dt = random.uniform(_delay*0.2, _delay*0.6)
        else:
            dt = random.uniform(_delay*0.5, _delay*1.2)

        time.sleep(dt)
        time.sleep( 0.5)
def scroll_to_element(driver, element_selector="",element=None):
    if element == None:
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
    element_y = int(element.location['y'])
    element_height = int(element.size['height'])

    while not is_element_in_screen_bound(driver, element_selector,element):        
        cur_window = driver.get_window_size()
        screen_height = int(cur_window['height'])
        cur_scrollY = int(driver.execute_script('return window.scrollY'))

        if cur_scrollY + screen_height < element_y + element_height + 150:
            random_move(driver, direction="up")
        elif cur_scrollY > element_y - 120:
            random_move(driver, direction="down")
def part_int(n,k):
    def _part(n, k, pre):
        if n <= 0:
            return []
        if k == 1:
            if n <= pre:
                return [[n]]
            return []
        ret = []
        for i in range(min(pre,n), 0 , -1):
            ret += [[i]+sub for sub in _part(n-i,k-1,i)]
        return ret
    return _part(n,k,n)
def random_scroll_with_wait(driver,minutes=3):
    for _ in range(minutes):
        print(_, ' 분째 대기중')
        wait_times = random.choice(part_int(60,6))
        print(wait_times)
        # wait_times : [10,9,11,10,9,11]
        for wait_second in wait_times:
            if random.random() < 0.85:
                randY = random.randrange(400,750)
            else:
                randY = random.randrange(1000,1400)
            
            if random.random() < 0.06:
                randY = - randY

            sx = random.randrange(100,270)
            sy = random.randrange(250,500)
            ActionChains(driver).scroll_by_amount(0, randY).perform()

            print(f"     - {wait_second} 초 대기중 // {randY}")
            time.sleep(wait_second)
def naver_login(driver,_id,_pw):
    id_selector = "#id"
    pw_selector = "#pw"

    #아이디 element 클릭하고, 복붙하기
    print("아이디 복붙하기")
    random_click(driver,id_selector)
    pyperclip.copy(_id) #클립보드에 텍스트를 복사
    time.sleep(0.5)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform() #맥유저 Keys.COMMAND

    time.sleep(2)
    #비밀번호 element 클릭하고, 복붙하기
    print("비밀번호 복붙하기")
    random_click(driver,pw_selector)
    pyperclip.copy(_pw) #클립보드에 텍스트를 복사
    time.sleep(0.5)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform() #맥유저 Keys.COMMAND

    time.sleep(2)
    print("로그인 버튼 누르기")

    로그인버튼_selector= "#upper_login_btn"
    try:
        random_click(driver,로그인버튼_selector)
    except:
        로그인버튼_selector = "#log\.login"
        random_click(driver,)
    time.sleep(3)
def check_alert(driver):
    try:
        WebDriverWait(driver,3).until(EC.alert_is_present())
        #여기 ? 팝업창이 존재한다
        alert = driver.switch_to.alert
        alert.accept()
        return True
    except:
        return False
def press_heart(driver,_id,_pw):
    
    좋아요_selector = "#ct > div._postView > div.section_t1 > div > div.btn_like_w > div > div > a"
    try:
        좋아요_element = driver.find_element(By.CSS_SELECTOR, 좋아요_selector)
        # 스크롤 해야함. 좋아요 버튼 있는곳까지
        # 만약에, 이미 좋아요가 눌러져있는 글이라면, 패스해야됨.
        aria_pressed = 좋아요_element.get_attribute("aria-pressed")
        if aria_pressed =='true':
            print("이미 좋아요가 눌러져 있어서 패스합니다.")
            return
            
        random_click(driver,css_selector=좋아요_selector)
        print("좋아요 버튼을 눌렀습니다.")
        random_wait()
        #팝업 클릭하기
        alert_result = check_alert(driver)
        if alert_result == True: #팝업창을 누른경우
            naver_login(driver,_id,_pw) #로그인 성공 !
            time.sleep(3)
            random_scroll_with_wait(driver,minutes=1)
            좋아요_element = driver.find_element(By.CSS_SELECTOR, 좋아요_selector)
            aria_pressed = 좋아요_element.get_attribute("aria-pressed")
            if aria_pressed =='true':
                print("이미 좋아요가 눌러져 있어서 패스합니다.")
                return
            random_click(driver,css_selector=좋아요_selector)

        else: #로그인 팝업이 없다?
            #좋아요 버튼이 이미 눌러진 상태임.
            pass

    except:
        print("좋아요가 없습니다.")
        

def press_scrap(driver,_id,_pw):
    print("스크랩 버튼 누르기")
    move_to_bottom(driver)
    time.sleep(3)
    스크랩_selector = "#ct > div._postView > div.section_t1 > div > div.btn_r > a.naver-splugin.btn_share._returnFalse"
    try:
        스크랩_element = driver.find_element(By.CSS_SELECTOR, 스크랩_selector)
    except:
        print("스크랩 버튼이 없습니다.")
    try:    
        
        blog_title_selector  = "div[id^='SE-'] > div > div > div.se-module.se-module-text.se-title-text"
        blog_title = driver.find_element(By.CSS_SELECTOR,blog_title_selector).text
    except:
        print("블로그 제목이 없습니다")
    try:
        random_click(driver, 스크랩_selector)
        time.sleep(3)
        블로그_공유_selector="#naver-splugin-wrap > div._spi_card_ly.spi_card.nv_notrans > div._spi_card.spi_area > div > div > div > a.spim_be.lnk_blog._spi_blog"
        random_click(driver,블로그_공유_selector)
        time.sleep(3)
        NAVER_LOGIN_TRY=False
        if "https://nid.naver.com/" in driver.current_url:
            naver_login(driver,_id,_pw)
            NAVER_LOGIN_TRY=True
            
        time.sleep(3)
        덧붙임글_selector = "#ct > div > div.post_wr > textarea"
        random_click(driver,덧붙임글_selector)
        time.sleep(1)
        pyperclip.copy(blog_title)
        time.sleep(1)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform() #맥유저 Keys.COMMAND

        time.sleep(2)

        공개_selector="#ct > div > div.post_set > dl > dd:nth-child(2) > a.set_open"
        random_click(driver, 공개_selector)
        time.sleep(1)
        등록_selector="body > div.head.type1 > a.btn_ok"
        random_click(driver, 등록_selector)
        time.sleep(3)

        팝업_selector = "#lyr4"
        if "내 블로그에 공유했습니다" in driver.find_element(By.CSS_SELECTOR,팝업_selector).text:
            취소_selector="#_confirmLayercancel"
            random_click(driver,취소_selector)
        
        if NAVER_LOGIN_TRY == True:
            random_scroll_with_wait(driver,minutes=1)
        #여기까지 코드가 오면? 
        # 로그인 된 상태로 블로그로 공유 버튼을 잘 누른 상태가됨

    except:
        print("스크랩 버튼이 없습니다.")

def record_client_ip(account_id):
    import requests,datetime
    cur_ip = requests.get("https://api.ipify.org?format=json").json()['ip']
    with open("./record.txt",'a',encoding="utf8") as f:
        now = datetime.datetime.now().now()
        now = now.strftime("%Y-%m-%d %H:%M")
        f.write(f"{now}#{cur_ip}#{account_id}\n")

def read_accounts():
    accounts = []
    with open("./maccount.txt","r",encoding="utf8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            accounts.append(line.rstrip())
    return accounts

def change_ip():
    print("데이터 끄기")
    import subprocess
    subprocess.call("adb shell svc data disable", shell=True)
    time.sleep(1)
    subprocess.call("adb shell settings put global airplane_mode_on 1")
    time.sleep(3)

    subprocess.call("adb shell settings put global airplane_mode_on 0")
    print("데이터 켜기")
    subprocess.call("adb shell svc data enable", shell=True)
    time.sleep(5)
