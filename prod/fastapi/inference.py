import torch
import torch.nn as nn
import torch.nn.functional as F

import pickle

from transformers import AutoModel, AutoTokenizer

from tqdm import tqdm

from typing import Tuple, List, Dict

from entites import *


def predict(output: torch.Tensor, tree: Dict[int, List[int]]):
    softmax = HierarchicalSoftmax(tree)
    
    output = softmax(output)
    
    tree_heads = list(tree.keys())
    
    groups_prob = output[:, tree_heads]
    
    groups_index = groups_prob.argmax(dim=1).tolist()
    
    indexes = []
    for k, gi in enumerate(tqdm(groups_index)):
        theme_index = output[:, tree[gi]].argmax(dim=1)[k].item()
        
        indexes.append([gi, tree[gi][theme_index]])
        
    return indexes


def make_embeddings(encoder, tokenizer, texts):
    x = tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt").to(encoder.device)

    y = encoder(**x).last_hidden_state.mean(dim=1)

    return y


def make_predict(model: Model, 
                 input_tensors: torch.Tensor, 
                 tree: Dict[int, List[int]],
                 reversed_mapping: Dict[int, str]) -> Dict[str, str]:

    predictions = predict(model(input_tensors), tree)

    
    results = []
    for pred in predictions:
        results.append({
            "group": reversed_mapping[pred[0]].replace("Группа: ", ""),
            "theme": reversed_mapping[pred[1]]
        })

    return results