from flask import Flask, request
from flask_restful import Api,Resource,reqparse
from flask_jwt import JWT, jwt_required, current_identity
import sqlite3
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'

class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('master.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('master.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    def __str__(self):
        return "User(id='%s')" % self.id


def identity(payload):
    # user_id = payload['identity']
    # return userid_table.get(user_id, None)
    cursor, connection = dbConnect()
    data = request.get_json()
    print(data)
def authenticate(username, password):
    user = User.find_by_username(username)
    print(user)
    if user and password == user.password:
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
jwt = JWT(app, authenticate, identity)


def dbConnect():
    connection = sqlite3.connect('master.db')
    cursor = connection.cursor()
    return cursor,connection

parser = reqparse.RequestParser()
parser.add_argument('date', help='The date parameter is not provided', required=True)
parser.add_argument('name', help='need the name', required=True)
class UserAPI(Resource):
    def get(self):
        cursor,connection = dbConnect()
        x=[]
        for row in cursor.execute("SELECT * from toDoList"):
            x.append(row)
        return {"output":x}

    @jwt_required()
    def post(self):

        data = parser.parse_args()
        date = data['date']
        name = data['name']
        cursor,connection = dbConnect()
        query = "INSERT INTO toDoList VALUES (?,?,?)"
        print(date,name)
        cursor.execute(query,(None,date,name))
        connection.commit()
        connection.close()
        return {'message':'succesful'} , 200

    def put(self):
        cursor, connection = dbConnect()
        data = request.get_json()
        old = data['old']
        new = data['new']
        query = f"UPDATE toDoList SET toDO=? WHERE toDo=?"
        print(old,new,query)
        cursor.execute(query, (new,old))
        connection.commit()
        connection.close()
        return {'message': f"delete {new}updated"}, 200
    def delete(self):
        cursor, connection = dbConnect()
        date = request.get_json()
        date = date['name']
        query = "DELETE FROM toDoList WHERE  toDo=?"
        cursor.execute(query,(date,))
        connection.commit()
        connection.close()
        return {'message':f"delete {date}successful"},200

api.add_resource(UserAPI,'/todo')


if __name__=='__main__':
    app.run(debug=True,port=6969)