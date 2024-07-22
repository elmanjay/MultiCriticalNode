import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler
import torch.nn.functional as F
from torch_geometric.data import Data, Dataset
from torch_geometric.nn import GCNConv
from torch_geometric.loader import DataLoader
from visualize import create_train_data, read_solution, read_raw

# Read and prepare data
x, y, z, a = read_solution()
A, V = read_raw()
nodes, edges = create_train_data(A, V, x, y, z, a)
nodes["node_id"] = nodes["node_id"] - 1
#scaler = MinMaxScaler()
#nodes["node_id"] = scaler.fit_transform(nodes[["node_id"]])
print(nodes)
edges["source"] = edges["source"] - 1
edges["target"] = edges["target"] - 1

print(edges)


xdata = torch.tensor(nodes["node_id"].values, dtype=torch.float).unsqueeze(1)
ydata = torch.tensor(nodes["label"].values, dtype=torch.long)
edge_index = torch.tensor(edges[["source", "target"]].values.T, dtype=torch.long)
print("xdata shape:", xdata.shape)
print(edge_index)





data = Data(x=xdata, edge_index=edge_index, y=ydata, dtype=torch.long)
data.num_classes= len(torch.unique(data.y))

#Define the GNN model
class GNN(torch.nn.Module):
    def __init__(self, num_features, num_classes, hidden_dim):
        super(GNN, self).__init__()
        self.gcn1 = GCNConv(num_features, hidden_dim)
        self.gcn2 = GCNConv(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x, edge_index):
        x = self.gcn1(x, edge_index)
        x = x.relu()
        x = F.dropout(x, p=0.5, training=self.training)
        
        x = self.gcn2(x, edge_index)
        x = x.relu()
        x = F.dropout(x, p=0.4, training=self.training)
        
        x = F.log_softmax(self.out(x), dim=1)
        return x

#Initialize model, optimizer, and loss function
hidden_dim = 16
model = GNN(num_features=data.num_features, num_classes=data.num_classes, hidden_dim=hidden_dim)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

#Create a DataLoader
data_list = [data]  # In a real scenario, you might have multiple data objects
loader = DataLoader(data_list, batch_size=1, shuffle=True)

#Training loop
def train(num_epochs=10000):
    for epoch in range(num_epochs):
        model.train()
        for data in loader:
            optimizer.zero_grad()
            out = model(data.x, data.edge_index)
            loss = criterion(out, data.y)
            loss.backward()
            optimizer.step()
            print(f"Loss: {loss.item()}")

#Run the training
train()

# Make predictions
def predict(model, data):
    model.eval()  # Switch model to evaluation mode
    with torch.no_grad():  # Disable gradient calculation
        out = model(data.x, data.edge_index)
        predictions = out.argmax(dim=1)  # Get the predicted class with the highest probability
    return predictions

# Get predictions
predictions = predict(model, data)

# Print predictions
print("Predictions:", predictions.numpy())