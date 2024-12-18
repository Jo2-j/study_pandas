import pandas as pd
import numpy as np
from pymongo import MongoClient


client = MongoClient('mongodb://192.168.0.46:27017/')
db_name = client['DB_SGMN']
collection_name = db_name['COL_FEE_RATES']

# 1. 변경후 데이터 가져오기
rawData = collection_name.find({"Unnamed: 4": "변경후"})
postChgData = list(rawData)


# 2. DataFrame으로 변환 및 필요한 컬럼만 선택
df = pd.DataFrame(postChgData)[['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 3', '스마트폰.1', '스마트폰']]

df = df.rename(columns={
    'Unnamed: 0': '증권사명',
    'Unnamed: 2': '기준일',
    'Unnamed: 3': '거래대금',
    '스마트폰.1': '은행 개설 계좌',
    '스마트폰': '증권사 개설 계좌'
})

# 3. 데이터 전처리
# NaN 값 처리
columns_to_check = ['은행 개설 계좌', '증권사 개설 계좌']  # 처리할 컬럼명 지정
df_filled = df.copy()
df_filled[columns_to_check] = df_filled[columns_to_check].fillna(0)

# 은행 계좌가 0인 경우, 증권사 계좌 값으로 채우기
zeroBankAccount = df_filled['은행 개설 계좌'] == 0
df_filled.loc[zeroBankAccount, '은행 개설 계좌'] = df_filled.loc[zeroBankAccount, '증권사 개설 계좌']

# 증권사 계좌가 0인 경우, 은행 계좌 값으로 채우기
zeroSecAccount = df_filled['증권사 개설 계좌'] == 0
df_filled.loc[zeroSecAccount, '증권사 개설 계좌'] = df_filled.loc[zeroSecAccount, '은행 개설 계좌']

# 새로운 컬럼 추가
df_filled['수수료합'] = df_filled['증권사 개설 계좌'] + df_filled['은행 개설 계좌']

# 거래대금 컬럼을 숫자로 변환
df_filled['거래대금'] = df_filled['거래대금'].str.replace('원', '').replace(
    {'억': '*100000000', '만': '*10000'}, regex=True).map(eval)


# 수수료율 계산 (수수료합 / 거래대금)
df_filled['수수료율'] = df_filled['수수료합'] / df_filled['거래대금'] * 2

finalSeries = df_filled['수수료율']

meanResult = finalSeries.mean()

# 4. 회사별

# 1. 회사별 평균 계산
company_means = df_filled.groupby('증권사명')['수수료율'].mean()

# 2. 원래 DataFrame의 수수료율을 회사별 평균으로 대체
df_filled['수수료'] = df_filled['증권사명'].map(company_means)

# 3. 증권사별로

# 증권사명으로 그룹화하여 나열
grouped_df = df_filled.groupby('증권사명').agg({
    '수수료율': 'mean'
}).round(4)

grouped_df = grouped_df.reset_index()

# 전체 평균보다 작은 증권사들 필터링
low_fee_companies = grouped_df[grouped_df['수수료율'] < meanResult]

# 수수료율 오름차순으로 정렬
low_fee_companies = low_fee_companies.sort_values('수수료율', ascending=True)




print("------------")