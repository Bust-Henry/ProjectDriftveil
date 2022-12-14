from flask import Flask, jsonify, request, abort, render_template, url_for
from dbconnector import DBConnector
from blueStackController import BlueStackController
import os
from PIL import Image
from base64 import b64encode
import io
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
con:DBConnector = None

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/')
@app.route('/help')
def home():
    """this route returns all other routes and their aliases

    Returns:
        dict: a dict with all routes and their aliases
    """
    import json
    path = os.path.join(os.path.dirname(__file__), os.environ.get("descriptions"))
    desriptions:dict = json.load(open(path, "r"))
    links = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            print(url)
            if url in desriptions.keys():
                links[url] = desriptions[url]
            else:
                links[url] = rule.alias
    return jsonify(links)

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

@app.route("/add", methods=["POST"])
def addPokemon():
    json = request.get_json()
    if "number" in json:
        re = con.registerPokemon(json["number"])
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})

@app.route("/addShiny", methods=["POST"])
def addShiny():
    json = request.get_json()
    if "number" in json:
        re = con.registerPokemon(json["number"], True)
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})


@app.route("/remove", methods=["POST"])
def removePokemon():
    json = request.get_json()
    if "number" in json:
        re = con.deRegisterPokemon(json["number"])
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})

@app.route("/removeShiny", methods=["POST"])
def removeShiny():
    json = request.get_json()
    if "number" in json:
        re = con.deRegisterPokemon(json["number"], True)
        if re:
            return jsonify({"response": "Success"})
        return jsonify({"response": "Failure"})
    return jsonify({"request": "invalid"})

@app.route("/list")
def listPokemon():
    result = con.getAllOwned()
    return jsonify(result)

@app.route("/listShiny")
def listShinyPokemon():
    result = con.getAllOwned(True)
    return jsonify(result)

@app.route("/listMissing")
def listMissingPokemon():
    result = con.getAllMissing()
    return jsonify(result)

@app.route("/listMissingShiny")
def listMissingShinyPokemon():
    result = con.getAllMissing(True)
    return jsonify(result)

@app.route("/update")
def updatePokemon():
    try:
        controller = BlueStackController()
        controller.closeAll()
        if controller.reloadSaveData():
            result = controller.sendSaveData()
        return jsonify({"result": result})
    except Exception as e:
        print(e)
        abort(503)

@app.route("/status")
def status():
    try:
        controller = BlueStackController()
        img:Image = controller.screenshotPIL()
        data = io.BytesIO()
        img.save(data, "PNG")
        encode_img_data = b64encode(data.getvalue())
        return render_template("index.html", img_data="data:image/png;base64,"+encode_img_data.decode("UTF-8"))
    except Exception as e:
        print(e)
        abort(503)

@app.route("/claimPokemon", methods=["POST"])
def claimPokemon():
    try:
        data:dict = request.get_json()
        if "user" not in data.keys():
            return jsonify({"request": "missing key user!"})
        if "pokemon" not in data.keys():
            return jsonify({"request": "missing key pokemon!"})
        user = data["user"]
        pokemon:list = data["pokemon"]
        result = con.claimPokemon(pokemon, user)
        return jsonify(result)
    except Exception as e:
        print(e)
        abort(503)

@app.route("/unClaimPokemon", methods=["POST"])
def unClaimPokemon():
    try:
        data:list = request.get_json()
        result = con.unClaimPokemon(data)
        return jsonify(result)
    except Exception as e:
        print(e)
        abort(503)

def run(dbpath):
    print(dbpath)
    global con
    con = DBConnector(dbpath)
    app.run("0.0.0.0", 8080, True)
    
if __name__ == "__main__":
    run(os.path.join(os.path.dirname(__file__), os.environ.get("dbpath")))