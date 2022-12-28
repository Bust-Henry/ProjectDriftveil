from flask import Flask, jsonify, request, abort, render_template, send_file
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

@app.route("/pokemon/update/")
def updatePokemon():
    try:
        controller = BlueStackController()
        controller.closeAll()
        if controller.reloadSaveData():
            result = controller.sendSaveData()
        return jsonify({"result": result})
    except:
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
    

def run(dbpath):
    print(dbpath)
    global con
    con = DBConnector(dbpath)
    app.run("0.0.0.0", 8080, True)
    
if __name__ == "__main__":
    run(os.path.join(os.path.dirname(__file__), os.environ.get("dbpath")))

