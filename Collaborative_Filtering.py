# Basic CF( User-User and Item-Item )
# Trust All
# MT1
# MT2
# MT3
import Reader

K = 20

user, trust = Reader.get_raw_data()


average = {}
for k,v in user.items():
    average[k] = 0.0
    for i,j in v.items():
        average[k] += j
    average[k] = average[k] / len(v)