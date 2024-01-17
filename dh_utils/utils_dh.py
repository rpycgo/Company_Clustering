import re
import time
from typing import Tuple

import requests
from bs4 import BeautifulSoup as bs

from dh_utils.constant_dh import DCMNO_REGEX, ELEID_REGEX, RCPNO_REGEX


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
