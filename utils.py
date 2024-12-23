from PIL import Image
import matplotlib.pyplot as plt
import io


# COCO classes
CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]
COLORS = [
    [0.000, 0.447, 0.741],
    [0.850, 0.325, 0.098],
    [0.929, 0.694, 0.125],
    [0.494, 0.184, 0.556],
    [0.466, 0.674, 0.188],
    [0.301, 0.745, 0.933],
]


# Update JSON dictionary with rounded values and class names
def generate_output_json(json_dict):
    json_dict['scores'] = [round(score, 3) for score in json_dict['scores']]
    json_dict['boxes'] = [[round(coord, 3) for coord in box] for box in json_dict['boxes']]
    json_dict['labels'] = [CLASSES[label] for label in json_dict['labels']]
    return json_dict


# Generate matplotlib figure from prediction scores and boxes
def generate_output_figure(image_path, predictions, threshold):
    pil_img = Image.open(image_path)

    plt.figure(figsize=(16, 10))
    plt.imshow(pil_img)
    ax = plt.gca()
    colors = COLORS * 100

    print("\t Detailed information...")
    for score, label, box in zip(predictions["scores"], predictions["labels"], predictions["boxes"]):
        #box = [round(i, 2) for i in box]
        print(
            f"\t\t Detected {label} with confidence "
            f"{score} at location {box}"
        )

        if score > threshold:
            c = COLORS[hash(label) % len(COLORS)]
            ax.add_patch(
                plt.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], fill=False, color=c, linewidth=3)
            )
            text = f"{label}: {score:0.2f}"
            ax.text(box[0], box[1], text, fontsize=15, bbox=dict(facecolor="yellow", alpha=0.5))
    plt.axis("off")

    return plt.gcf()


#  Generate PIL image from matplotlib figure
def generate_output_image(output_figure):
    # Convert matplotlib figure to PIL image
    #output_figure = plt.gcf()
    buf = io.BytesIO()
    output_figure.savefig(buf, bbox_inches="tight")
    buf.seek(0)
    output_pil_img = Image.open(buf)

    return output_pil_img


def generate_gradio_outputs(image_path, prediction_dict, threshold):
    output_json = generate_output_json(prediction_dict)
    output_figure = generate_output_figure(image_path, output_json, threshold)
    output_pil_img = generate_output_image(output_figure)
    return output_json, output_pil_img
