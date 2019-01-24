import csv


def csv_sort(file, i=0):
    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in sorted(reader, key=lambda x: int(x[i]) if x[i].isdigit() else x[i]):
            yield row


file_name = "ir-analytics.csv"
writer = csv.writer(open('cov_' + file_name, 'w', newline=''))

for row in csv_sort(file_name):
    writer.writerow(row)
