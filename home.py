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
        # Assuming the file is in Excel format (xlsx)
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return f"Error reading the file: {str(e)}"

        file_columns = df.columns.tolist()

        required_columns = ['email', 'subject', 'first name', 'last name']

        missing_columns = [col for col in required_columns if col not in file_columns]

        if missing_columns:
            missing_msg = f"The following required columns are missing: {', '.join(missing_columns)}"
        else:
            missing_msg = "All required columns are present in the Excel file."

        present_columns_msg = f"Columns present in the file: {', '.join(file_columns)}"

        print(df.head())

        return f"{present_columns_msg}<br>{missing_msg}"

if __name__ == '__main__':
    app.run()
