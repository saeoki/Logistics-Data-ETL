import csv
import os

fields = []
rows = []

path = os.getcwd()
# print(path)

files = os.listdir(path)


for file in files:
    if ".csv" in file:
        print(file)
        with open(file, "r", newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)

            for row in csvreader:
                newrow = [row[0], row[-7], " ".join(row[-4:-1]), row[-1]]
                rows.append(newrow)


print(rows[0])
print(len(rows))
# print(len(compress_by_category.keys()))

with open("20220112.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)
