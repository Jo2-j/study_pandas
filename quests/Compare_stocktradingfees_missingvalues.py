# - target : Mongo(compare_stocktradingfees_merges)
# - from Mongo with query : {'구분' : '변경후'}

import pandas as pd
import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.0.46:27017/')
db_name = client['DB_SGMN']
collection_name = db_name['COL_FEE_RATES']

# 1. 변경후만 가져오기

rawData = collection_name.find({
    "Unnamed: 4": "변경후"
})

postChgData = list(rawData)

# 2. DataFrame으로 변환

df = pd.DataFrame(postChgData)

# 3. 필요없는 컬럼 삭제(필요한 컬럼만 선택)


df = pd.DataFrame(postChgData)[['Unnamed: 0',
                                'Unnamed: 2',
                                'Unnamed: 3', 
                                'HTS', 
                                '스마트폰']]

print("-------")

                            


# 4.1 결측치 임의로 0으로 채우기
# 0으로 채우고 그 행 드롭
# 유실되는 데이터가 많을 것 같음

# 특정 컬럼만 처리
columns_to_check = ['HTS', '스마트폰']  # 처리할 컬럼명 지정
df_filled = df.copy()
df_filled[columns_to_check] = df_filled[columns_to_check].fillna(0)
rows_with_zeros = df_filled[columns_to_check].isin([0]).any(axis=1)
df_no_zeros = df_filled[~rows_with_zeros]
# 5. 필요한 컬럼 생성 

df_no_zeros['수수료 합'] = df['HTS'] + df['스마트폰']

finalSeries = df_no_zeros['수수료 합']

meanResult = finalSeries.mean()

print("----------")

# 4.2 결측치 상대값으로 채우기

# 만약 HTS에서 값이 있지만, 스마트폰에 없으면 HTS의 것을 채우자
# 만약 HTS에서 값이 없지만, 스마트폰에 값이 있으면 스마트폰의 것을 채우자

# df['HTS'] = df['HTS'].fillna(0)
# df['스마트폰'] = df['스마트폰'].fillna(0)


# 5.

# 4.1 방법 사용
underMean = df_no_zeros[df_no_zeros['수수료 합'] < meanResult]

print("----------")

# - 스마트폰 수수료 평균 이상인 증권사들 파일(CSV) 저장