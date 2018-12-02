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
        # self.user_count = 49290
        self.user_count = 40001


    def read_rating(self):
        with open(self.rating_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                u, v, rating = int(row[0]), int(row[1]), int(row[2])
                if u > 40000 or v > 40000:
                    continue
                if u not in self.rating:
                    self.rating[u] = {}
                self.rating[u][v] = rating

    def read_trust(self):
        with open(self.trust_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            counter = 0
            for row in spamreader:
                
                u, v, trust = int(row[1]), int(row[2]), int(row[3])
                if u > 40000 or v > 40000:
                    continue
                if u not in self.trust:
                    self.trust[u] = {}
                self.trust[u][v] = trust

    def get_raw_data(self):
        print(len(self.rating), len(self.trust))
        return self.rating, self.trust

    def modified_bfs(self, user, depth, discount_factor = 1):
        local_graph = [[] for i in range(self.user_count+1)]
        pred = [[] for i in range (self.user_count+1)]
        level = [0 for i in range (self.user_count + 1)]
        q = queue.Queue()
        q.put(user)
        visited = [ 0 for i in range (self.user_count+1) ]
        visited[user] = 1
        prev_level = 0
        while not q.empty():
            cur_user = q.get()
            #print("Here ", cur_user)
                #print("Yay")
            # print("Visiting ", cur_user, " len of queue = ", q.qsize())
            visited[cur_user] = 1
            if level[cur_user] > prev_level:
                #print('>>>>>>>>>>>>>>>>>>>>')
                q2 = q
                prev_level = level[cur_user]
                while not q2.empty():
                    visited[q2.get()] = 1
            if level[cur_user] > depth:
                break
            if cur_user in self.trust:
                for k,v in self.trust[cur_user].items():
                    if visited[k] == 0:
                        local_graph[cur_user].append(k)
                        pred[k].append(cur_user)
                        level[k] = level[cur_user] + 1
                        l = []
                        q2 = q
                        while not q2.empty():
                            l.append(q2.get())
                        # l contains a copy of q
                        # ensuring the user doesn't get put twice
                        if k not in l:
                            q.put(k)

        trust_scores = {}
        q = queue.Queue()
        q.put(user)
        visited = [ 0 for i in range (self.user_count+1) ]
        visited[user] = 1

        level = [0 for i in range (self.user_count + 1)]
        discount_power = 0
        trust_scores[user] = 1

        # printing local graph
        # for i in range(self.user_count):
        #     if local_graph[i] != []:
        #         print(i, local_graph[i])


        prev_level = 0
        while not q.empty():
            cur_user = q.get()
            num = 0
            denom = 0
            # print("Current active User ", cur_user)
            for papa in pred[cur_user]: # assumes we know the ans for the predecessors of curr user
                if papa in trust_scores:
                    discount_power = level[cur_user]
                    if papa in trust_scores:
                        num += trust_scores[papa]*1*(discount_factor**discount_power)
                    denom += trust_scores[papa]
            if denom == 0:
                trust_scores[cur_user] = 1
            else:
                trust_scores[cur_user] = num/denom
            for v in local_graph[cur_user]:
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

    def modified_bfs_tidal(self, user, depth, discount_factor = 1):
        local_graph = [[] for i in range(self.user_count+1)]
        pred = [[] for i in range (self.user_count+1)]
        level = [0 for i in range (self.user_count + 1)]
        q = queue.Queue()
        q.put(user)
        visited = [ 0 for i in range (self.user_count+1) ]
        visited[user] = 1
        prev_level = 0
        while not q.empty():
            cur_user = q.get()
            # print("Here ", cur_user)
            #if q.qsize() > 0:
                # print("Yay")
            # print("Visiting ", cur_user, " len of queue = ", q.qsize())
            visited[cur_user] = 1
            if level[cur_user] > prev_level:
                # print('>>>>>>>>>>>>>>>>>>>>')
                q2 = q
                prev_level = level[cur_user]
                while not q2.empty():
                    visited[q2.get()] = 1
            if level[cur_user] > depth:
                break
            if cur_user in self.trust:
                for k,v in self.trust[cur_user].items():
                    if visited[k] == 0:
                        local_graph[cur_user].append(k)
                        pred[k].append(cur_user)
                        level[k] = level[cur_user] + 1
                        l = []
                        q2 = q
                        while not q2.empty():
                            l.append(q2.get())
                        # l contains a copy of q
                        # ensuring the user doesn't get put twice
                        if k not in l:
                            q.put(k)

        trust_scores = {}
        q = queue.Queue()
        q.put(user)
        visited = [ 0 for i in range (self.user_count+1) ]
        visited[user] = 1

        level = [0 for i in range (self.user_count + 1)]
        discount_power = 0
        trust_scores[user] = 1

        # printing local graph
        # for i in range(self.user_count):
        #     if local_graph[i] != []:
        #         print(i, local_graph[i])


        prev_level = 0
        while not q.empty():
            cur_user = q.get()
            trust_scores[cur_user] = 0
            if(cur_user == user):
                trust_scores[cur_user] = 1
            num = 0
            denom = 0
            # print("Current active User ", cur_user)
            for papa in pred[cur_user]: # assumes we know the ans for the predecessors of curr user
                if papa not in trust_scores:
                    trust_scores[cur_user] = max(trust_scores[cur_user], min(1, 1**level[cur_user]))
                else:
                    trust_scores[cur_user] = max(trust_scores[cur_user],min(1, trust_scores[papa]*discount_factor))

            for v in local_graph[cur_user]:
                if visited[v] == 0:
                    level[v] = level[cur_user] + 1
                    visited[v] = 1
                    q.put(v)
        return trust_scores

    def tidal_trust(self,depth):
        moletrust_matrix = {}
        for user in range(1, self.user_count):
            moletrust_matrix[user] = self.modified_bfs_tidal(user, depth) # { uid : weight, uid : w2 }
        return moletrust_matrix


    def get_test_data(self):
        pass