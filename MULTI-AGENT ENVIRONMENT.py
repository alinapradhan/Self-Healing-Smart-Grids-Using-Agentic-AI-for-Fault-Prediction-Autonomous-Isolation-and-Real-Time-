##This is the core MARL scaffold
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from ray.rllib.env.multi_agent_env import MultiAgentEnv

class SelfHealingGridEnv(MultiAgentEnv):
    """
    Each agent controls one switch
    """

    def __init__(self, config):
        self.num_buses = config.get("num_buses", 33)
        self.switches = config.get("switches", {
            "sw_1": (0, 1),
            "sw_2": (1, 2),
            "sw_3": (2, 3)
        })

        self.agents = list(self.switches.keys())
        self.max_steps = 20
        self.step_count = 0

        # Fault location
        self.fault_bus = np.random.randint(0, self.num_buses)

        # Observation: [local_voltage, fault_signal]
        self.observation_space = spaces.Box(
            low=0.0, high=1.2, shape=(2,), dtype=np.float32
        )

        # Actions:
        # 0 = do nothing
        # 1 = open switch
        # 2 = close switch
        self.action_space = spaces.Discrete(3)

    def reset(self, *, seed=None, options=None):
        self.step_count = 0
        self.fault_bus = np.random.randint(0, self.num_buses)

        obs = {}
        for agent in self.agents:
            obs[agent] = np.array([1.0, 1.0], dtype=np.float32)

        return obs, {}

    def step(self, action_dict):
        self.step_count += 1

        obs, rewards, dones, infos = {}, {}, {}, {}

        for agent, action in action_dict.items():
            # Fake voltage drop if fault not isolated
            voltage = 0.7 if self.step_count < 5 else 0.95

            # Reward design
            reward = 0.0
            if action == 1:      # open switch
                reward += 1.0
            if voltage < 0.9:
                reward -= 0.5

            obs[agent] = np.array([voltage, 1.0], dtype=np.float32)
            rewards[agent] = reward
            dones[agent] = False
            infos[agent] = {}

        dones["__all__"] = self.step_count >= self.max_steps

        return obs, rewards, dones, infos
