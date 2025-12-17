# file: controller.py
def rule_based_isolate(predicted_bus, net, switches):
    """
    predicted_bus: int or -1 (no fault)
    net: pandapower network
    switches: mapping switch_id -> (from_bus, to_bus)
    """
    if predicted_bus == -1:
        return None
    # basic rule: open nearest switch(es) that isolate predicted_bus subtree
    # For a radial network you can open the upstream switch feeding that bus
    # Implementation depends on your network model; here's a placeholder:
    actions = []
    for sw_id, (f,t) in switches.items():
        if t == predicted_bus or f == predicted_bus:
            # open switch
            actions.append(("open", sw_id))
    return actions
