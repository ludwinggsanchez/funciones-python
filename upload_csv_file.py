import pandas as pd
from flask import jsonify, request

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
