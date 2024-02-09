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


chat = ChatOpenAI(
    temperature=0,  # 모델의 창의성? 같은 것 낮을수록 덜 창의적이고 높을수록 창의적이고 무작위성을 보임
    streaming=True,
    model="gpt-3.5-turbo-1106",
    api_key="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",
)

summarization = []

templates = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a corporate and business expert"),
        (
            "human",
            "Given the following document, summarize the main businesses of this company. {text}",
        ),
    ]
)

reduce_templates = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a corporate and business expert"),
        (
            "human",
            "Given the following str list, summarize the main businesses of this company. {str_list}",
        ),
    ]
)

text_splitter = TokenTextSplitter(chunk_size=16385, chunk_overlap=0)


for i in tqdm(data.index):
    res: List[str] = []
    texts = text_splitter.split_text(data["full"][i])
    if len(texts) != 1:
        for text in texts:
            prompt = templates.format_messages(text=text)
            res.append(str(chat.predict_messages(prompt).content))
        # prompt = templates.format_messages(text=" ".join(res))
        reduce_prompt = reduce_templates.format_messages(str_list=res)
        final_result = chat.predict_messages(reduce_prompt)
        summarization.append(final_result.content)
    else:
        prompt = templates.format_messages(text=data["full"][i])
        summarization.append(str(chat.predict_messages(prompt).content))
data2 = pd.DataFrame()
data2["stock_code"] = data.index
data2["summarization"] = summarization

data2.to_csv(
    "/Users/raphaelseo/Documents/projects/side_project/finance/Company_Clustering/summary.csv"
)
