# *_*coding:utf-8 *_*
import math
from operator import itemgetter

def ItemSimilarity(train):
    #计算物品之间的共同的用户数，加惩罚项
    C = dict()
    N = dict()
    for users, items in train.items():
        for i in users:
            N[i] += 1
            for j in users:
                if i == j:
                    continue
            C[i][j] += 1 / math.log(1 + len(items) * 1.0)

    #计算相似度矩阵 W
    W = dict()
    for i,related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W


def Recommendation(train, user_id, W, K):
    rank = dict()
    ru = train[user_id]
    for i,pi in ru.items():
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            rank[j].weight += pi * wj
            rank[j].reason[i] = pi * wj
    return rank
