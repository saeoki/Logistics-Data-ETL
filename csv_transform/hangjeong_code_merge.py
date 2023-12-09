import pandas as pd

geo2 = pd.read_csv("output2.csv")
code = pd.read_excel("dataset/hangjeong_code.xlsx", sheet_name=0)

geo2.reset_index(inplace=True)

for i in geo2.index:
    try:
        sido_name = geo2.loc[i, "시도"]
        sigungu_name = geo2.loc[i, "시군구"]
        dong_name = geo2.loc[i, "읍면동/구"]
        # print(geo[sheet].loc[i, "시도"])
        #    print(i, geo2.loc[i, "시군구"])
        # print(geo[sheet].loc[i, "읍면동/구"])
        sido_code = code.loc[code["시도명칭"] == sido_name, "시도코드"].values[0]
        sigungu_code = "000"
        dong_code = "000"
        if not pd.isna(sigungu_name):
            sigungu_code = code.loc[
                (code["시군구명칭"] == sigungu_name) & (code["시도명칭"] == sido_name), "시군구코드"
            ].values[0]

        if not pd.isna(dong_name):
            dong_name = (
                "".join(dong_name.rsplit("제", 1)) if "제" in dong_name else dong_name
            )
            geo2.loc[i, "읍면동/구"] = dong_name
            dong_code = code.loc[
                (code["시군구명칭"] == sigungu_name)
                & (code["시도명칭"] == sido_name)
                & (code["읍면동명칭"] == dong_name),
                "읍면동코드",
            ].values[0]
        geo2.loc[i, "행정구역 코드"] = (
            str(sido_code) + "{:03}".format(sigungu_code) + "{:03}".format(dong_code)
        )
        # print(geo2.loc[i, "행정구역 코드"])
    except IndexError:
        continue

geo2 = geo2.drop("읍/면/리/동", axis=1)
geo2 = geo2.drop("리", axis=1)

geo2["행정구역 코드"] = pd.to_numeric(geo2["행정구역 코드"], errors="coerce")
geo2 = geo2.dropna(subset=["행정구역 코드"])
geo2["행정구역 코드"] = geo2["행정구역 코드"].astype(int)

geo2.to_csv("output3.csv", index=False)
