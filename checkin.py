# -*- coding: utf-8 -*-

import time
import requests
import json
import tkinter as tk
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def tip(text):
    global label_tip
    label_tip['text'] = text


def lock():
    global entry_username
    global entry_password
    global btn_login
    entry_username['state'] = 'disabled'
    entry_password['state'] = 'disabled'
    btn_login['state'] = 'disabled'
    tip('开始签到')


def release():
    global entry_username
    global entry_password
    global btn_login
    entry_username['state'] = 'normal'
    entry_password['state'] = 'normal'
    btn_login['state'] = 'normal'
    tip('网络错误')


def check_in(retry=3):
    global endpoint
    global username
    global token
    global is_keep
    link = endpoint + '/checkIn.php?username=' + username.get() + '&' + 'token=' + token
    try:
        http = requests.get(link, verify=False)
        data = json.loads(http.content.decode('utf-8'))
        if (data['code'] == 200):
            tip('签到成功！')
        else:
            if (retry != 0):
                tip('签到失败，重试')
                check_in(retry - 1)
            else:
                print('签到失败')
                tip('签到失败，延迟5分钟')
    except Exception:
        if (retry != 0):
            tip('签到失败，重试')
            check_in(retry - 1)
        else:
            print('签到失败')
            tip('签到失败，延迟5分钟')


def get_token(retry=3):
    global endpoint
    global username
    global password
    global token
    global is_keep
    link = endpoint + '/getToken.php?username=' + username.get() + '&' + 'password=' + password.get()
    try:
        http = requests.get(link, verify=False)
        data = json.loads(http.content.decode('utf-8'))
        if (data['code'] == 200):
            print(data)
            token = data['body']
            tip('获取Token成功')
        else:
            if (retry != 0):
                get_token(retry - 1)
            else:
                print('获取Token失败')
                tip('获取Token失败')
                is_keep = False
    except Exception:
        if (retry != 0):
            get_token(retry - 1)
        else:
            print('获取Token失败')
            tip('获取Token失败')
            is_keep = False


def counter(times):
    global label_counter
    print(times)
    while times != 0:
        print(times)
        times = times - 1
        label_counter['text'] = times
        time.sleep(1)
    print('结束计数')


def keeper():
    global is_keep
    while is_keep is True:
        # 获取Token
        get_token()
        # 签到
        check_in()
        # 暂停5分钟
        if (is_keep is True):
            counter(5 * 60)
    release()


def login():
    global username
    global password
    global is_keep
    global thread
    if (username.get() == '' and password.get() == ''):
        tip('信息缺失')
    else:
        lock()
        thread = []
        is_keep = True
        print(username.get())
        print(password.get())
        tr = threading.Thread(target=keeper, daemon=True)
        thread.append(tr)
        tr.start()


def create_ui():
    global entry_username
    global entry_password
    global btn_login
    global label_counter
    global label_tip
    global username
    global password
    global VERSION

    win = tk.Tk()
    win.title('Check-in Game ' + VERSION)
    win.minsize(280, 80)
    win.resizable(False, False)

    label_username = tk.Label(win, text='用户名：')
    label_username.grid(row=0, column=0, padx=5, pady=2, sticky=tk.E)
    label_password = tk.Label(win, text='密码：')
    label_password.grid(row=1, column=0, padx=5, pady=2, sticky=tk.E)

    username = tk.StringVar()
    password = tk.StringVar()

    entry_username = tk.Entry(win, textvariable=username)
    entry_username.grid(row=0, column=1, padx=0, pady=0)
    entry_password = tk.Entry(win, textvariable=password)
    entry_password['show'] = '*'
    entry_password.grid(row=1, column=1, padx=0, pady=0)

    btn_login = tk.Button(win, text="登录并签到", command=login)
    btn_login.grid(row=0, rowspan=2, column=2, padx=5, pady=2, sticky=tk.N+tk.S)

    label_charts = tk.Label(win, text='排行榜', fg='blue')
    label_charts.grid(row=2, column=0, columnspan=2, padx=5, pady=1, sticky=tk.W)

    label_counter = tk.Label(win, text='0', fg='red')
    label_counter.grid(row=2, column=2, padx=5, pady=1, sticky=tk.E)

    label_tip = tk.Label(win, text='就绪', anchor='w')
    label_tip.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky=tk.W)

    win.mainloop()


def main():
    global endpoint
    global username
    global password
    global token
    global is_keep
    global VERSION
    VERSION = '1.0.0'
    is_keep = False
    endpoint = 'https://checkin.tcapps.twocola.com/'
    username = ''
    password = ''
    token = ''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    create_ui()


if __name__ == '__main__':
    main()
