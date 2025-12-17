## This is actual RLLib MARL training code.
import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from env import SelfHealingGridEnv

ray.init(ignore_reinit_error=True)

env_config = {
    "num_buses": 33,
    "switches": {
        "sw_1": (0, 1),
        "sw_2": (1, 2),
        "sw_3": (2, 3)
    }
}

config = (
    PPOConfig()
    .environment(env=SelfHealingGridEnv, env_config=env_config)
    .framework("torch")
    .rollouts(num_rollout_workers=1)
    .training(
        gamma=0.99,
        lr=3e-4,
        train_batch_size=400,
        model={"fcnet_hiddens": [128, 128]}
    )
    .multi_agent(
        policies={"shared_policy"},
        policy_mapping_fn=lambda agent_id, *args, **kwargs: "shared_policy"
    )
)

tune.run(
    "PPO",
    config=config.to_dict(),
    stop={"training_iteration": 50},
    checkpoint_at_end=True
)
