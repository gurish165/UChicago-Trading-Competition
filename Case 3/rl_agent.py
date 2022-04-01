import gym
from gym import spaces

import numpy as np

class AllocateEnv(gym.Env):
    def __init__(self,window_size, price,a_pred1,a_pred2,a_pred3):
        np.random.seed(0)
        self.np_random = np.random
        self.window_size = window_size
        self.observation_high_1d = np.full((9,), np.finfo(np.float32).max, dtype=np.float32)
        self.observation_min_1d = np.full((9,), np.finfo(np.float32).min, dtype=np.float32)

        self.observation_high_2d = np.full((9,window_size), np.finfo(np.float32).max, dtype=np.float32)
        self.observation_min_2d = np.full((9,window_size), np.finfo(np.float32).min, dtype=np.float32)

        # allocation of each stock (processed later)
        self.action_space = spaces.Box(self.observation_min_1d, self.observation_high_1d, dtype=np.float32)
        # analyst 1, analyst 2, analyst 3, window price data
        self.observation_space = spaces.Tuple((spaces.Box(self.observation_min_1d, self.observation_high_1d, dtype=np.float32), spaces.Box(self.observation_min_1d, self.observation_high_1d, dtype=np.float32),
                                               spaces.Box(self.observation_min_1d, self.observation_high_1d, dtype=np.float32), spaces.Box(self.observation_min_2d, self.observation_high_2d, dtype=np.float32)))
        self.ts = self.window_size # timestep

        self.price = price
        self.a_pred1 = a_pred1
        self.a_pred2 = a_pred2
        self.a_pred3 = a_pred3

        self.obs_begin = (self.a_pred1[self.ts][:], self.a_pred2[self.ts][:], self.a_pred3[self.ts][:],
                          self.price[self.ts-self.window_size:self.ts])

        self.returns = []

    def get_reward(self, action):
        # TODO make reward function
        # process action
        weight = action
        prev_row = np.array(self.price[self.ts], dtype=np.float32)
        current_row = np.array(self.price[self.ts+1], dtype=np.float32)
        return_pct = weight*((current_row - prev_row) / prev_row)
        return np.sum(return_pct, dtype=np.float32)

    def step(self, action):

        # set reward based on profit
        reward = self.get_reward(action)
        # set observation
        observation = (np.array(self.a_pred1[self.ts], dtype=np.float32), np.array(self.a_pred2[self.ts], dtype=np.float32),
                        np.array(self.a_pred3[self.ts][:], dtype=np.float32),
                       np.array(self.price[self.ts-self.window_size:self.ts], dtype=np.float32))
        self.ts += 1
        done = False
        if (self.ts >= len(self.price)-1):
            done = True

        self.returns.append(reward)
        return observation, reward, done, {}

    def reset(self):
        self.ts = self.window_size
        self.returns = []
        return (np.zeros((9,), dtype=np.float32), np.zeros((9,), dtype=np.float32), np.zeros((9,), dtype=np.float32), np.zeros((9,self.window_size), dtype=np.float32))

    def render(self):
        self.returns = np.array(self.returns, dtype=np.float32)
        print("Mean :",np.mean(self.returns))
        print("Std :", np.std(self.returns))
        sharpe_ratio = np.mean(self.returns) / np.std(self.returns)
        print(f"SHARPE RATIO: {sharpe_ratio}")
        pass

