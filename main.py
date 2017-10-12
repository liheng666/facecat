# -*- coding: utf-8 -*-


from flask import Flask
from flask import request
import json
import recommendations

from dataCollation import dataCollation
from dbConnect import dbConnect


app = Flask(__name__)


@app.route('/updateRecommendDate')
def index():
    data = dataCollation().userData()
    similarItems = recommendations.calculateSimilarItems(data)

    json_data = json.dumps(data)
    jsonSimilarItems = json.dumps(similarItems)

    redis_con = dbConnect.redisCon()
    if not redis_con.set('recommendUserDate', json_data):
        return 'error'

    if not redis_con.set('similarItems', jsonSimilarItems):
        return 'error'

    return 'ok'


# 根据用户ID推荐商品
@app.route('/recommend')
def recommend():

    user_id = request.args.get("user_id")

    redis_con = dbConnect.redisCon()
    prefs = redis_con.get('recommendUserDate')
    similarItems = redis_con.get('similarItems')

    prefs = json.loads(prefs)
    similarItems = json.loads(similarItems)

    return json.dumps(recommendations.getRecommendactionItems(prefs, similarItems, user_id))


if __name__ == '__main__':
    app.run(debug=True)
