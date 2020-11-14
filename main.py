from flask import jsonify, request 
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app()

@app.route ('/test/')
def test():
    return jsonify({
"message":  "des API travail très bien"
    })

@app.route('/', methods=['GET'])
def show_characters():
    all_Characters = list(db.db.bloodborne.find())
    for character in all_Characters:
       del character ["_id"]
    return jsonify({"all_Characters":all_Characters})
    


@app.route('/characters/<int:n_top>/', methods=['GET'])
def show_a_top_Characters(n_top):
    character = db.db.bloodborne.find_one({'n_top':n_top})
    del character ["_id"]

    return jsonify({
            "character":character
        })


@app.route('/api/new_character/', methods=['POST'])
def add_new_character():
    db.db.bloodborne.insert_one({
        "n_top": request.json["n_top"],
        "name":request.json["name"],
        "location":request.json["location"],
        "drops":request.json["drops"],
        "img":request.json["img"],
    })
    return jsonify({
        "message":"un nouvelle chef a été introduit de maniére satisfaisant",
        "status": 200,
    })


@app.route('/api/top_characters/update/<int:n_top>',methods=['PUT'])
def update_characters(n_top):

    if db.db.bloodborne.find_one({'n_top':n_top}):
        db.db.bloodborne.update_one({'n_top':n_top},
        {'$set':{   
        "n_top": request.json["n_top"],
        "name":request.json["name"],
        "location":request.json["location"],
        "drops":request.json["drop"],
        "img":request.json["img"],
        }})
    else:
        return jsonify({"status":400, "message": f"Character #{n_top} not found"})

    return jsonify({"status":200, "message": f"The character #{n_top} of the top was updated"})


@app.route('/api/top_characters/del/<int:n_top>',methods=['DELETE'])
def delete_characters(n_top):
    if db.db.bloodborne.find_one({'n_top':n_top}):
        db.db.bloodborne.delete_one({'n_top':n_top})
    else:
        return jsonify({"status":400, "message": f"character #{n_top} not found"})
    return jsonify({"status":200, "message": f"The character #{n_top} was deleted"})

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080) 