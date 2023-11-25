import torch
import torch.nn as nn

import torch.nn.functional as F

import pickle

from transformers import AutoModel, AutoTokenizer

from tqdm import tqdm

from typing import Tuple, List, Dict


class Layer(nn.Module):
    
    def __init__(self, dim: int, device: str = "cuda"):
        super().__init__()
                        
        self.linear = nn.Sequential(
            nn.Linear(dim, dim, device=device),
            nn.BatchNorm1d(dim, device=device),
            nn.ReLU(),
        )
        
    def forward(self, x):        
        return self.linear(x)
    
    
class HierarchicalSoftmax(nn.Module):
    
    def __init__(self, tree: Dict[int, List[int]]):
        super().__init__()
        
        self.tree = tree
        self.specified_indexes_list = [list(tree.keys())]
        
        for head in tree.keys():
            self.specified_indexes_list.append(tree[head])
    
    def forward(self, x):
        x = x.clone()
        
        for specified_indexes in self.specified_indexes_list:
            sub_tensor = x[:, specified_indexes]
        
            softmax_result = F.softmax(sub_tensor, dim=1)
        
            x[:, specified_indexes] = softmax_result
            
        return x


class Model(nn.Module):
    
    def __init__(self, embed_dim: int, hidden_dim: int, num_classes: int, n_layers: int = 1, device: str = "cuda"):
        super().__init__()
        
        self.input = nn.Linear(embed_dim, hidden_dim, device=device)
        self.relu = nn.ReLU()
        self.layers = nn.ModuleList([Layer(hidden_dim, device) for _ in range(n_layers)])
        self.output = nn.Linear(hidden_dim, num_classes, device=device)
        
    def forward(self, x):
        x = self.input(x)
        x = self.relu(x)
        
        for layer in self.layers:
            x = layer(x)
        
        return self.output(x)