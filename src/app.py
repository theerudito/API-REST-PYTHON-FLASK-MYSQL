# APP
from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
#from flask_cors import CORS


app = Flask(__name__)

conection = MySQL(app)


# ================================= SHOW ALL CHARACTERS ==================================
@app.route('/characters', methods=['GET'])
def list_persons():
    try:
        charater = conection.connection.cursor()
        sql = "SELECT * FROM `characters`"
        charater.execute(sql)
        data = charater.fetchall()
        persons = []
        for person in data:
            print(person)
            allcharacters = {
                "id": person[0], "name": person[1], "age": person[2], "clan": person[3]}
            persons.append(allcharacters)
        return jsonify(persons)
    except Exception as ex:
        return jsonify({"message": "List Error"})
# ================================== SHOW ALL CHARACTERS ==================================


# ================================== SHOW ONE CHARACTERS ==================================
@app.route('/characters/<int:id>', methods=['GET'])
def get_person(id):
    try:
        charater = conection.connection.cursor()
        sql = "SELECT * FROM `characters` WHERE id = '{0}'".format(id)
        charater.execute(sql)
        data = charater.fetchall()
        print(data)
        if data != None:
            person = {
                "id": data[0][0], "name": data[0][1], "age": data[0][2], "clan": data[0][3]}
            return jsonify(person)
    except Exception as ex:
        return jsonify({"message": "Person not found"})

# ================================== SHOW ONE CHARACTERS ==================================


# ==================================== CREATE CHARACTER ===================================
@app.route('/characters', methods=['POST'])
def create_person():
    try:
        data = request.get_json()
        charater = conection.connection.cursor()
        sql = """INSERT INTO `characters` (`name`, `age`, `clan`) 
        VALUES ('{0}', {1}, '{2}')""".format(request.json['name'], request.json['age'], request.json['clan'])
        charater.execute(sql)
        conection.connection.commit()
        return jsonify({"message": "Person created"})
    except Exception as ex:
        return jsonify({"message": "Error"})
# ==================================== CREATE CHARACTER ===================================


# ==================================== UPDATE CHARACTER ===================================
@app.route('/characters/<int:id>', methods=['PUT'])
def update_person(id):
    try:
        charater = conection.connection.cursor()
        print(request.json)
        sql = """UPDATE `characters` SET `name` = '{0}', `age` = '{1}', clan = '{2}' WHERE `id` = '{3}'""".format(
            request.json['name'], request.json['age'], request.json['clan'], id)
        charater.execute(sql)
        conection.connection.commit()
        return jsonify({"message": "Person updated"})
    except Exception as ex:
        return jsonify({"message": "Error"})
# ==================================== UPDATE CHARACTER ===================================


# ==================================== DELETE CHARACTER ===================================
@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_person(id):
    try:
        charater = conection.connection.cursor()
        sql = """DELETE FROM `characters` WHERE id = '{0}'""".format(id)
        charater.execute(sql)
        conection.connection.commit()
        return jsonify({"message": "Person deleted"})
    except Exception as ex:
        return jsonify({"message": "Error"})
# ==================================== DELETE CHARACTER ===================================

# PAGE NOT FOUND


def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1> ", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
