import gradio as gr
import base64
import os
import requests
import json
import utils

from dotenv import load_dotenv, find_dotenv


# List of ML models
list_models = ["facebook/detr-resnet-50", "facebook/detr-resnet-101", "hustvl/yolos-tiny", "hustvl/yolos-small"]
list_models_simple = [os.path.basename(model) for model in list_models]


# Retrieve API URLs from env file or global settings
def retrieve_api():

    env_path = find_dotenv('config_api.env')
    if env_path:
        load_dotenv(dotenv_path=env_path)
        print("config_api.env file loaded successfully.")
    else:
        print("config_api.env file not found.")

    # Use of AWS endpoint or local container by default
    global AWS_API
    AWS_API = os.getenv("AWS_API", default="http://localhost:8080")


#@spaces.GPU
def detect(image_path, model_id, threshold):
    print("\n Gradio - Object detection...")
    print("\t ML model:", list_models[model_id])

    with open(image_path, 'rb') as image_file:
       image_bytes = image_file.read()

    # API Call for object prediction with model type as query parameter
    if AWS_API == "http://localhost:8080":
        API_endpoint = AWS_API + "/2015-03-31/functions/function/invocations"
    else:
        API_endpoint = AWS_API + "/dev/detect"
    print("\t API_Endpoint: ", API_endpoint)

    # Encode the image data in base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    # Requests arguments
    payload = {
        'body': encoded_image,
        'isBase64Encoded': True,
    }
    headers = {"Content-Type": "application/json"}

    # Prepare the query string parameters
    model_name = list_models_simple[model_id]
    params = {
        'model': model_name
    }

    # response = requests.post(API_endpoint, json=payload, headers=headers)
    response = requests.post(API_endpoint, json=payload, headers=headers, params=params)

    if response.status_code == 200:
        # Process the response
        response_json = response.json()
        print('\t API response', response_json)
        print('\t API response - type', type(response_json))
        prediction_dict = json.loads(response_json["body"])
        print('\t API body prediction_dict', prediction_dict)
        print('\t API body prediction_dict - type', type(prediction_dict))
    else:
        prediction_dict = {"Error": response.status_code}
        gr.Error(f"\t API Error: {response.status_code}")

    # Generate gradio output components: image and json
    output_json, output_pil_img = utils.generate_gradio_outputs(image_path, prediction_dict, threshold)

    return output_json, output_pil_img


def demo():
    with gr.Blocks(theme="base") as demo:
        gr.Markdown("# Object detection task - use of AWS Lambda")
        gr.Markdown(
            """
            This web application uses transformer models to detect objects on images.
            Machine learning models were trained on the COCO dataset.
            You can load an image and see the predictions for the objects detected.
            
            Note: This web application uses deployed ML models, available via AWS Lambda and AWS API Gateway.
            """
        )

        with gr.Row():
            with gr.Column():
                model_id = gr.Radio(list_models, \
                               label="Detection models", value=list_models[0], type="index", info="Choose your detection model")
            with gr.Column():
                threshold = gr.Slider(0, 1.0, value=0.9, label='Detection threshold', info="Choose your detection threshold")

        with gr.Row():
            input_image = gr.Image(label="Input image", type="filepath")
            output_image = gr.Image(label="Output image", type="pil")
            output_json = gr.JSON(label="JSON output", min_height=240, max_height=300)

        with gr.Row():
            submit_btn = gr.Button("Submit")
            clear_button = gr.ClearButton()

        gr.Examples(['samples/savanna.jpg', 'samples/boats.jpg'], inputs=input_image)

        submit_btn.click(fn=detect, inputs=[input_image, model_id, threshold], outputs=[output_json, output_image])
        clear_button.click(lambda: [None, None, None], \
                        inputs=None, \
                        outputs=[input_image, output_image, output_json], \
                        queue=False)

    demo.queue().launch(debug=True)

if __name__ == "__main__":
    retrieve_api()
    demo()