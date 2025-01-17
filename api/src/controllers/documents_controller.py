import os
import logging
from flask import Blueprint, request, jsonify
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import pandas as pd

# Create the Blueprint for the documents controller
documents_bp = Blueprint('documents', __name__)

# Define the environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/service-account-file.json'  # Replace with your credentials

# Get the logger
logger = logging.getLogger(__name__)

# Create the uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def trim_text(text: str):
    """ Removes spaces and newline characters. """
    return text.strip().replace("\n", " ")

def online_process(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> documentai.Document:
    """
    A function to process a document online using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read document
    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)
    result = documentai_client.process_document(request=request)
    return result.document

@documents_bp.route('/analyze', methods=['POST'])
def analyze_document():
    """
    Accepts a document and processes it using Google Document AI to extract relevant fields.
    """
    try:
        logger.info("Received document for analysis.")

        # Ensure a file is uploaded
        if 'file' not in request.files:
            logger.error("No file part in the request.")
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file.")
            return jsonify({"error": "No selected file"}), 400
        
        # Save the file temporarily in the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        logger.info(f"File saved to {file_path}.")

        # Setup Document AI parameters (replace these with your actual parameters)
        project_id = 'your-project-id'
        location = 'us'  # You may need to adjust this
        processor_id = 'your-processor-id'
        mime_type = 'application/pdf'  # Assuming the uploaded file is a PDF

        document = online_process(project_id, location, processor_id, file_path, mime_type)
        logger.info("Document processed successfully.")

        # Extract relevant fields from the processed document
        names = []
        values = []
        
        for page in document.pages:
            for field in page.form_fields:
                names.append(trim_text(field.field_name.text_anchor.content))
                values.append(trim_text(field.field_value.text_anchor.content))

        # Define the keys you are interested in
        invoice_key = [
            "Account Number", "Billing Period", "Notice Number", "Amount Due from Previous Period", 
            "Amount Paid", "New Charges for Current Period", "Total Amount Due for Current Period", "Payment Due Date"
        ]
        
        # Filter the results based on the invoice keys
        extracted_data = {
            "Field Name": [],
            "Field Value": []
        }
        
        for name, value in zip(names, values):
            if name in invoice_key:
                extracted_data["Field Name"].append(name)
                extracted_data["Field Value"].append(value)

        logger.info("Extracted relevant fields from the document.")
        return jsonify(extracted_data), 200
    
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        return jsonify({"error": str(e)}), 500