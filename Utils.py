import csv
import random
import math
import numpy as np
from sklearn.model_selection import KFold
import user_user
import item_item
import trust
import tidal_trust

def shuffle():
    rating_file = 'epinions/ratings_data.txt'
    data = []
    with open(rating_file, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for rows in file:
            if int(rows[0]) > 40000 or int(rows[1]) > 40000:
                continue
            data.append(rows)
        print(len(data))
        random.shuffle(data)
    return data

def shuffle_cold_start():
    rating_file = 'epinions/ratings_data.txt'
    train = []
    with open(rating_file, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for rows in file:
            if int(rows[0]) > 36000 or int(rows[1]) > 40000:
                continue
            train.append(rows)
        print(len(train))
        random.shuffle(train)

    test = []
    with open(rating_file, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for rows in file:
            if int(rows[0]) < 36000 or int(rows[0]) > 40000 or int(rows[1]) > 40000:
                continue
            test.append(rows)
        random.shuffle(test)
    return train, test

def read_list(data):
    data_dick = {}
    for row in data:
        u, v, rating = int(row[0]), int(row[1]), int(row[2])
        if u not in data_dick:
            data_dick[u] = {}
        data_dick[u][v] = rating
    return data_dick


def kfold():
    # solving regular problem
    data = np.array(shuffle())
    kf = KFold(n_splits=5)
    for train, test in kf.split(data):
        x = data[train]
        y = data[test]
        train_dick = read_list(x)
        test_dick = read_list(y)
        uu_mae = user_user.user_user_exec(train_dick, test_dick)
        print("User User = ", uu_mae)
        ii_mae = item_item.item_item_exec(train_dick, test_dick)
        print("Item Item = ", ii_mae)
        t_mae = trust.user_user_exec(train_dick, test_dick)
        print("Trust = ", t_mae)
        tidal_trust_mae = tidal_trust.user_user_exec(train_dick, test_dick)

    # # solving cold start problem
    # train, test = shuffle_cold_start()
    # x, y = train, test
    # train_dick = read_list(x)
    # test_dick = read_list(y)
    # uu_mae = user_user.user_user_exec(train_dick, test_dick)
    # print("User User = ", uu_mae)
    # ii_mae = item_item.item_item_exec(train_dick, test_dick)
    # print("Item Item = ", ii_mae)
    # t_mae = trust.user_user_exec(train_dick, test_dick)
    # print("Trust = ", t_mae)
    # tidal_trust_mae = tidal_trust.user_user_exec(train_dick, test_dick)

kfold()