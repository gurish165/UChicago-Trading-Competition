import gym
from gym import spaces

import numpy as np


def get_reward(action, price_df):
    # TODO make reward function
    # process action
    return -1



class AllocateEnv(gym.Env):
    def __init__(self,window_size):
        np.random.seed(0)
        self.np_random = np.random
        self.window_size = window_size
        # allocation of each stock (processed later)
        self.action_space = spaces.Box(shape=(9,))
        # analyst 1, analyst 2, analyst 3, window price data
        self.observation_space = spaces.Tuple((spaces.Box(shape=(9,1)), spaces.Box(shape=(9,1)),
                                               spaces.Box(shape=(9,1)), spaces.Box(shape=(9,window_width))))
        self.ts = 0 # timestep

    def step(self, action, price_df,a_df1,a_df2,a_df3):

        # set reward based on profit
        reward = get_reward(action, price_df)

        observation = (a_df1[:][self.ts], a_df2[:][self.ts], a_df3[:][self.ts]) # set observation

        self.ts += 1

        if (self.ts >= len(price_df)):
            done = True

        return observation, reward, done, {}

    def reset(self):

        return (0, 0, False)

    def render(self):
        pass

