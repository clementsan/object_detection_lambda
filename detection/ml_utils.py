"""
Utility functions for detection module
"""

import torch


def convert_tensor_dict_to_json(tensor_dict):
    """Convert a dictionary of tensors to a JSON-serializable dictionary."""

    json_dict = {
        key: (
            value.detach().cpu().numpy().tolist()
            if isinstance(value, torch.Tensor)
            else value
        )
        for key, value in tensor_dict.items()
    }

    # Convert to JSON string
    # json_str = json.dumps(json_dict)
    # print(json_str)

    return json_dict
