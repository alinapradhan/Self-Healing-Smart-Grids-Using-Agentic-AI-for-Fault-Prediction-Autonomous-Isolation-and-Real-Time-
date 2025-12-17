
# file: create_33bus.py
import pandapower as pp
import pandapower.networks as pn
import numpy as np
import pandas as pd

# Option A: Use built-in or repo version of 33-bus if available. Otherwise build from line data.
# Quick: create a simple radial network using pandapower example (you can replace with IEEE 33 lines)
net = pn.create_cigre_network_mv()  # small test network - replace with IEEE 33 model if you have data

# Example: function to inject single-line-to-ground fault at a bus by creating a short (low impedance)
def inject_fault(net, bus_idx, z_fault=1e-3):
    # create a new element that imposes a connection to ground: simple approach is to add a shunt with large admittance
    vn_kv = net.bus.vn_kv.iloc[bus_idx]
    # Add an external short - using an external load with very low impedance
    pp.create_load(net, bus=bus_idx, p_mw=0.0, q_mvar=0.0, const_z_percent=0.0)
    # NOTE: For accurate transient short-circuit you would use specialized tools (OpenDSS/GridLAB-D)
    return

# Run power flow and read measurements
pp.runpp(net)
voltages = net.res_bus.vm_pu.values
print("Bus voltages (pu):", voltages)

