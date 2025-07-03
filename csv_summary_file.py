import pandas as pd
from flask import jsonify, request

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
