# -*- coding: utf-8 -*-
from dbConnect import dbConnect

# '整理推荐商品需要的数据类'


class dataCollation(object):

    def __init__(self):
        self.db = dbConnect.db()

    def userData(self):
        data = {}
        users = self.user()
        for user_id in users:
            data.setdefault(user_id, {})
            data[user_id] = self.userBuySkuMoney(user_id)

        return data

    # 用户购买的sku和总金额统计
    def userBuySkuMoney(self, user_id):
        cursor = self.db.cursor()
        sql = 'SELECT order_sku_relation.sku_id,order_sku_relation.quantity,order_sku_relation.price,order_sku_relation.discount FROM `order` inner join `order_sku_relation` ON order.id=order_sku_relation.order_id WHERE order.type=6 and order.user_id=' + str(user_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        data = []
        for item in results:
            sku_id = item[0]
            quantity = item[1]
            price = item[2]
            discount = item[3]
            data.append({'sku_id': sku_id, 'quantity': quantity,
                         'price': price, 'discount': discount})

        # sku和对应的货款金额
        sku_money = {}
        for item in data:
            sku_money.setdefault(item['sku_id'], 0.00)
            sku_money[item['sku_id']] += item['quantity'] * \
                (float(item['price']) - float(item['discount']))
        return sku_money

    # 获取分销商用户ID 列表
    def user(self):
        cursor = self.db.cursor()
        sql = 'SELECT id FROM users WHERE type=1'
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        data = []
        for item in results:
            id = item[0]
            data.append(id)

        return data
