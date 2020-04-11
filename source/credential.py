# modified from https://github.com/MXWXZ/sjtu-automata

from time import sleep
import os
from PyQt5.QtCore import qDebug
from captcha import Captcha

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from tenacity import retry, retry_if_exception_type, wait_fixed

from utils import (re_search, get_timestamp)
from utils import (RetryRequest, AutomataError)


def _create_session():
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    qDebug("out create session")
    return session


@retry(retry=retry_if_exception_type(RequestException), wait=wait_fixed(3))
def _get_login_page(session, url):
    # return page text
    req = session.get(url)
    # if last login exists, it will go to error page. so ignore it
    if '<form id="form-input" method="post" action="ulogin">' in req.text:
        qDebug("out get page")
        return req.text
    else:
        raise RetryRequest  # make it retry


@retry(retry=retry_if_exception_type(RequestException), wait=wait_fixed(3))
def _bypass_captcha(session, url):
    # return captcha code
    captcha = session.get(url)
    log_dir = os.path.join(
                   os.path.split(os.path.abspath(__file__))[0],
                   "log")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    with open(os.path.join(log_dir, 'captcha.jpeg'), 'wb') as f:
        f.write(captcha.content)
    qDebug("out captcha")
    return None


@retry(retry=retry_if_exception_type(RequestException), wait=wait_fixed(3))
def _login(session, sid, returl, se, client, username, password, code, uuid):
    # return 0 suc, 1 wrong credential, 2 code error, 3 30s ban
    data = {'sid': sid, 'returl': returl, 'se': se,
            'client': client, 'user': username,
            'pass': password, 'captcha': code,
            'v': '', 'uuid': uuid}
    req = session.post(
        'https://jaccount.sjtu.edu.cn/jaccount/ulogin', data=data)

    # result
    # be careful return english version website in english OS
    if '请正确填写验证码' in req.text or 'wrong captcha' in req.text:
        return 2
    elif '请正确填写你的用户名和密码' in req.text or \
         'wrong username or password' in req.text:
        return 1
    elif '30秒后' in req.text:  # 30s ban
        return 3
    elif '<i class="fa fa-gear" aria-hidden="true" id="wdyy_szbtn">':
        return 0
    else:
        raise AutomataError


def login(url, parent=None, username=None, password=None):
    if (not password) or (not username):
        return None
#       username = input('Username: ')
#       password = getpass('Password(no echo): ')
    qDebug("in login")
    while True:
        session = _create_session()
        # qDebug("session")
        req = _get_login_page(session, url)
        # qDebug("page")
        captcha_id = re_search(r'img.src = \'captcha\?(.*)\'', req)
        # qDebug("captcha")
        if not captcha_id:
            qDebug('Captcha not found! Retrying...')
            sleep(3)
            continue
        captcha_id += get_timestamp()
        captcha_url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha?' +\
                      captcha_id
        _bypass_captcha(session, captcha_url)
        check = Captcha()
        if not check.exec_():
            session.close()
            return None
        code = check.captchaInput.text()
        qDebug(code)
        sid = re_search(r'sid" value="(.*?)"', req)
        returl = re_search(r'returl" value="(.*?)"', req)
        se = re_search(r'se" value="(.*?)"', req)
        client = re_search(r'client" value="(.*?)"', req)
        uuid = re_search(r'captcha\?uuid=(.*?)&t=', req)
        if not (sid and returl and se and uuid):
            qDebug('Params not found! Retrying...')
            sleep(3)
            continue

        res = _login(session, sid, returl, se, client,
                     username, password, code, uuid)

        if res == 2:
            parent.LogInfo.emit('[MSG]Wrong captcha! Try again!\n')
            qDebug('Wrong captcha! Try again!')
            continue
        elif res == 1:
            parent.LogInfo.emit(
                '[MSG]Wrong username or password! Try again!\n'
                )
            qDebug('Wrong username or password! Try again!')
            break
        elif res == 3:
            parent.LogInfo.emit(
                '[MSG]Opps! You are banned for 30s...Waiting...\n'
                )
            qDebug('Opps! You are banned for 30s...Waiting...')
            sleep(30)
            continue
        else:
            return session


# if __name__ == "__main__":
#     import json
#     url = "https://oc.sjtu.edu.cn/login/openid_connect"
#     url2 = "https://oc.sjtu.edu.cn/courses"
#     url3 = "https://oc.sjtu.edu.cn/courses/17256"
#     url4 = "https://oc.sjtu.edu.cn/courses/17256/files"
#     url5 = "https://oc.sjtu.edu.cn/api/v1/courses/17256/folders/root"
#     url6 = "https://oc.sjtu.edu.cn/api/v1/folders/77300/files"
#     url7 = "https://oc.sjtu.edu.cn/api/v1/folders/77300/folders"
#     url8 = "https://oc.sjtu.edu.cn/api/v1/folders/83455/folders"
#     session = login(url)


#    path = "./log/file_tree.json"
#    with open(path, 'r') as f:
#        data = f.read()
#    data = json.loads(data)
#    target = data['17230'][2]['content'][3]['name']
#    url = data['17230'][2]['content'][3]['url']
#    qDebug(url)
#    r = session.get(url, stream = True)
#    # r = requests.get(url, stream = True)
#    with open("{}".format(target), 'wb') as f:
#        for chunk in r.iter_content(chunk_size = 1024):
#            if chunk:
#                f.write(chunk)
#            sleep(0.002)
#    # data = session.get(url8)
#    # with open("source/empty_folders.json", "w") as f:
#    #     f.write(data.text)
#    # data = json.loads(data.text[9:])
#    # qDebug(data)
#    # qDebug(data[0])
#    session.close()
