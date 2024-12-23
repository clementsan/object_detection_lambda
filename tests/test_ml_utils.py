from detection import ml_utils
import torch
import json


# Test dictionary conversion
def test_convert_tensor_dict_to_json():
    my_dict = {'scores': torch.tensor([1, 2, 3])}
    my_list_gt = {'scores': [1, 2, 3]}
    my_list = ml_utils.convert_tensor_dict_to_json(my_dict)
    assert my_list == my_list_gt
