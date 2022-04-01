from argparse import ArgumentParser
from rl_agent import AllocateEnv

import gym
import ray
import pandas as pd
import numpy as np
from ray.tune.registry import register_env
from ray.rllib.agents.ppo import PPOTrainer

arg_parser = ArgumentParser()
arg_parser.add_argument("--iter", type=int, default=100)
args = arg_parser.parse_args()

price = pd.read_csv('Acutal Testing Data.csv',index_col=0, dtype=np.float32).to_numpy()
a1 = pd.read_csv('Predicted Testing Data Analyst 1.csv',index_col=0, dtype=np.float32).to_numpy()
a2 = pd.read_csv('Predicted Testing Data Analyst 2.csv',index_col=0, dtype=np.float32).to_numpy()
a3 = pd.read_csv('Predicted Testing Data Analyst 3.csv',index_col=0, dtype=np.float32).to_numpy()

window_size = 50

def create_env(config):
    return AllocateEnv(50, price, a1, a2, a3)


env_name = 'AllocateEnv'
register_env(env_name, create_env)

ray.init()

config = {
    'env': env_name,
    'framework': 'torch',
    'num_workers': 1,
    'evaluation_interval': 1,
    'evaluation_duration': 100,
    'evaluation_config': {
    'explore': False
    },
}

agent = PPOTrainer(env=env_name, config=config)

#from tqdm import tqdm

train_iters = 10

#for i in tqdm(range(train_iters)):
   #agent.train()

# for i in range(args.iter):
#     print('iter: ',i)
result = agent.train()

agent.evaluate()