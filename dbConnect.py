# -*- coding: utf-8 -*-

import pymysql
import redis


class dbConnect(object):

    @staticmethod
    def db():

        db = pymysql.connect("127.0.0.1", "root", "123456", "kingfisher")
        return db

    @staticmethod
    def redisCon():

        redisCon = redis.Redis(host='127.0.0.1', port=6379, db=0)
        return redisCon
