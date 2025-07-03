import pandas as pd
import io
from flask import jsonify, send_file, request

def upload_csv_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        df = pd.read_csv(file)
        return jsonify({'columns': df.columns.tolist(), 'rows': len(df)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def upload_xlsx_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        df = pd.read_excel(file)
        return jsonify({'columns': df.columns.tolist(), 'rows': len(df)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def csv_summary_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    try:
        df = pd.read_csv(file)
        summary = df.describe(include='all').to_dict()
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def xlsx_summary_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    try:
        df = pd.read_excel(file)
        summary = df.describe(include='all').to_dict()
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def convert_csv_to_xlsx_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    try:
        df = pd.read_csv(file)
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='converted.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 400
