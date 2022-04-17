import ray
from ray.tune.registry import register_env


def create_env(config):
    return BlackjackEnv(config['seed'])


env_name = 'Blackjack'

ray.init()
register_env(env_name, create_env)

from ray.rllib.agents.ppo import PPOTrainer

config = {
    'env': env_name,
    'env_config' : {
      'seed': 999
    },
    'framework': 'torch',
    'num_workers': 1,
    'evaluation_interval': 1,
    'evaluation_duration': 100,
    'evaluation_config': {
      'env_config' : {
        'seed': 0
      },
      'explore': False
    },
}

agent = PPOTrainer(env=env_name, config=config)

from tqdm import tqdm

train_iters = 10

for i in tqdm(range(train_iters)):
   agent.train()

num_episodes = 10000

env = BlackjackEnv()

total_reward = 0.0

for _ in range(num_episodes):
    observation = env.reset()
    done = False
    while not done:
        action = agent.compute_single_action(observation)
        observation, reward, done, info = env.step(action)
    total_reward += reward
env.close()

print("Average reward: " + str(total_reward / num_episodes))

env = BlackjackEnv()

while not input("Press enter to continue"):
    observation = env.reset()
    done = False
    while not done:
        action = agent.compute_single_action(observation)
        observation, reward, done, info = env.step(action)
    env.render()
env.close()