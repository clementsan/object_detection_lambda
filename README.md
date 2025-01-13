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

[![](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)


<b>Aim: AI-driven object detection task</b>

Architecture:
 - Front-end: user interface via Gradio library
 - Back-end: use of AWS Lambda function to run deployed ML model

You can try out our deployed [Hugging Face Space](https://huggingface.co/spaces/cvachet/object_detection_lambda
)!

<b>Table of contents: </b>
 - [Local development](#1-local-development)
 - [AWS deployment](#2-deployment-to-aws)
 - [Hugging Face deployment](#3-deployment-to-hugging-face)


## 1. Local development

### 1.1. Build and run the Docker container

<details>

Step 1 - Building the docker image

bash
> docker build -t object-detection-lambda .

Step 2 - Running the docker container locally

bash

> docker run --name object-detection-lambda-cont -p 8080:8080 object-detection-lambda

</details>

### 1.2. Execution via user interface
Use of Gradio library for web interface

<b>Note:</b> The environment variable ```AWS_API``` should point to the local container
> export AWS_API=http://localhost:8080

Command line for execution:
> python3 app.py

The Gradio web application should now be accessible at http://localhost:7860


### 1.3. Execution via command line:

Example of a prediction request

bash
> encoded_image=$(base64 -i ./tests/data/boats.jpg)

> curl -X POST "http://localhost:8080/2015-03-31/functions/function/invocations" \
> -H "Content-Type: application/json" \
> -d '{"body": "'"$encoded_image"'", "isBase64Encoded": true, "model":"yolos-small"}'

python
> python3 inference_api.py \
> --api http://localhost:8080/2015-03-31/functions/function/invocations \
> --file ./tests/data/boats.jpg \
> --model yolos-small


## 2. Deployment to AWS

### 2.1. Pushing the docker container to AWS ECR

<details>

Steps:
 - Create new ECR Repository via aws console

Example: ```object-detection-lambda```


 - Optional for aws cli configuration (to run above commands):
> aws configure
 
 - Authenticate Docker client to the Amazon ECR registry
> aws ecr get-login-password --region <aws_region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com

 - Tag local docker image with the Amazon ECR registry and repository
> docker tag object-detection-lambda:latest <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/object-detection-lambda:latest

 - Push docker image to ECR
> docker push <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/object-detection-lambda:latest

[Link to AWS ECR Documention](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

</details>

### 2.2. Creating and testing a Lambda function

<details>

<b>Steps</b>: 
 - Create function from container image

Example name: ```object-detection```

 - Notes: the API endpoint will use the ```lambda_function.py``` file and ```lambda_hander``` function
 - Test the lambda via the AWS console


Advanced notes:
 - Steps to update the Lambda function with latest container via aws cli:
> aws lambda update-function-code --function-name object-detection --image-uri <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/object-detection-lambda:latest

</details>

### 2.3. Creating a REST API via API Gateway

<details>

<b>Steps</b>: 
 - Create a new ```Rest API``` (e.g. ```object-detection-api```)
 - Add a new resource to the API (e.g. ```/detect```)
 - Add a ```POST``` method to the resource
 - Integrate the Lambda function to the API
   - Notes: currently using proxy integration option unchecked
 - Deploy API with a specific stage (e.g. ```dev``` stage)

</details>

Example AWS API Endpoint:
```https://<api_id>.execute-api.<aws_region>.amazonaws.com/dev/detect```


### 2.4. Execution for deployed model

Example of a prediction request

bash
> encoded_image=$(base64 -i ./tests/data/boats.jpg)

> curl -X POST "https://<api_id>.execute-api.<aws_region>.amazonaws.com/dev/detect" \
> -H "Content-Type: application/json" \
> -d '{"body": "'"$encoded_image"'", "isBase64Encoded": true, "model":"yolos-small"}'

python
> python3 inference_api.py \
> --api https://<api_id>.execute-api.<aws_region>.amazonaws.com/dev/detect \
> --file ./tests/data/boats.jpg \
> --model yolos-small


## 3. Deployment to Hugging Face

This web application is available on Hugging Face

Hugging Face space URL:
https://huggingface.co/spaces/cvachet/object_detection_lambda

Note: This space uses the ML model deployed on AWS Lambda
