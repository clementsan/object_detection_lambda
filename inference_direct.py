from detection import ml_detection, ml_utils
import json
from PIL import Image


# Run detection pipeline: load ML model, perform object detection and return json object
def detection_pipeline(model_type, image_bytes):
    # Load correct ML model
    detr_processor, detr_model = ml_detection.load_model(model_type)

    # Perform object detection
    results = ml_detection.object_detection(detr_processor, detr_model, image_bytes)

    # Convert dictionary of tensors to JSON object
    result_json_dict = ml_utils.convert_tensor_dict_to_json(results)

    return result_json_dict


def main():
    print('Main function')

    model_type = "facebook/detr-resnet-50"
    image_path = './samples/boats.jpg'

    # Reading image file as image_bytes (similar to API request)
    print('Reading image file...')
    with open(image_path, 'rb') as image_file:
       image_bytes = image_file.read()

    result_json = detection_pipeline(model_type, image_bytes)
    print("result_json:", result_json)


if __name__ == "__main__":
    main()

