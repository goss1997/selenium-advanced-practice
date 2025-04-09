import time
from threading import Thread

from pynput import mouse

sx, sy, st = 0, 0, 0
current_time = time.time()


def on_click(x, y, button, pressed):
    global sx, sy, st

    if button == mouse.Button.left:
        print("왼쪽 클릭 : ", pressed, x, y)

        if pressed:
            st = time.time()
            sx = x
            sy = y
        else:
            with open("./mobile_scroll.txt", "a") as f:
                rx = x - sx
                ry = y - sy
                rt = time.time() - st
                f.write(f"scroll#{rx}#{ry}#{rt}\n")


# PC Scroll 수집
def on_scroll(x, y, dx, dy):
    global current_time
    print("Scroll했음 {0} at {1}".format('down' if dy < 0 else 'up', (x, y)))
    print(dx, dy)
    delay_time = time.time() - current_time
    current_time = time.time()
    with open('./pc_scroll.txt', 'a') as f:
        f.write(f"scroll#{dx}#{dy}#{delay_time}\n")


def main():
    while True:
        listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
        listener.start()  # 리스너가 시작됨
        listener.join()  # 리스너 대기시키기


# 메인 스레드 생성 및 시작
mainThread = Thread(target=main)
mainThread.start()
mainThread.join()  # 메인 스레드가 종료될 때까지 대기
