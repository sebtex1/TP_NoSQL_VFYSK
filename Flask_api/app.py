from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request 
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://admin:admin@cluster0.p7bgj.mongodb.net/RepairCafe"

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=False)

@app.route('/')
def helloWorld():
    return render_template('pages/home.html')

@app.route('/read')
def readRepairs():
    request = mongo.db.coll1.find({}, {"_id": 0, "datasetid": 0, "recordid": 0, "geometry": 0, "record_timestamp": 0, "fields.ville0": 0})
    resp = dumps(request)
    jsonData = json.loads(resp)
    return render_template('pages/read.html', jsonData=jsonData, test=type(jsonData))

@app.route('/read_one')
def readRepairs_one():
    repairs = mongo.db.coll1.find_one()
    resp = dumps(repairs)
    return resp

@app.route('/read/<ville>')
def readRepairs_ville(ville):
    repairs = mongo.db.coll1.find({"fields.ville": ville})
    resp = dumps(repairs)
    return resp

@app.route('/read/aggregate')
def aggregate():
    repairs = mongo.db.coll1.aggregate([{"$addFields": {"results": {"$regexFind": {"input": "$fields.specialite", "regex": "Couture|Informatique" }}}}, varProject ])
    resp = dumps(repairs)
    return resp 

@app.route('/read/aggregate1')
def aggregate1():
    varMatch = {"$match": {"fields.specialite": {"$regex":"Informatique"}}}
    varSort = {"$sort": {"nom_repair_cafe": 1}}
    repairs = mongo.db.coll1.aggregate([varMatch, varProject, varSort ])
    resp = dumps(repairs)
    return resp