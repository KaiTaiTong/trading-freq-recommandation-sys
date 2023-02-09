import random
import os
from utils.io import load_yaml_config


TRAIN_SPLIT = load_yaml_config('./configs.yaml')['TRAIN_SPLIT']
PARENT_DIR = ['./data/stock_market_data/forbes2000/csv/', 
              './data/stock_market_data/nasdaq/csv/', 
              './data/stock_market_data/nyse/csv/']


def generate_train_test_set(train_split, parent_dir, output_dir):
    """
    Generate train_set.txt and test_set.txt. For our specific application, we do not 
    need validation set

    Args:
        train_split (float): ratio of trainset
        parent_dir (list): parent dir list
        output_dir (str): output dir
    """
    assert(0 < train_split <= 1), "train_split must be in (0, 1]"

    # Load raw dataset dir
    train_set, test_set = [], []
    for current_parent_dir in parent_dir:
        child_dir = os.listdir(current_parent_dir)
        train_set += [current_parent_dir + i for i in child_dir[0:int(train_split*len(child_dir))]]
        test_set += [current_parent_dir + i for i in child_dir[int(train_split*len(child_dir)):]]

    # Shuffle dataset
    random.shuffle(train_set)
    random.shuffle(test_set)

    with open(output_dir + './train_set.txt', 'w') as f:
        for line in train_set:
            f.write(f"{line}\n")
    with open(output_dir + './test_set.txt', 'w') as f:
        for line in test_set:
            f.write(f"{line}\n")


if __name__ == '__main__':
    generate_train_test_set(TRAIN_SPLIT, PARENT_DIR, './data/')