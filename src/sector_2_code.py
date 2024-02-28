from ast import literal_eval

import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tqdm import tqdm

data = pd.read_csv(
    "/Users/raphaelseo/Documents/projects/side_project/finance/Company_Clustering/sector.csv",
    index_col=0,
)

API_KEY = "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"

chat = ChatOpenAI(
    temperature=0,  # 모델의 창의성? 같은 것 낮을수록 덜 창의적이고 높을수록 창의적이고 무작위성을 보임
    streaming=True,
    model="gpt-3.5-turbo",
    api_key=API_KEY,
)

templates = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a corporate and business expert and you can only return one python list like ['test', 'test']",
        ),
        (
            "human",
            """아래의 리스트 내용 한글로 번역해서 파이썬 리스트로 반환해줘. {text}. 하나의 리스트 빼면 아무것도 출력하지마""",
        ),
    ]
)

summary = data["sector"]

res = []

for i in tqdm(summary):
    prompt = templates.format_messages(text=i)
    res.append(literal_eval(chat.predict_messages(prompt).content))

result = pd.DataFrame()
result["stock_code"] = data["stock_code"]
result["sector"] = res

result.to_csv(
    "/Users/raphaelseo/Documents/projects/side_project/finance/Company_Clustering/sector2.csv"
)
