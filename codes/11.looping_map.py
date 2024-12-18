def add_elements(first, second=1):
    result =  first + second
    return result

list_first = [1, 2, 3]
list_second = [4, 5, 6]

#with zip 두 데이터가 분리가 되어있지만 성격이 동일함
# 1,4
# 2,5
# 3,6

# for 이해
result_list = list()
# use one parameter

# for number_first, number_second in zip(list_first, list_second):
#     result = add_elements(number_first)
#     result_list.append(result)
# result_list
pass

# # map() : callback function for을 안에 포함
# result_map = map(add_elements, list_first)
# result_map_list = list(result_map)
# pass

# apply() with pandas
data = {'col_first': list_first, 'col_second': list_second}
import pandas as pd

df_first = pd.DataFrame(data)
pass

# result_df = df_first['col_first'].apply(add_elements)
# pass
