import re
import time
from typing import Tuple

import requests
from bs4 import BeautifulSoup as bs

RCPNO_REGEX: str = r'''node[0-9]\['rcpNo'\]\s*=\s*"[0-9]*"'''
DCMNO_REGEX: str = r'''node[0-9]\['dcmNo'\]\s*=\s*"[0-9]*"'''
ELEID_REGEX: str = r'''node[0-9]\['eleId'\]\s*=\s*"[0-9]*"'''

OG_URL = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcpno}"  # 브라우저를 통해서 직접 DART를 접속했을시에 표시되는 url (original_url)
SRC_URL = "https://dart.fss.or.kr/report/viewer.do?rcpNo={rcpno}&dcmNo={dcmNo}&eleId={id}&offset=800&length=4053&dtd=dart3.xsd"


def find_rcpNo(text: str) -> int:
    rcpNo = re.findall(RCPNO_REGEX, text)
    num = re.findall(r"[0-9]+", str(rcpNo[0]))[-1]
    return int(num)


def find_dcmNo(text: str) -> int:
    dcmNo = re.findall(DCMNO_REGEX, text)
    num = re.findall(r"[0-9]+", str(dcmNo[0]))[-1]
    return int(num)


def find_max_eleid(text: str) -> int:
    id_ls = re.findall(ELEID_REGEX, text)
    max_id = re.findall(r"[0-9]+", str(id_ls[-1]))
    return int(max_id[-1])


def del_blank(text: str) -> str:
    text = re.sub("\s{2,}", " ", text)
    text = re.sub("\n", " ", text)
    return text.strip()


def text_from_url(url: str) -> str:
    req = requests.get(url).text
    soup = bs(req, "lxml")
    try:
        text = soup.select("body")[0].get_text()
    except IndexError:
        text = ""
    return text


def check_count(cnt: int, start: float) -> Tuple[int, float]:
    if cnt == 99:
        diff = time.time() - start
        if diff < 60:
            time.sleep(round(60 - diff) + 1)
            cnt = 0
            start = time.time()
    else:
        cnt += 1
    return (cnt, start)


def crawl(rcpno: str, cnt: int) -> Tuple[dict, int]:
    res = {}
    og = OG_URL.format(rcpno=rcpno)
    start = time.time()
    req = requests.get(og).text
    cnt, start = check_count(cnt, start)
    change = req.find("정 정 신 고")
    dcmNo = find_dcmNo(req)
    if change == -1:
        id = [4, 10]
    else:
        id = [6, 12]
    for i in id:
        src = SRC_URL.format(rcpno=rcpno, dcmNo=dcmNo, id=i)
        text = text_from_url(src)
        cnt, start = check_count(cnt, start)
        text = del_blank(text)
        if i == id[0]:
            res["회사의 개요"] = text
        else:
            res["사업의 개요"] = text

    return (res, cnt)


def crawl_first_page(rcpno: str, cnt: int) -> Tuple[dict, int]:
    res = {}
    og = OG_URL.format(rcpno=rcpno)
    start = time.time()
    req = requests.get(og).text
    cnt, start = check_count(cnt, start)
    # change = req.find("정 정 신 고")
    dcmNo = find_dcmNo(req)
    # if change == -1:
    #     id = [4, 10]
    # else:
    #     id = [6, 12]
    # for i in id:
    src = SRC_URL.format(rcpno=rcpno, dcmNo=dcmNo, id=1)
    text = text_from_url(src)
    cnt, start = check_count(cnt, start)
    text = del_blank(text)
    # if i == id[0]:
    #     res["회사의 개요"] = text
    # else:
    #     res["사업의 개요"] = text
    res["text"] = text
    return (res, cnt)
