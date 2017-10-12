# -*- coding: utf-8 -*-

import pymysql
import redis

class dbConnect(object):

    # mysql 连接
    _db = None

    # redis连接
    _redisCon = None
    
    @staticmethod
    def db():
        if dbConnect._db:
            return dbConnect._db
        else:
            dbConnect._db = pymysql.connect("127.0.0.1", "root", "123456", "kingfisher")
            return dbConnect._db

    @staticmethod
    def redisCon():
        if dbConnect._redisCon:
            return dbConnect._redisCon
        else:
            dbConnect._redisCon = redis.Redis(host='127.0.0.1',port=6379,db=0)
            return dbConnect._redisCon