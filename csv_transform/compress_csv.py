import csv
import os

fields = []
rows = []

path = os.getcwd() + "/dataset/"
# print(path)

files = os.listdir(path)

for file in files:
    print(file)
    if ".csv" not in file:
        continue
    with open(f"dataset/{file}", "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)


compress_by_category = {}
for row in rows:
    # properties = row.split(",")
    key = ",".join(row[:4])
    compress_by_category[key] = compress_by_category.get(key, 0) + 1


results = []
for k, v in compress_by_category.items():
    row = k.split(",") + [v]
    results.append(row)

print(len(compress_by_category.keys()))
print(results[0])

with open("dataset/202309.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerows(results)
