import pandas as pd

import numpy as np

# 행정구역 별 코드를 추가로 더하고, 좌표를 이용하여 거리를 구하는 코드
geo = pd.read_excel("dataset/hangjeong_geo.xlsx", sheet_name=None)
# 1. 행정구역 별 좌표를 불러온다.


# print(code.head())

for sheet in geo:
    drop_list = []
    # print(sheet)
    for i in geo[sheet].index:  # 1.1.1 리 단위 정보는 제외하고 가져온다.
        if not pd.isna(geo[sheet].loc[i, "읍/면/리/동"]):
            if geo[sheet].loc[i, "읍/면/리/동"][-1] == "리":
                drop_list.append(i)
        if not pd.isna(geo[sheet].loc[i, "리"]):
            drop_list.append(i)
    for i in drop_list:
        geo[sheet].drop(i, inplace=True)

# '읍/면/리/동'에 동이 존재하는 경우엔 시도, 시군구, 읍면동/구, 읍/면/리/동 -> 시도, 시군구+읍면동/구, 읍/면/리/동으로 나누어서 저장한다.
for sheet in geo:
    geo[sheet].reset_index(inplace=True)
    # print(sheet)
    for i in geo[sheet].index:  # 1.1.1 리 단위 정보는 제외하고 가져온다.
        if not pd.isna(geo[sheet].loc[i, "읍/면/리/동"]):
            si = geo[sheet].loc[i, "시군구"]
            gu = geo[sheet].loc[i, "읍면동/구"]
            dong = geo[sheet].loc[i, "읍/면/리/동"]
            geo[sheet].loc[i, "시군구"] = si + " " + gu
            geo[sheet].loc[i, "읍면동/구"] = dong
            # print(geo[sheet].loc[i, "시군구"])

# 모든 sheet의 DataFrame을 합침
all_data = pd.concat(geo.values(), ignore_index=True)

# 합친 DataFrame을 CSV 파일로 저장
all_data.to_csv("output2.csv", index=False)
