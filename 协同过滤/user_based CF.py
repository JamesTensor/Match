# *_*coding:utf-8 *_*
import math
from operator import itemgetter

def UserSimilarity(train):
    # build inverse table for item_users
    item_users = dict()
    #第一个for，取出每一个评分数据中的用户和物品.
    for u, items in train.items():
        #第二个for取出物品的每个发生行为的用户.
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    #计算用户对之间有过的共同行为物品数量
    C = dict()
    N = dict()
    # 建立倒排表
    for i, users in item_users.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                C[u][v] += 1 / math.log(1 + len(users))

    # 计算相似度矩阵 W
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W

def Recommend(user, train, W):
    rank = dict()
    interacted_items = train[user]
    #wuv是用户相似度，rvi是i用户的推荐分数
    for v, wuv in sorted(W[u].items, key=itemgetter(1), reverse=True)[0:K]:
        for i, rvi in train[v].items:
            if i in interacted_items:
                #过滤
                continue
            rank[i] += wuv * rvi
    return rank