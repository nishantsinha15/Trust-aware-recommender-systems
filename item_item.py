import math

item = {}
item_average = {}
user = {}
item_similarity = {}
user_average = {}


def item_item_predict(a, i, actual_rating):
    global item, item_average, user, item_similarity, user_average
    if(i not in item or a not in user):
        return actual_rating
    ans = item_average[i]
    j = 0
    num = 0.0
    den = 0.0
    for u,x in item.items():
        if u in user[a]:
            num = num + item_similarity[i][u] * (user[a][u] - user_average[a])
            den = den + item_similarity[i][u]
    if(den == 0.0 and num == 0.0):
        return ans
    else :
        return ans + num/den

def item_item_exec(train, test):
    global item, item_average, user, item_similarity, user_average
    user = train
    for k,v in user.items():
        for i, j in v.items():
            if i not in item:
                item[i] = {}
                item[i][k] = j
            elif k not in item[i]:
                item[i][k] = j

    for k, v in item.items():
        item_average[k] = 0.0
        for i, j in v.items():
            item_average[k] += j
        item_average[k] = item_average[k] / len(v)

    # In[43]:

    user_average = {}
    for k, v in user.items():
        user_average[k] = 0.0
        for i, j in v.items():
            user_average[k] += j
        user_average[k] = user_average[k] / len(v)

    # In[44]:

    item_similarity = {}
    for u, x in item.items():
        item_similarity[u] = {}
        for v, z in item.items():
            mod_u = 0.0
            mod_v = 0.0
            sim = 0.0
            for key, val in item[u].items():
                if key in item[v]:
                    rating_v = item[v][key]
                    sim = sim + val * rating_v
                    mod_u = mod_u + val * val
                    mod_v = mod_v + rating_v * rating_v
            mod_u = math.sqrt(mod_u)
            mod_v = math.sqrt(mod_v)
            if (mod_u * mod_v > 0.0):
                item_similarity[u][v] = sim / (mod_u * mod_v)
            else:
                item_similarity[u][v] = 0.0


    error = 0.0
    sz = 0
    content_test = test
    for k, v in content_test.items():
        for i,j in v.items():
            error = error + (abs(j - item_item_predict(k, i, j)))*2
        sz += len(v)
    error = error / sz
    print(error)
    return error

