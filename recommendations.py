# -*- coding: utf-8 -*-

from math import sqrt
import csv


# 使用欧几里德距离公式计算 两个人偏好的相似度
def sim_distance(prefs, person1, person2):
    si = {}
    # shared_iten 列表
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# 使用皮尔逊相关系数计算两个人相似度
def sim_pearson(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    # 对所有偏好求和
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    # 求平方和
    sum1Sq = sum([pow(prefs[person1][item], 2) for item in si])
    sum2Sq = sum([pow(prefs[person2][item], 2) for item in si])

    # 乘积之和
    pSum = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    # 计算皮尔逊评价值
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den
    # print(r)
    return r


# 从反应偏好的数据中返回最匹配者
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


# 构建商品相关的商品信息合集
def calculateSimilarItems(prefs, n=10):
    result = {}
    itemsPrefs = conversionData(prefs)
    c = 0
    for item in itemsPrefs:
        c += 1
        if c % 100 == 0:
            print("%d / %d" % (c, len(itemsPrefs)))
        scores = topMatches(itemsPrefs, item, n)
        result[item] = scores

    return result


# 基于用户对比 推荐商品
def getRecommendactions(prefs, person, n=10, similarity=sim_pearson):
    totals = {}
    simSums = {}

    for other in prefs:
        # 不和自己比较
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person]:
                # 相似度 * 评价值
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total / simSums[item], item)
                for item, total in totals.items() if simSums[item] != 0]

    rankings.sort()
    rankings.reverse()

    return rankings[0, n]


# 基于商品相关  推荐商品
def getRecommendactionItems(prefs, similarItems, user):
    if user in prefs:
        userRatings = prefs[user]
    else:
        return None

    scores = {}
    totalSim = {}

    for (item, rating) in userRatings.items():
        for (similar, item2) in similarItems[item]:
            if item2 in userRatings:
                continue

            # 未评价的商品 预测评价值总和
            scores.setdefault(item2, 0)
            scores[item2] += similar * rating

            # 未评价商品 相似值总和
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similar

    rankings = [(score / totalSim[item], item)
                for (item, score) in scores.items() if totalSim[item] != 0]
    rankings.sort()
    rankings.reverse()
    return rankings


# 转换数据 电影下用户评分集合
def conversionData(prefs):
    newData = {}

    for user, items in prefs.items():
        for movie, rating in items.items():
            newData.setdefault(movie, {})
            newData[movie][user] = float(rating)

    return newData
