import csv

with open("products.csv", "r") as in_file, open("final.csv", "w") as to_file:
    writer = csv.writer(to_file, delimiter = ",", quotechar="'", quoting=csv.QUOTE_ALL)
    reader = csv.reader(in_file, delimiter=",",quotechar='"', quoting=csv.QUOTE_ALL)
    seen = set()
    for row in reader:
        try:
            if row[0] in seen:
                continue
            seen.add(row[0])
            writer.writerow(row)
        except Exception:
           pass

    in_file.close()
    to_file.close()






