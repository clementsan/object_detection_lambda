---
title: Object Detection Lambda
emoji: 🌖
colorFrom: purple
colorTo: green
sdk: gradio
sdk_version: 5.5.0
app_file: app.py
pinned: false
short_description: Object detection Lambda
---

# Object detection via AWS Lambda

<b>Aim: AI-driven object detection task</b>
 - Front-end: user interface via Gradio library
 - Back-end: use of AWS Lambda function to run ML models

## Local development

### User interface
Use of Gradio library for web interface

Command line:
> python3 app.py

<b>Note:</b> The Gradio app should now be accessible at http://localhost:7860


### Building the docker image:

bash
> docker build -t object-detection-lambda .

### Running the docker container locally:

bash

> docker run --name object-detection-lambda-cont -p 8080:8080 object-detection-lambda


### Testing locally:

Example of a prediction request

python
> python3 inference_api.py --api http://localhost:8080/2015-03-31/functions/function/invocations --file ./tests/data/boats.jpg
