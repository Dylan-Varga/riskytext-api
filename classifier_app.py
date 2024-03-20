# -------------------------------------------------------------------------
# Multilabel Classification for Text Risk Levels
# Credit to https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/samples/sample_multi_label_classify.py
# for sample code
# --------------------------------------------------------------------------

def sample_classify_document_multi_label(input) -> None:
    # [START multi_label_classify]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = "https://469-east-language.cognitiveservices.azure.com/"
    key = '6e79df009daf4408a273f240d36c4403'
    project_name = "cornellmovies"
    deployment_name = "deployment-1"
    path_to_sample_document = input

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(path_to_sample_document) as fd:
        document = [fd.read()]

    poller = text_analytics_client.begin_multi_label_classify(
        document,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = poller.result()
    for doc, classification_result in zip(document, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classifications = classification_result.classifications
            print(f"\nMessage with context '{doc}' was classified at the following risk levels:\n")
            for classification in classifications:
                print("'{}' with confidence score {}.".format(
                    classification.category, classification.confidence_score
                ))
        elif classification_result.is_error is True:
            print("File '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message
            ))
    # [END multi_label_classify]


def writeInputToFile(input_message):
    try:
        with open("tempFile.txt", "w") as f:
            f.write(input_message)
        return "tempFile.txt"
    except Exception as e:
        print("Error writing input to file:", e)
        return None

if __name__ == "__main__":
    filenameInput = input("Enter filepath with potential message, '1' to enter it directly, or '-1' to exit.\n")
    while(filenameInput != "-1"):
        if(filenameInput == '1'):
            inputMessage = input("Enter your message:\n")
            filenameInput = writeInputToFile(inputMessage)
            if filenameInput is None:
                print("Exiting due to error writing to file.")
                break 
        sample_classify_document_multi_label(filenameInput)
        filenameInput = input("-----------------------------------------------------\nEnter filepath with potential message, '1' to enter it directly, or '-1' to exit.\n")