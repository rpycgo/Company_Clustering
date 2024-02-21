import pandas as pd
import pickle
import re
import openai
from bs4 import BeautifulSoup
from tqdm import tqdm



def summarize(prompt, query, model):
    query = re.sub('\\s{2,}', '', query)
    query = f'''
    {prompt}
    
    {query}
    '''

    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": query
    }]

    return openai.ChatCompletion.create(model=model, messages=messages)


# if __name__ == '__main__':
#     data = pd.read_pickle('./reports_1_3.pkl').get('q1')
#     data = {key: value for key, value in data.items() if value.get('company_info')}
    
#     OPENAI_API_KEY = ''
#     openai.api_key = OPENAI_API_KEY
#     model = "gpt-3.5-turbo-0125"
    
#     for i, (key, value) in enumerate(tqdm(data.items())):
#         try:
#             company_info_summarized = summarize(
#                 '회사 주요 내용 짧게 요약해줘',
#                 BeautifulSoup(value.get('company_info'), 'lxml').text,
#                 model,
#                 )
#         except:
#             company_info_summarized = ''
            
#         try:
#             business_info_summarized = summarize(
#                 '사업 주요 내용 짧게 요약해줘',
#                 BeautifulSoup(value.get('business_info'), 'lxml').text,
#                 model,
#                 )
#         except:
#             business_info_summarized = ''
        
#         value.update({
#             'company_info_summarized': company_info_summarized,
#             'business_info_summarized': business_info_summarized,
#         })
        
#         if i%5 == 0:
#             with open('./reports_1_summarize_by_gpt.pkl', 'wb') as file:
#                 pickle.dump(data, file)
