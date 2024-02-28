from ast import literal_eval

import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tqdm import tqdm

data = pd.read_csv(
    "/Users/raphaelseo/Documents/projects/side_project/finance/Company_Clustering/summary_business.csv",
    index_col=0,
)

API_KEY = "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"

chat = ChatOpenAI(
    temperature=0,  # 모델의 창의성? 같은 것 낮을수록 덜 창의적이고 높을수록 창의적이고 무작위성을 보임
    streaming=True,
    model="gpt-3.5-turbo-1106",
    api_key=API_KEY,
)

templates = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a corporate and business expert and you can only python list",
        ),
        (
            "human",
            """In the following sentence, return just the business sector as a Python list in only string without any other verbiage. 
            위에서 생성한 리스트를 KSIC에 따른 코드분류로 분류한 리스트를 반환해줘. {text}""",
        ),
    ]
)

summary = data["summarization"]

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
