"""
%bookmark ri5 /Users/mas/learning/baby-steps-of-rl-ja/DP
%cd ri5
%pwd
"""

import numpy as np

#いずれかの段階でVが確定値になるのであれば、再帰的に関数設定することができる

#行動を5回行い、6回目がゴール

#Bellman Equation, Value Base
#ベルマン方程式に基づく価値
def V(s, gamma=0.99):
    V = R(s) + gamma * max_V_on_next_state(s)
    return V

#Reward Function
def R(s):
    if s == "happy_end":
        return 1
    elif s == "bad_end":
        return -1
    else:
        return 0

#次期の価値の期待値（選択可能な行動の中で最大の期待値）を返す
#結局全パターンを計算していることになる
def max_V_on_next_state(s):
    # If game end, expected value is 0.
    if s in ["happy_end", "bad_end"]:
        return 0
    actions = ["up", "down"]
    values = []
    #各行動毎の価値を求める
    for a in actions:
        #各状態への遷移確率
        transition_probs = transit_func(s, a)
        v = 0
        #来期の価値の期待値を求める
        for next_state in transition_probs:
            prob = transition_probs[next_state]
            v += prob * V(next_state)
        values.append(v)
    #print(s)
    #print(actions[np.argmax(values)] if len(transition_probs) > 1 else 'no choice')
    return max(values)

max_V_on_next_state("state_up_up_up_up_up")
max_V_on_next_state("state_up_up_up_up")


#次期の状態への遷移確率を返す
def transit_func(s, a):
    #状態をを初期状態_行動...で表す
    """
    Make next state by adding action str to state.
    ex: (s = 'state', a = 'up') => 'state_up'
        (s = 'state_up', a = 'down') => 'state_up_down'
    """
    actions = s.split("_")[1:]
    LIMIT_GAME_COUNT = 5
    HAPPY_END_BORDER = 4
    MOVE_PROB = 0.9
    #次回の状態
    def next_state(state, action):
        return "_".join([state, action])
    #終了状態、happy_endかbad_endが100%
    if len(actions) == LIMIT_GAME_COUNT:
        up_count = sum([1 if a == "up" else 0 for a in actions])
        state = "happy_end" if up_count >= HAPPY_END_BORDER else "bad_end"
        prob = 1.0
        return {state: prob}
    #終了状態以外
    else:
        opposite = "up" if a == "down" else "down"
        return {
            next_state(s, a): MOVE_PROB,
            next_state(s, opposite): 1 - MOVE_PROB
        }

V('status')
V('status_up')
V('status_up_up')
V('status_up_up_up')
V('status_up_up_up_up_up')
V('status_up_up_up_up_down')


if __name__ == "__main__":
    print(V("state"))
    print(V("state_up_up"))
    print(V("state_down_down"))
