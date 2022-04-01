from rl_agent import AllocateEnv
import pandas as pd
import numpy as np

env = AllocateEnv(10)

price_df = pd.read_csv('Acutal Testing Data.csv').to_numpy()
a_df1 = pd.read_csv('Predicted Testing Data Analyst 1.csv').to_numpy()
a_df2 = pd.read_csv('Predicted Testing Data Analyst 2.csv').to_numpy()
a_df3 = pd.read_csv('Predicted Testing Data Analyst 3.csv').to_numpy()

while not input("Press enter to continue"):
    observation = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action, price_df,a_df1,a_df2,a_df3)
    env.render()
env.close()
