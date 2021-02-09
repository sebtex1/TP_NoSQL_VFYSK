from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import request 
import json

#création de l'objet de classe Flask   
app = Flask(__name__)

#connexion à la base de données à distance à l’aide de l'URL
app.config['MONGO_URI'] = "mongodb+srv://admin:admin@cluster0.p7bgj.mongodb.net/RepairCafe"

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=False)

@app.route('/')
@app.route('/query')
def aggregate():

    matchList = {}
    varMatch = {}
    #Creer une requête qui fait partie de notre qry qui envoyait les données au serveur sous forme non chiffrée
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
        matchList['fields.specialite']= {'$regex':specialite.capitalize()}

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

    #on a défini l'agrégation pour facilité nous recherche sur notre base de données    
    varMatch['$match']=matchList
    varProject = {"$project": {"_id": 0, "datasetid": 0, "recordid": 0, "geometry": 0, "record_timestamp": 0, "fields.ville0": 0}}
    varSort = {"$sort": {"nom_repair_cafe": 1}}

    repairs = mongo.db.coll1.aggregate([varMatch, varProject, varSort])
    resp = dumps(repairs)
    jsonData = json.loads(resp)
    #renvoyer le résultat dans la page html
    return render_template('pages/home.html', jsonData=jsonData)

@app.route('/search', methods=['GET', 'POST'])
def readRepairs():
    varGroup = {"$group":{"_id":"$fields.ville"}}
    varSort = {"$sort": {"_id": 1}}
    repairs = mongo.db.coll1.aggregate([varGroup, varSort])
    resp = dumps(repairs)
    if request.method == 'GET':
        jsonVille = json.loads(resp)
        return render_template('pages/recherche.html', dataVille=jsonVille)
    
    
    #Reuperé les données du formulaire en fonction de son id 
    if "submit" in request.form:
        qry =""

        if request.form['nom']:
            nom = request.form['nom']
            qry = f"{qry}nom={nom}&"

        if request.form['ville']:
            ville = request.form['ville']
            qry = f"{qry}ville={ville}&"
        
        if request.form['adresse']:
            adresse = request.form['adresse']
            qry = f"{qry}adresse={adresse}&"
        
        if request.form['cp']:
            cp = request.form['cp']
            qry = f"{qry}cp={cp}&"
        
        if request.form['spec']:
            spec = request.form['spec']
            qry = f"{qry}specialite={spec}&"
        
        if request.form['inscrip']:
            inscrip = request.form['inscrip']
            qry = f"{qry}inscription={inscrip}&"


        return redirect('/query?' + qry)

@app.route('/detail')
def details():

    matchList = {}
    varMatch = {}
    
    #Verifie si le term  existe dans l'url
    if request.args.get('adresse'):
        adresse = request.args.get('adresse')
        matchList['fields.adresse']={'$regex':adresse}

        
    varMatch['$match']=matchList
    varProject = {"$project": {"_id": 0, "datasetid": 0, "recordid": 0, "geometry": 0, "record_timestamp": 0, "fields.ville0": 0}}
    varSort = {"$sort": {"nom_repair_cafe": 1}}

    repairs = mongo.db.coll1.aggregate([varMatch, varProject, varSort])
    resp = dumps(repairs)
    jsonData = json.loads(resp)
    return render_template('pages/detail.html', jsonData=jsonData)
