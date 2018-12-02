import csv

ar = []
with open('trust_data.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader: 
        row = row[1:]   	
        u, v, rating = int(row[0]), int(row[1]), int(row[2])
        if u > 1000 or v > 1000:
            continue
        ar.append(row)


with open('sub_graph.csv', 'w') as writeFile:
    writer = csv.writer(writeFile, delimiter=' ')
    writer.writerows(ar)