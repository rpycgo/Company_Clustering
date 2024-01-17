import json
import time
from typing import Tuple

import pandas as pd
import requests
from tqdm import tqdm

from dh_utils.constant_dh import OG_URL, SRC_URL
from dh_utils.utils_dh import check_count, del_blank, find_dcmNo, text_from_url


def main(rcpno: str, cnt: int) -> Tuple[dict, int]:
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


if __name__ == "__main__":
    df = pd.read_csv("./반기보고서_코드.csv")
    stock_rcpno = df.to_dict("records")
    result = {}
    cnt = 0
    for dic in tqdm(stock_rcpno):
        rcpno = dic["rcept_no"]
        res, cnt = main(rcpno, cnt)
        result[str(dic["stock_code"])] = res
    with open("./result.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
