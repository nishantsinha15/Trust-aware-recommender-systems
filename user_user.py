import math
import Reader
import Utils

average = {}
user = {}
ordered_users = {}
similarity = {}
K = 20
def user_user_predict(a, i):
    ans = average[a]
    tk = 0
    j = 0
    top_k_users = []
    while (j < K):
        if (i in user[ordered_users[a][j][1]]):
            top_k_users.append(ordered_users[a][j][1])
            tk += 1
        j += 1
    num = 0.0
    den = 0.0
    for j in top_k_users:
        num = num + similarity[a][j] * (user[j][i] - average[j])
        den = den + similarity[a][j]
    if (len(top_k_users) == 0):
        return average[a]
    ans = ans + num / den
    return ans

def user_user_exec(train, test):
    user = train
    content_test = test
    reader = Reader.Reader()
    user, trust = reader.get_raw_data()

    average = {}
    for k, v in user.items():
        average[k] = 0.0
        for i, j in v.items():
            average[k] += j
        average[k] = average[k] / len(v)

    similarity = {}
    for u, x in user.items():
        print(u)
        similarity[u] = {}
        for v, z in user.items():
            mod_a = 0.0
            mod_v = 0.0
            sim = 0.0
            for key, val in user[u].items():
                if key in user[v]:
                    rating_v = user[v][key]
                    sim = sim + val * rating_v
                    mod_a = mod_a + val * val
                    mod_v = mod_v + rating_v * rating_v
            mod_a = math.sqrt(mod_a)
            mod_v = math.sqrt(mod_v)
            if (mod_a * mod_v > 0.0):
                similarity[u][v] = sim / (mod_a * mod_v)
            else:
                similarity[u][v] = 0.0
    print('Similarity computed')
    ordered_users = {}
    for u in user:
        ordered_users[u] = []
        for k, v in similarity[u].items():
            ordered_users[u].append((v, k))
        ordered_users[u].sort(reverse=True)

    print("Done: Ordered Users")

    error = 0.0
    sz = 0
    for k,v in content_test.items():
        for i,j in v.items():
            error = error + abs(j - user_user_predict(k, i))
        sz = sz + len(v)
    error = error / sz
    print(error)
    return error
