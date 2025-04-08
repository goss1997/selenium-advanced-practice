import random, os, subprocess, time, random

from selenium.webdriver.common.by import By

# import chromedriver_autoinstaller
# chromedriver_autoinstaller.install()

import mdriver
import mutil

if __name__ == "__main__":

    
    
    accounts = mutil.read_accounts()
    keyword = "파이썬 selenium"
    target_blog_link = "https://m.blog.naver.com/target_id"
    for account in accounts:
        account_id,account_pw = account.split("//") # #id//pw
        
        # mutil.change_ip()

        # mutil.record_client_ip(account_id)
        

        
        driver = mdriver.make_driver(account_id)
        
        #1. 네이버를 켜고
        links = ["https://m.naver.com","https://www.naver.com"]
        link = random.choice(links)
        driver.get(link)
        time.sleep(2)
        if random.random() < 0.2:
            login_url = f"https://nid.naver.com/nidlogin.login?mode=form&url={link}"
            mutil.naver_login(driver,account_id,account_pw)

        time.sleep(2)
        #2. 네이버 검색창을 활성화 시키고
        검색창_selector = '#MM_SEARCH_FAKE'
        mutil.random_click(driver,검색창_selector)

        mutil.random_wait() #좀 쉬자

        #3. '파이썬 selenium'' 키워드를 입력하고
        검색입력창_selector= "#query"
        mutil.element_typer(driver,검색입력창_selector,keyword)


        #4. 네이버 검색하기를 누르고
        검색버튼_selector = "#sch_w > div > form > button"
        mutil.random_click(driver, 검색버튼_selector)
        
        mutil.random_wait() #좀 쉬자

        #5. 타겟 블로그가 있는지 확인
        
        
        TARGET_BLOG_FOUND = False
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, f'a[href^="{target_blog_link}"')
            if len(elements) != 0 :
                TARGET_BLOG_FOUND = True
        except: #에러가 발생되는 경우 : 타겟 블로그가 없는경우.
            print("타겟 블로그가 없습니다")
            pass
        
        if TARGET_BLOG_FOUND: # 블로그가 있는경우 5-1
            #5-1. 있으면 스크롤 해서 이동
                # 클릭하기
                # 끝
            print("타겟 블로그 찾았습니다 블로그 글에 방문하겠습니다")
            print(len(elements))
            elements = driver.find_elements(By.CSS_SELECTOR, f'a[href^="{target_blog_link}"')
            element = random.choice(elements[1:]) # 0 index를 제외하고 선택된 리스트에서
            mutil.scroll_to_element(driver,element=element)
            mutil.element_random_click(driver, element)
            # 클릭하기 끝 !
        else: #5-2 View탭 누르기       
            #5-2. 없으면 View탭을 눌러서
            print("타겟 블로그가 없어서 View탭을 누릅니다")
            elements = driver.find_elements(By.CSS_SELECTOR,f'a[href^="?where=m_view"')
            print(len(elements))
            element = elements[-1]
            mutil.scroll_to_element(driver,element=element)
            mutil.element_random_click(driver, element)
            mutil.random_wait()
            
            # 업데이트된 데이터에서 타겟 블로그가 있는지 확인하기
            for _ in range(0,10): #10번 인피티 스크롤 업데이트하기
                print(_,' 번째 인피니티 스크롤 시도중')
                elements = driver.find_elements(By.CSS_SELECTOR, f'a[href^="{target_blog_link}"')
                if len(elements) != 0 :
                    TARGET_BLOG_FOUND = True
                if TARGET_BLOG_FOUND == True:
                    break
                # 인피티니 스크롤 부분이 활성화되도록 ' 데이터를 새로 받아오는 곳까지 스크롤하기
                mutil.move_to_bottom(driver)
                
                mutil.random_wait()
                mutil.random_wait()
                mutil.random_wait()

            if TARGET_BLOG_FOUND == True:
                # 클릭하기
                elements = driver.find_elements(By.CSS_SELECTOR, f'a[href^="{target_blog_link}"')
                element = random.choice(elements[1:]) # 0 index를 제외하고 선택된 리스트에서
                mutil.scroll_to_element(driver,element=element)
                mutil.element_random_click(driver, element)
            else:
                #5-3. 끝까지 스크롤했는데도 없다? 에러 발생시키기
                # 주의할부분
                pass # 키워드 검색으로 노출이 안되는 블로그인 경우임.
            # 끝
            
        #6. 여기는 블로그에 들어온 상태 
        #Todo [O] 체류 (스크롤)
        mutil.random_scroll_with_wait(driver,minutes=2)

        #Todo [O] 공감하기    
        #Todo [O] 스크랩하기
        
        if random.random()< 0.5:
            print("공감하기 먼저 작업")
            mutil.press_heart(driver,account_id,account_pw)
            mutil.random_scroll_with_wait(driver,minutes=1)

            mutil.random_wait()
            if random.random() < 0.2:
                mutil.press_scrap(driver,account_id,account_pw) #좋아요만 누를확률 80%
                mutil.random_scroll_with_wait(driver,minutes=1)

        else:
            print("스크랩하기 먼저 작업")
            if random.random() < 0.2:
                mutil.press_scrap(driver,account_id,account_pw)
                mutil.random_scroll_with_wait(driver,minutes=1)

            mutil.random_wait()
            mutil.press_heart(driver,account_id,account_pw)
            mutil.random_scroll_with_wait(driver,minutes=1)

        driver.close()
        #다음 작업까지 대기시간 설정하는 부분
        time.sleep(60)
