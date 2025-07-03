import pandas as pd
import io
from flask import jsonify, send_file, request

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
