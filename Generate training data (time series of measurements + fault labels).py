# file: data_gen.py
import numpy as np
import pandas as pd
from create_33bus import net, inject_fault, pp, pp as pandapower

def sample_scenarios(net, n_samples=500, n_steps=100):
    rows = []
    labels = []
    for s in range(n_samples):
        # randomly choose if a fault occurs and where
        fault_occur = np.random.rand() < 0.5
        fault_bus = np.random.randint(len(net.bus)) if fault_occur else None
        # simulate a small sequence (this is steady-state per step; for transient you'd need time-series simulator)
        seq = []
        for t in range(n_steps):
            if fault_occur and t == n_steps//3:
                inject_fault(net, fault_bus)
            pp.runpp(net)
            vm = net.res_bus.vm_pu.values.copy()
            seq.append(vm)
        rows.append(np.stack(seq))          # shape: (n_steps, n_buses)
        labels.append(fault_bus if fault_occur else -1)
        # reset net to pre-fault state — implement restore function as needed
    return np.array(rows), np.array(labels)

# Example usage:
# X, y = sample_scenarios(net, n_samples=200, n_steps=80)
# Save to disk
# np.save("X.npy", X); np.save("y.npy", y)
