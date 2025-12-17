# file: model.py
import torch
import torch.nn as nn

class CNNEncoder(nn.Module):
    def __init__(self, n_buses, hidden=64):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=n_buses, out_channels=hidden, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool1d(32)
    def forward(self, x):  # x: batch, time, buses
        x = x.permute(0,2,1) # batch, buses, time
        x = self.conv1(x)    # batch, hidden, time
        x = self.pool(x)     # batch, hidden, 32
        return x.permute(0,2,1)  # batch, time', hidden

class SimpleTransformer(nn.Module):
    def __init__(self, hidden=64, nhead=4, nlayers=2, out_dim=34):
        super().__init__()
        self.enc = nn.TransformerEncoder(nn.TransformerEncoderLayer(d_model=hidden, nhead=nhead), nlayers)
        self.fc = nn.Linear(hidden, out_dim)  # out_dim = num_buses + 1 (no-fault)
    def forward(self, x):
        # x: batch, time', hidden
        x = x.permute(1,0,2) # time', batch, hidden
        x = self.enc(x)
        x = x.mean(dim=0)    # batch, hidden
        return self.fc(x)    # logits

class FaultDetector(nn.Module):
    def __init__(self, n_buses):
        super().__init__()
        self.cnn = CNNEncoder(n_buses)
        self.trans = SimpleTransformer(hidden=64, out_dim=n_buses+1)
    def forward(self, x):
        out = self.cnn(x)
        logits = self.trans(out)
        return logits

# Training loop example omitted for brevity - standard CrossEntropy loss over (n_buses + 1) classes
