from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'excel_file' not in request.files:
        return "No file part"

    file = request.files['excel_file']

    if file.filename == '':
        return "No selected file"

    if file:
        df = pd.read_excel(file)
        print(df.head())

        return "File uploaded and processed successfully"

if __name__ == '__main__':
    app.run()
