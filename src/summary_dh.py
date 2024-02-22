from typing import List

import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import TokenTextSplitter
from tqdm import tqdm

data = pd.read_json(
    "/Users/raphaelseo/Documents/projects/side_project/finance/Company_Clustering/result.json"
).T

data["full"] = data["사업의 개요"] + data["회사의 개요"]

API_KEY = "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"

chat = ChatOpenAI(
    temperature=0,  # 모델의 창의성? 같은 것 낮을수록 덜 창의적이고 높을수록 창의적이고 무작위성을 보임
    streaming=True,
    model="gpt-3.5-turbo-1106",
    api_key=API_KEY,
)

summarization = []

templates = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a corporate and business expert"),
        (
            "human",
            "Summarize the company's main businesses in one line using English using the following text. {text}",
        ),
    ]
)

reduce_templates = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a corporate and business expert"),
        (
            "human",
            "Summarize the company's main businesses in one line using English using the following list. {str_list}",
        ),
    ]
)

text_splitter = TokenTextSplitter(chunk_size=16385, chunk_overlap=0)

index_ls = list(data.index)

target = index_ls
for i in tqdm(target):
    res: List[str] = []
    texts = text_splitter.split_text(data["사업의 개요"][i])
    if len(texts) != 1:
        for text in texts:
            prompt = templates.format_messages(text=text)
            res.append(str(chat.predict_messages(prompt).content))
        # prompt = templates.format_messages(text=" ".join(res))
        reduce_prompt = reduce_templates.format_messages(str_list=res)
        final_result = chat.predict_messages(reduce_prompt)
        summarization.append(final_result.content)
    else:
        prompt = templates.format_messages(text=data["사업의 개요"][i])
        summarization.append(str(chat.predict_messages(prompt).content))
data2 = pd.DataFrame()
data2["stock_code"] = target
data2["summarization"] = summarization

data2.to_csv(
    "/Users/raphaelseo/Documents/projects/side_project/finance/Company_Clustering/summary_business.csv"
)
