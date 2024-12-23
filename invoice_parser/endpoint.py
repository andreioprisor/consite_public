from flask import Flask, request, jsonify
import logging
from parser import Parser
from io import BytesIO

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/process', methods=['POST'])
def process_file():
    app.logger.info("Received request")
    if 'file' not in request.files:
        app.logger.error("No file part")
        return jsonify({"error": "No file received"}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the file stream into a BytesIO object
        file_stream = BytesIO(file.read())
        
        # Assuming your Parser expects a file-like object
        parser = Parser(file_stream)
        parser.parse()
        
        return parser.response, 200
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.logger.info("Starting Flask app on port 65432")
    app.run(debug=True, port=65432, host='0.0.0.0')
