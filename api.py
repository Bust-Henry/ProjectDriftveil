from flask import Flask, jsonify, request
from dbconnector import DBConnector
import os

app = Flask(__name__)
con:DBConnector = None

@app.route('/')
def home():
    return jsonify({"ProjectDriftveil": "api"})

@app.route('/nextPokemon')
def nextPokemon():
    re = con.getNextPokemon()
    if re == None:
        return jsonify({"response": "None"})
    return jsonify({"response": re})

@app.route('/nextShiny')
def nextShiny():
    re = con.getNextPokemon(True)
    if re == None:
        return jsonify({"response": "None"})
    return jsonify({"response": re})

@app.route("/pokemon/add/", methods=["POST"])
def addPokemon():
    json = request.get_json()
    if "number" in json:
        re = con.registerPokemon(json["number"])
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})

@app.route("/pokemon/addShiny", methods=["POST"])
def addShiny():
    json = request.get_json()
    if "number" in json:
        re = con.registerPokemon(json["number"], True)
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})


@app.route("/pokemon/remove", methods=["POST"])
def removePokemon():
    json = request.get_json()
    if "number" in json:
        re = con.deRegisterPokemon(json["number"])
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})

@app.route("/pokemon/removeShiny", methods=["POST"])
def removeShiny():
    json = request.get_json()
    if "number" in json:
        re = con.deRegisterPokemon(json["number"], True)
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})

@app.route("/pokemon/list/")
def listPokemon():
    pass

def run(dbpath):
    global con
    con = DBConnector(dbpath)
    app.run("0.0.0.0", 8080, True)
    
if __name__ == "__main__":
    run(os.path.join(os.path.dirname(__file__), "data", "db.sqlite"))

