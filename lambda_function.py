"""
AWS Lambda function
"""

import base64
import json
import logging
from detection import ml_detection, ml_utils


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Find ML model type based on string request
def get_model_type(query_string):
    """Find ML model type based on string request"""
    # Default ml model type
    if query_string == "":
        model_type = "facebook/detr-resnet-50"
    # Assess query string value
    elif "detr" in query_string:
        model_type = "facebook/" + query_string
    elif "yolos" in query_string:
        model_type = "hustvl/" + query_string
    else:
        raise Exception("Incorrect model type.")
    return model_type


# Run detection pipeline: load ML model, perform object detection and return json object
def detection_pipeline(model_type, image_bytes):
    """detection pipeline: load ML model, perform object detection and return json object"""
    # Load correct ML model
    processor, model = ml_detection.load_model(model_type)

    # Perform object detection
    results = ml_detection.object_detection(processor, model, image_bytes)

    # Convert dictionary of tensors to JSON object
    result_json_dict = ml_utils.convert_tensor_dict_to_json(results)

    return result_json_dict


def lambda_handler(event, context):
    """
        Lambda handler (proxy integration option unchecked on AWS API Gateway)

        Args:
            event (dict): The event that triggered the Lambda function.
            context (LambdaContext): Information about the execution environment.

        Returns:
            dict: The response to be returned from the Lambda function.
        """

    # logger.info(f"API event: {event}")
    try:
        # Retrieve model type
        model_query = event.get("model", "")
        model_type = get_model_type(model_query)
        logger.info("Model query: %s", model_query)
        logger.info("Model type: %s", model_type)

        # Decode the base64-encoded image data from the event
        image_data = event["body"]
        if event["isBase64Encoded"]:
            image_data = base64.b64decode(image_data)

        # Run detection pipeline
        result_dict = detection_pipeline(model_type, image_data)
        logger.info("API Results: %s", str(result_dict))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result_dict),
        }
    except Exception as e:
        logger.info("API Error: %s", str(e))
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
