from flask import Flask, jsonify, request
import requests, json
from datetime import date
from db_connection import DBConnect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all():
    session = DBConnect()
    query = "SELECT * FROM Widgets ORDER BY Name;"
    session.exe(query, {})
    results = session.get_results()
    session.close()

    response = {'response': {'results': results}, 'Success': 'OK', 'message': 'Get all Record'}
    return jsonify(response), 200


@app.route('/<int:widget_id>', methods=['GET'])
def get(widget_id):
    session = DBConnect()
    params = (str(widget_id))
    query = "SELECT * FROM Widgets WHERE ID = ?;"
    session.exe(query, params)
    results = session.get_results()

    # Validation
    if len(results) == 0:
        return jsonify({'message': f'No record exists for {widget_id}'.format(widget_id) }), 404

    session.close()

    response = {'response': {'results': results}, 'Success': 'OK', 'message': 'Get Record'}
    return jsonify(response), 200


@app.route('/', methods=['POST'])
def create():
    data = json.loads(request.get_data())

    session = DBConnect()
    params = (data['name'], int(data['number_of_parts']))
    query = "INSERT INTO Widgets (Name, NumberOfParts, CreatedDate) VALUES (?, ?, DateTime('now'))"
    session.exe(query, params)

    widget_id = session.last_row_id()

    session.commit()
    session.close()

    response = {'response': {'id': widget_id}, 'Success': 'OK', 'message': 'Inserted New Record'}
    return jsonify(response), 201


@app.route('/<int:widget_id>', methods=['PUT'])
def update(widget_id):
    data = json.loads(request.get_data())

    session = DBConnect()
    params = (data['name'], int(data['number_of_parts']), widget_id)
    query = "UPDATE Widgets SET Name = ?, NumberOfParts = ? WHERE ID = ?"
    session.exe(query, params)

    session.commit()
    session.close()

    response = {'response': {'id': widget_id}, 'Success': 'OK', 'message': 'Updated Record'}
    return response, 200


@app.route('/<int:widget_id>', methods=['DELETE'])
def delete(widget_id):
    session = DBConnect()
    params = (str(widget_id))
    query = "DELETE FROM Widgets WHERE ID = ?;"
    session.exe(query, params)

    session.commit()
    session.close()

    response = {'response': {'id': widget_id}, 'Success': 'OK', 'message': 'Deleted Record'}
    return response, 200


if __name__ == '__main__':
    app.run(debug=True)
