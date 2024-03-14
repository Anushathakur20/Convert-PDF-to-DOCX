
from flask import Flask, request, render_template, send_file,redirect,url_for,Response,send_from_directory
from pdf2docx import Converter
import os
# import pdfplumber
# import pandas as pd
# import openpyxl
# from openpyxl.utils.exceptions import IllegalCharacterError
# from docx2pdf import convert
from werkzeug.utils import secure_filename
# from docx import Document
# from io import BytesIO
UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def Layout():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('layout.html',files=files)

@app.route('/upload')
def uploadpdf():
    return render_template('upload.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert_to_docx():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return "No file uploaded"

        # Get the uploaded file
        pdf_file = request.files['file']

        # Check if the file is empty
        if pdf_file.filename == '':
            return "No selected file"

        # Save the uploaded file to a temporary location
        try:
        # Save the uploaded file to a temporary location
            pdf_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pdf_file.filename))
            pdf_file.save(pdf_filename)
        except Exception as e:
            print("Error uploading file:", e)  # Add this line for error handling
            return "Error uploading file"

        # Extract filename without extension
        filename = os.path.splitext(pdf_file.filename)[0]
        # Define output DOCX filename
        docx_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.docx")
        

        # Define output DOCX filename
        # docx_file = f"{filename}.docx"

        # Create a Converter object
        cv = Converter(pdf_filename)

        # Convert PDF to DOCX
        cv.convert(docx_filename, start=0, end=None)

        # Close the Converter object
        cv.close()

        # Remove the temporary PDF file
        os.remove(pdf_filename)
        
        # Return the converted DOCX file as a downloadable attachment
        return send_file(docx_filename, as_attachment=True)
    else:
        # Handle GET request, render the upload form
        return render_template('upload.html')
      
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view/<path:filename>')
def view_file(filename):
    # Construct the full path to the file
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Determine the file extension
    file_extension = filename.split('.')[-1]

    # Set appropriate MIME type based on file extension
    mime_type = None
    if file_extension == 'docx':
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif file_extension == 'pdf':
        mime_type = 'application/pdf'
    # Add more elif conditions for other file types if needed

    # If MIME type is found, send the file
    if mime_type:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype=mime_type)
    else:
        return "Unsupported file type", 400
    
if __name__ == '__main__':
    app.run(debug=True)
