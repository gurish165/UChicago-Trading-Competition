from rl_agent import AllocateEnv
import pandas as pd
import numpy as np

price = pd.read_csv('Acutal Testing Data.csv',index_col=0).to_numpy()
a1 = pd.read_csv('Predicted Testing Data Analyst 1.csv',index_col=0).to_numpy()
a2 = pd.read_csv('Predicted Testing Data Analyst 2.csv',index_col=0).to_numpy()
a3 = pd.read_csv('Predicted Testing Data Analyst 3.csv',index_col=0).to_numpy()

env = AllocateEnv(10, price, a1, a2, a3)

while not input("Press enter to continue"):
    observation = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
    env.render()
env.close()
