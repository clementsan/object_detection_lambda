import os
import sys
import pytest
import json
import base64


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(parent_dir))

from lambda_function import lambda_handler


@pytest.fixture
def event():
    # Get the directory of the current test file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the image path relative to the test directory
    image_path = os.path.join(test_dir, 'data', 'savanna.jpg')

    # Read image data
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Encode the image data in base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    # Prepare the payload
    json_event = {
        'body': encoded_image
    }

    return json_event


@pytest.fixture
def context():
    return None


def test_lambda_handler(event, context):
    lambda_response = lambda_handler(event, context)
    response_data = json.loads(lambda_response["body"])

    print("lambda_response - type",type(lambda_response))
    print("lambda_response", lambda_response)
    print("response_data - type", type(response_data))
    print("response_data", response_data)

    response_keys = list(response_data.keys())
    gt_keys = ['scores', 'labels', 'boxes']

    assert lambda_response["statusCode"] == 200
    assert set(response_keys) == set(gt_keys), "Response keys do not match ground truth"
    assert len(response_data['scores']) == 5
    assert len(response_data['labels']) == 5