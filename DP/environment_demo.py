"""
%bookmark ri5 /Users/mas/learning/baby-steps-of-rl-ja/DP
%cd ri5
%pwd
"""

import random
from environment import Environment

class Agent():
    #環境クラスを入力とする
    def __init__(self, env):
        self.actions = env.actions
    #状態を受け取り、行動を返す（ランダム）
    def policy(self, state):
        return random.choice(self.actions)

def main():
    # Make grid environment.
    grid = [
        [0, 0, 0, 1],
        [0, 9, 0, -1],
        [0, 0, 0, 0]
    ]
    env = Environment(grid)
    agent = Agent(env)

    # Try 10 game.
    for i in range(10):
        # Initialize position of agent.
        state = env.reset()
        #終了フラグ
        total_reward = 0
        done = False
        cnt = 0
        #1エピソードの実行
        while not done:
            #行動の決定
            action = agent.policy(state)
            #行動
            next_state, reward, done = env.step(action)
            cnt += 1
            total_reward += reward
            state = next_state
        #出力
        print("Episode {}: Agent gets {} reward. {} steps.".format(i, total_reward, cnt))


if __name__ == "__main__":
    main()
