from flask import Flask, request
from flask_restful import Api,Resource
import sqlite3
app = Flask(__name__)
api = Api(app)

def dbConnect():
    connection = sqlite3.connect('master.db')
    cursor = connection.cursor()
    return cursor,connection

class UserAPI(Resource):
    def get(self):
        cursor,connection = dbConnect()
        x=[]
        for row in cursor.execute("SELECT * from toDoList"):
            x.append(row)
        return {"output":x}
    def post(self):
        data = request.json
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
        return {"Message":"Update succesful"}
    def delete(self):
        return {"message":"delete succesful"}

api.add_resource(UserAPI,'/todo')

if __name__=='__main__':
    app.run(debug=True,port=6969)