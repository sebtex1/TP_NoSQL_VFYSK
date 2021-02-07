from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request 
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

@app.route('/readOne')
def readRepairs_one():
    request = mongo.db.coll1.find_one({}, {"_id": 0, "datasetid": 0, "recordid": 0, "geometry": 0, "record_timestamp": 0, "fields.ville0": 0})
    resp = dumps(request)
    return resp

@app.route('/read/aggregate')
def aggregate():
    match = ""
    ville = request.args.get('ville')
    inscription = request.args.get('inscription')

    if ville != "":
        match = {"fields.ville": {"$regex": ville }}

    if inscription != "":
        match = {"fields.inscription": {"$regex": inscription.capitalize() }}

    varMatch = {"$match": match }
    varProject = {"$project": {"_id": 0, "datasetid": 0, "recordid": 0, "geometry": 0, "record_timestamp": 0, "fields.ville0": 0}}
    varSort = {"$sort": {"nom_repair_cafe": 1}}
    aggre = mongo.db.coll1.aggregate([varMatch, varProject, varSort])
    resp = dumps(aggre)
    return render_template('pages/read.html', result=resp)

