import json

import pandas as pd
from src.utils_dh import crawl_first_page
from tqdm import tqdm


def main(
    data_path: str, save_path: str
) -> None:  # save_path의 경우 저장할 위치에 원하는 json 파일명으로 입력
    df = pd.read_csv(data_path)
    stock_rcpno = df.to_dict("records")
    result = {}
    cnt = 0
    for dic in tqdm(stock_rcpno):
        rcpno = dic["rcept_no"]
        res, cnt = crawl_first_page(rcpno, cnt)
        result[str(dic["stock_code"]).zfill(6)] = res
    with open(save_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main("./반기보고서_코드.csv", "./first_page.json")
