from flask import Flask, jsonify, request, send_file, send_from_directory
import pandas as pd
import io
import os

app = Flask(__name__)

# Example in-memory data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_id = max(item["id"] for item in items) + 1 if items else 1
    new_item = {"id": new_id, "name": data.get("name", "Unnamed")}
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    for item in items:
        if item["id"] == item_id:
            item["name"] = data.get("name", item["name"])
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"result": "Item deleted"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

from file_endpoints import upload_csv_file, upload_xlsx_file, csv_summary_file, xlsx_summary_file, convert_csv_to_xlsx_file

@app.route('/upload/csv', methods=['POST'])
def upload_csv():
    return upload_csv_file()

@app.route('/upload/xlsx', methods=['POST'])
def upload_xlsx():
    return upload_xlsx_file()

@app.route('/csv/summary', methods=['POST'])
def csv_summary():
    return csv_summary_file()

@app.route('/xlsx/summary', methods=['POST'])
def xlsx_summary():
    return xlsx_summary_file()

@app.route('/convert/csv-to-xlsx', methods=['POST'])
def convert_csv_to_xlsx():
    return convert_csv_to_xlsx_file()

@app.route('/interface')
def serve_interface():
    return send_from_directory('.', 'interface.html')

@app.route('/interface.html')
def serve_interface_html():
    return send_from_directory('.', 'interface.html')

@app.route('/generic/one', methods=['POST'])
def generic_one():
    from generic_function_one import generic_function_one
    return generic_function_one()

@app.route('/generic/two', methods=['POST'])
def generic_two():
    from generic_function_two import generic_function_two
    return generic_function_two()

@app.route('/function/one', methods=['POST'])
def function_one_endpoint():
    from function_one import function_one
    return function_one()

@app.route('/function/two', methods=['POST'])
def function_two_endpoint():
    from function_two import function_two
    return function_two()

@app.route('/function/three', methods=['POST'])
def function_three_endpoint():
    from function_three import function_three
    return function_three()

@app.route('/function/four', methods=['POST'])
def function_four_endpoint():
    from function_four import function_four
    return function_four()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
