"""
Object detection - command line inference via API
"""

import sys
import base64
import argparse
import requests

# Default examples
# api = "http://localhost:8080/2015-03-31/functions/function/invocations"
# file = "./tests/data/boats.jpg"


def arg_parser():
    """Parse arguments"""

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Object detection inference via API call"
    )
    # Add arguments
    parser.add_argument(
        "--api", type=str, help="URL to server API (with endpoint)", required=True
    )
    parser.add_argument(
        "--file", type=str, help="Path to the input image file", required=True
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["detr-resnet-50", "detr-resnet-101", "yolos-tiny", "yolos-small"],
        help="Model type",
        required=False,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase output verbosity"
    )
    return parser


def main(args=None):
    """Main function"""

    args = arg_parser().parse_args(args)
    # Use the arguments
    if args.verbose:
        print(f"Input file: {args.file}")

    # Retrieve model type
    if args.model:
        model_name = args.model
    else:
        model_name = ""

    # Load image
    with open(args.file, "rb") as image_file:
        image_data = image_file.read()

    # Encode the image data in base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    # Prepare the payload
    payload = {
        "body": encoded_image,
        "isBase64Encoded": True,
        "model": model_name,
    }

    # Send request to API
    # Option 'files': A dictionary of files to send to the specified url
    # response = requests.post(args.api, files={'image': image_data})
    # Option 'json': A JSON object to send to the specified url
    response = requests.post(args.api, json=payload, timeout=60)

    if response.status_code == 200:
        print("Detection Results:")
        # Process the response
        # processed_data = json.loads(response.content)
        # print('processed_data', processed_data)
        results = response.json()
        print("results: ", results)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
