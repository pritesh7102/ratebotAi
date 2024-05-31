from flask import Flask, jsonify, request
import psycopg2
import pandas as pd
import json
from flask_cors import CORS
import traceback


employees = [
    {
        "id": 1,
        "name": "John Doe",
        "dob": "1990-01-01",
        "salary": 50000,
        "age": 34,
        "gender": "Male",
        "department_id": 101
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "dob": "1985-05-15",
        "salary": 60000,
        "age": 39,
        "gender": "Female",
        "department_id": 102
    },
    {
        "id": 3,
        "name": "Sam Johnson",
        "dob": "1992-08-22",
        "salary": 55000,
        "age": 31,
        "gender": "Male",
        "department_id": 103
    }
]


app = Flask(__name__)

CORS(app)

conn = psycopg2.connect(
    database="interns",
    user="pritesh",
    password="pritesh",
    host="192.168.0.148",
    port="5432"
)

cur = conn.cursor()

@app.route('/addEmployee', methods=['POST'])
def addEmployee():
    data = request.json

    id = data['id']
    name = data['name']
    dob = data['dob']
    salary = data['salary']
    gender = data['gender']
    age = data['age']
    department_id = data['department_id']

    query = "INSERT INTO employee VALUES (%s, '%s', '%s', %s, '%s', %s, %s)" %(id, name, dob, salary, gender, age, department_id)
    try:
        cur.execute(query)
        conn.commit()
        return jsonify({
            'status_message': 'success',
            'message': 'Employee added successfully'})
    except:
        return jsonify({
            'status_message': 'error',
            'message': traceback.format_exc()})

@app.route('/getAllEmployees', methods=['GET'])
def getAllEmployees():
    query = "SELECT * FROM employee"
    df = pd.read_sql_query(query, conn)
    jf = df.to_json(orient='records')
    print(jf)
    result = json.loads(jf)
    print(result)
    return {"data":result}

@app.route('/getEmployee', methods=['GET'])
def getEmployee():
    id = request.json
    data = id['id']
    query = "SELECT * FROM employee WHERE employee_id = %s" %(data)
    df = pd.read_sql_query(query, conn)
    print(df)
    jf = df.to_json(orient='records')
    # cur.execute(query)
    # result = cur.fetchall()
    result = json.loads(jf)
    return result

@app.route('/addDepartment', methods=['GET'])
def addDepartment():
    data = request.json

    dept_id = data['id']
    dept_name = data['name']
    manager = data['manager']

    query = "INSERT INTO department VALUES (%s, '%s', '%s')" %(dept_id, dept_name, manager)
    cur.execute(query)
    conn.commit()
    return jsonify({'message': 'Department added successfully'})

@app.route('/getDepartment', methods=['GET'])
def getDepartment():
    id = request.json
    data = id['id']
    query = "SELECT * FROM department WHERE dept_id = %s" %(data)
    df = pd.read_sql_query(query, conn)
    jf = df.to_json(orient='records')
    result = json.loads(jf)
    return result

@app.route('/updateEmployee', methods=['GET'])
def updateEmployee():
    data = request.json

    id = data['employee_id']
    name = data['employee_name']
    dob = data['dob']
    salary = data['salary']
    gender = data['gender']
    age = data['age']
    department_id = data['dept_id']

    query = "UPDATE employee SET employee_id = %s, employee_name = '%s', dob = '%s', salary = %s, gender = '%s', age = %s, dept_id = %s WHERE employee_id = %s" %(id, name, dob, salary, gender, age, department_id, id)
    cur.execute(query)
    conn.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/deleteEmployee', methods=['GET'])
def deleteEmployee():
    data = request.json
    id = data['id']
    query = "DELETE FROM employee WHERE employee_id = %s" %(id)
    cur.execute(query)
    conn.commit()
    return jsonify({'message': 'Employee deleted successfully'})
    

if __name__ == '__main__':
    app.run(debug=True)