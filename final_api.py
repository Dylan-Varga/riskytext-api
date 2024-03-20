from flask import Flask, request, jsonify
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)

# Azure Text Analytics Configuration
endpoint = "https://469-east-language.cognitiveservices.azure.com/"
azure_key = '6e79df009daf4408a273f240d36c4403'
project_name = "cornellmovies"
deployment_name = "deployment-1"

text_analytics_client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(azure_key),
)

# API Key Configuration
api_key = 'testkey123'

# Request and Error Logging
def log_request(message, source):
    print(f"Request: {message}, Source: {source}")

def log_error(error_code, source):
    print(f"Error: {error_code}, Source: {source}")

@app.route('/classify', methods=['POST'])
def classify_text():
    try:
        # Check for API key
        provided_key = request.headers.get('X-API-Key')
        if provided_key != api_key:
            return jsonify({'error': 'Invalid API key'}), 401

        content = request.json
        input_message = content.get('message')
        is_file = content.get('is_file', False)  # Default to False if not provided

        if is_file:
            # If message is a filename, read from the file
            with open(input_message) as file:
                text_to_classify = file.read()
        else:
            # If message is the text itself
            text_to_classify = input_message

        # Perform classification
        document = [text_to_classify]
        poller = text_analytics_client.begin_multi_label_classify(
            document,
            project_name=project_name,
            deployment_name=deployment_name
        )

        document_results = poller.result()

        results = []
        for doc, classification_result in zip(document, document_results):
            if classification_result.kind == "CustomDocumentClassification":
                classifications = classification_result.classifications
                classified_risks = []
                for classification in classifications:
                    classified_risks.append({
                        'category': classification.category,
                        'confidence_score': classification.confidence_score
                    })
                results.append({'message': doc, 'risks': classified_risks})
            elif classification_result.is_error is True:
                error_code = classification_result.error.code
                log_error(error_code, source='Azure Text Analytics')
                results.append({'message': doc, 'error': {
                    'code': error_code,
                    'message': classification_result.error.message
                }})

        # Log the request
        log_request(message=input_message, source='Client')

        return jsonify(results)
    
    except Exception as e:
        log_error(error_code=str(e), source='Server')
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='10.249.239.176')
