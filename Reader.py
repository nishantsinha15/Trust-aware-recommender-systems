import csv
import queue
'''
user_id is in [1,49290]
item_id is in [1,139738]
rating_value is in [1,5]
trust value is always 1
'''


class Reader:
    def __init__(self):
        self.trust = {}
        self.rating = {}
        self.rating_file = 'epinions/ratings_data.txt'
        self.trust_file = 'epinions/trust_data.txt'
        self.read_rating()
        self.read_trust()
        self.user_count = 49290
        self.limit = 1000


    def read_rating(self):
        with open(self.rating_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            counter = 0
            for row in spamreader:
                counter+=1
                if counter == 1000:
                    break
                u, v, rating = int(row[0]), int(row[1]), int(row[2])
                if u not in self.rating:
                    self.rating[u] = {}
                self.rating[u][v] = rating

    def read_trust(self):
        with open(self.trust_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                u, v, trust = int(row[1]), int(row[2]), int(row[3])
                if u not in self.trust:
                    self.trust[u] = {}
                self.trust[u][v] = trust

    def get_raw_data(self):
        return self.rating, self.trust

    def modified_bfs(self, user, depth, discount_factor = 1):
        local_graph = [[] * (self.user_count+1)]
        pred = [[] * (self.user_count+1)]
        level = [0 * (self.user_count + 1)]
        q = queue()
        q.put(user)
        visited = [ 0 * (self.user_count+1) ]
        visited[user] = 1
        prev_level = 0
        while not q.empty():
            cur_user = q.get()
            visited[cur_user] = 1
            if level[cur_user] > prev_level:
                temp_list = list(q)
                prev_level = level[cur_user]
                for nodes in temp_list:
                    visited[nodes] = 1
            if level[cur_user] > depth:
                break
            for k,v in self.trust[cur_user]:
                if visited[v] == 0:
                    local_graph[cur_user].append(v)
                    pred[v].append(cur_user)
                    level[k] = level[cur_user] + 1
                    if v not in q:
                        q.put(v)

        trust_scores = {}
        q = queue()
        q.put(user)
        visited = [ 0 * (self.user_count+1) ]
        visited[user] = 1

        level = [0 * (self.user_count + 1)]
        discount_power = 0
        while not q.empty():
            cur_user = q.get()
            num = 0
            denom = 0
            for papa in pred[cur_user]:
                discount_power = level[cur_user]
                num += trust_scores[papa]*1*(discount_factor**discount_power)
                denom += trust_scores[papa]
            trust_scores[cur_user] = num/denom
            for k,v in local_graph[cur_user]:
                if visited[v] == 0:
                    level[v] = level[cur_user] + 1
                    visited[v] = 1
                    q.put(v)
        return trust_scores

    def moletrust(self,depth):
        moletrust_matrix = {}
        for user in range(1, self.user_count):
            moletrust_matrix[user] = self.modified_bfs(user, depth) # { uid : weight, uid : w2 }
        return moletrust_matrix

    def get_test_data(self):
        pass