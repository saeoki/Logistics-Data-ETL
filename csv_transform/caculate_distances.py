import pandas as pd
import haversine as hs

geo3 = pd.read_csv("output3.csv")

print(geo3.head())

distances = []
for i in geo3.index:
    for j in geo3.index:
        if i != j:
            loc1 = (geo3.loc[i, "위도"], geo3.loc[i, "경도"])
            loc2 = (geo3.loc[j, "위도"], geo3.loc[j, "경도"])
            distance = hs.haversine(loc1, loc2)
            distances.append(
                {
                    "src_region": geo3.loc[i, "행정구역 코드"],
                    "dest_region": geo3.loc[j, "행정구역 코드"],
                    "distance": distance,
                }
            )

distances_df = pd.DataFrame(distances)

distances_df.to_csv("distances.csv", index=False)
