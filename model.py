import pandas as pd
import torch
from torch_geometric.data import Data, Dataset
from torch_geometric.nn import GCNConv 
from torch_geometric.loader import DataLoader
from visualize import create_train_data, read_solution,read_raw


x, y, z, a = read_solution()
A,V = read_raw()
nodes, edges = create_train_data(A,V,x, y, z, a)

xdata = torch.tensor(nodes['label'].values, dtype=torch.long)
edge_index = torch.tensor(edges[['source', 'target']].values.T, dtype=torch.long)

data = Data(x=xdata, edge_index=edge_index)

print(data.num_classes)


class GNN(torch.nn.Module):
    
    def __init__(self , hidden_dim):
        super(GNN,self).__init__()
        
        # initilialize the layers
        self.gcn1 = GCNConv(dataset.num_features , hidden_dim)
        self.gcn2 = GCNConv(hidden_dim , hidden_dim)
        
        self.out = torch.nn.Linear(hidden_dim , dataset.num_classes)
        
    def forward(self, x , edge_index):
        
        # first message passing layer
        x = self.gcn1( x , edge_index)
        x = x.relu()
        x = F.dropout(x, p=0.5)
        
        # second message passing layer
        x = self.gcn2(x , edge_index)
        x = x.relu()
        x = F.dropout(x, p=0.4)
        
        # Output layer 
        x = F.log_softmax(self.out(x), dim=1)
        return x