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

@app.route('/read/aggregate')
def aggregate():

    matchList = {}
    varMatch = {}

    if request.args.get('ville'):
        ville = request.args.get('ville')
        matchList['fields.ville']= {'$regex':ville.capitalize()}

    if request.args.get('inscription'):
        inscription = request.args.get('inscription')
        matchList['fields.inscription']={'$regex':inscription.capitalize()}

    if request.args.get('adresse'):
        adresse = request.args.get('adresse')
        matchList['fields.adresse']={'$regex':adresse}
        
    if request.args.get('specialite'):
        specialite = request.args.get('specialite')
        matchList['fields.specialite']= {'$regex':specialite}

    if request.args.get('cp'):
        cp = request.args.get('cp')
        matchList['fields.cp']={'$regex':cp}
    
    if request.args.get('periodicite'):
        periodicite = request.args.get('periodicite')
        matchList['fields.periodicite']={'$regex':periodicite}

    if request.args.get('horaire'):
        horaire = request.args.get('horaire')
        matchList['fields.horaire']={'$regex':horaire}

    if request.args.get('nom'):
        nom = request.args.get('nom')
        matchList['fields.nom_repair_cafe']={'$regex':nom}

        
    varMatch['$match']=matchList
    varProject = {"$project": {"_id": 0, "datasetid": 0, "recordid": 0, "geometry": 0, "record_timestamp": 0, "fields.ville0": 0}}
    varSort = {"$sort": {"nom_repair_cafe": 1}}

    repairs = mongo.db.coll1.aggregate([varMatch, varProject, varSort])
    resp = dumps(repairs)
    return resp