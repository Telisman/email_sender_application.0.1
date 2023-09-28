from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, static_folder='static')

# Define a dictionary to map operation names to processing functions
operations = {
    'Collect Emails': lambda df: df['email'].tolist() if 'email' in df.columns else None,
    'Collect Subjects': lambda df: df['subject'].tolist() if 'subject' in df.columns else None,
    'Collect Both Email and Subject': lambda df: df[['email', 'subject']].to_dict(orient='records') if 'email' in df.columns and 'subject' in df.columns else None
}

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

    operation = request.form.get('operation')

    if file:
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return f"Error reading the file: {str(e)}"

        if operation in operations:
            result = operations[operation](df)
            if result is not None:
                message = f"{operation} data collected"
                return jsonify({"message": message, "data": result})
            else:
                return f"{operation} data not found in the file."

    return "Invalid operation or an error occurred."

if __name__ == '__main__':
    app.run()
