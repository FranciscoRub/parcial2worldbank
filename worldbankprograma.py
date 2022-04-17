from flask import Flask,request,render_template
from flask_restful import Api,Resource, reqparse
import ast
import requests

import decimal
import pandas as pd

app=Flask(__name__)
api=Api(app)


class WorldBank(Resource):
    def get(self):
        data= pd.read_csv('WorldbankD.csv',
                          error_bad_lines=False, engine='python')
        data=data.to_dict()
        return{'data':data},200
    pass

api.add_resource(WorldBank,'/worldbank')

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/datos')
def datos():
    data = requests.get("http://127.0.0.1:5000/worldbank").json()
    country = (data["data"]["Data Source"].get("2"))
    totalData = len(data["data"])
    i = 0
    lastPorcent = 0
    year = 0
    for db in data["data"]:
        i += 1
        current = db
        if(totalData - 1 == i):
            lastPorcent = data["data"][current]["2"]
            year = current
    return render_template("datos.html", pais=country, data=lastPorcent, year=year)
@app.route('/prome')
def prome():
    data = requests.get("http://127.0.0.1:5000/worldbank").json()
    totalData = len(data["data"])
    i = 0
    totalPorcent = 0
    for db in data["data"]:
        i += 1
        current = db
        if(i > 4):
            totalPorcent += data["data"][current]["2"]
    porcent = decimal.Decimal(totalPorcent / (totalData - 4))
    print(int(totalData))

    return render_template("prome.html", porcent=round(porcent, 2))

if __name__=='__main__':
    app.run()

