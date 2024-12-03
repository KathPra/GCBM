## conda env: clip_ex

# load packages
import torch
import torch.nn as nn
import tqdm
import glob
from collections import Counter
from utilities.dinov2 import compute_embeddings, compute_embeddings_batched, make_classification_eval_transform
import argparse

def load_dataset(dataset):
    if dataset == "cifar10":
        path = "cifar10"
    elif dataset == "cifar100":
        path = "cifar100"
    elif dataset == "ImageNet":
        path = "ImageNet/ILSVRC/Data/CLS-LOC"
    elif dataset == "ClimateTV":
        path = "ClimateTV"
    elif dataset == "CUB":
        path = "CUB_200_2011"
        # -> paths in test folder
    elif dataset == "Places365":
        path = "Places365/Data"
    elif dataset == "MiT-States":
        path = "MiT-States/release_dataset/"
    elif dataset == "ImageNet-R":
        path = "ImageNet-R/imagenet-r"
        # no train or test folder -> use val for test
    return path

def main(dataset, device):
    # load model
    model_name = "dinov2_vitl14" 
    model = torch.hub.load('facebookresearch/dinov2', model_name)
    preprocess = make_classification_eval_transform()
    model.eval() 
    model.to(device)

    dataset_path = load_dataset(dataset)
    ## train set ##
    train_list = glob.glob(dataset_path+"/train/*/*")
    # create and save embeddings Image embeddings
    output_train = f"images_{dataset}_train_{model_name}.torch"
    compute_embeddings_batched(train_list, model, preprocess, output_train, device)
    output_train = None
    
    ## val set ##
    val_list = glob.glob(dataset_path+"/val/*/*")
    # create and save embeddings Image embeddings
    output_val = f"images_{dataset}_val_{model_name}.torch"
    compute_embeddings_batched(val_list, model, preprocess, output_val, device)
    output_val = None

    ## test set ##
    test_list = glob.glob(dataset_path+"/test/*/*")
    print(len(test_list))
    output_test = f"images_{dataset}_test_{model_name}.torch"
    compute_embeddings_batched(test_list, model, preprocess, output_test, device)
    
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dataset', type=str, help='dataset name')
    parser.add_argument('--device', type=str, help='device')
    args = parser.parse_args()
    main(args.dataset, args.device)