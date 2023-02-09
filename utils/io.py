import pickle
import yaml

def save_as_pkl(obj, output_file):
    """
    Save obj as pkl file
    """
    with open(output_file, 'wb') as pkl_file:
        pickle.dump(obj, pkl_file)


def load_as_pkl(input_file):
    """
    Load pkl file
    """
    with open(input_file, 'rb') as pkl_file:
        obj = pickle.load(pkl_file)
    return obj

def load_yaml_config(file_path):
    """
    Load .yaml config files
    """
    with open(file_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config