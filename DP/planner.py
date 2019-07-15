"""
%bookmark ri5 /Users/mas/learning/baby-steps-of-rl-ja/DP
%cd ri5
%pwd
"""

#行動決定部分を定義する

#Valueベース、Policyベース共通のメソッド
class Planner():

    def __init__(self, env):
        self.env = env
        self.log = []

    def initialize(self):
        self.env.reset()
        self.log = []

    def plan(self, gamma=0.9, threshold=0.0001):
        raise Exception("Planner have to implements plan method.")
    
    #各状態への遷移確率と遷移先で得られる報酬を返す（ジェネレーターとして）
    def transitions_at(self, state, action):
        transition_probs = self.env.transit_func(state, action)
        for next_state in transition_probs:
            prob = transition_probs[next_state]
            reward, _ = self.env.reward_func(next_state)
            yield prob, next_state, reward
    #各状態毎の報酬（辞書形式）をリスト化（grid）して返す
    def dict_to_grid(self, state_reward_dict):
        grid = []
        for i in range(self.env.row_length):
            row = [0] * self.env.column_length
            grid.append(row)
        for s in state_reward_dict:
            grid[s.row][s.column] = state_reward_dict[s]

        return grid


# Valueベースの学習、状態別の価値を学習し、更新していく
# ある状態における各行動の期待値を算出し、最大値をその状態の価値としている
class ValuteIterationPlanner(Planner):
    #親クラスの初期化
    def __init__(self, env):
        #super()は親クラスを表す
        super().__init__(env)
    #動的計画プロセス
    def plan(self, gamma=0.9, threshold=0.0001):
        self.initialize()
        #選択可能な行動のリスト
        actions = self.env.actions
        V = {}
        #各状態の価値を辞書として定義
        for s in self.env.states:
            # Initialize each state's expected reward.
            #初期値はゼロ
            V[s] = 0
        #学習
        while True:
            delta = 0
            #学習毎にログに各状態別の価値のリストを追加
            self.log.append(self.dict_to_grid(V))
            #各状態（辞書）をループ、各状態の価値の期待値の最大値を求める
            for s in V:
                #通常状態以外はスキップして次のループへ
                if not self.env.can_action_at(s):
                    continue
                #各行動をループ、各行動別の価値の期待値を求める
                expected_rewards = []
                for a in actions:
                    r = 0
                    #次期の遷移確率と報酬
                    for prob, next_state, reward in self.transitions_at(s, a):
                        #価値の期待値
                        r += prob * (reward + gamma * V[next_state])
                    expected_rewards.append(r)
                max_reward = max(expected_rewards)
                #価値の更新幅の最大値（全状態）
                delta = max(delta, abs(max_reward - V[s]))
                V[s] = max_reward
            #価値の更新幅が閾値未満で学習終了
            if delta < threshold:
                break
        #各状態の価値をリスト（グリッド）で返す
        V_grid = self.dict_to_grid(V)
        return V_grid



# Policyベースの学習
# 各状態における価値の期待値を更新
class PolicyIterationPlanner(Planner):
    #親クラスの初期化
    def __init__(self, env):
        super().__init__(env)
        self.policy = {}
    #ポリシーを含めてリセット
    def initialize(self):
        super().initialize()
        self.policy = {}
        #選択可能な行動オブジェクトのリスト
        actions = self.env.actions
        #選択可能な状態オブジェクトのリスト
        states = self.env.states
        #状態別に各行動の選択確率を記録した辞書の辞書を作成（ポリシー）
        #初期値は等ウェイト
        for s in states:
            self.policy[s] = {}
            for a in actions:
                # Initialize policy.
                # At first, each action is taken uniformly.
                self.policy[s][a] = 1 / len(actions)
    #各状態価値の学習
    #ある状態における各行動の期待値とポリシー（各行動の選択確率）から、その状態の価値を求める
    def estimate_by_policy(self, gamma, threshold):
        #各状態の価値を初期化、全てゼロ
        V = {}
        for s in self.env.states:
            # Initialize each state's expected reward.
            V[s] = 0
        #学習
        while True:
            delta = 0
            #各状態をループ
            for s in V:
                expected_rewards = []
                #各行動をループ
                for a in self.policy[s]:
                    action_prob = self.policy[s][a]
                    r = 0
                    #次期の遷移確率と報酬のループ
                    #各行動の価値の期待値を求める
                    for prob, next_state, reward in self.transitions_at(s, a):
                        r += action_prob * prob * \
                             (reward + gamma * V[next_state])
                    expected_rewards.append(r)
                #全行動の期待値
                value = sum(expected_rewards)
                #価値の更新幅の最大値（全状態）
                delta = max(delta, abs(value - V[s]))
                V[s] = value
            #更新幅が小さくなったら学習終了
            if delta < threshold:
                break
        return V
    #各状態の価値の基づいたポリシー（行動選択確率）の更新
    #期待値が最大な行動の選択確率が100%になるように、ポリシーと状態価値を更新していく
    #各状態価値はポリシーに依存するため、相互に繰り返し計算を行う必要がある
    def plan(self, gamma=0.9, threshold=0.0001):
        self.initialize()
        states = self.env.states
        actions = self.env.actions
        #値が最大のキーを返す
        def take_max_action(action_value_dict):
            return max(action_value_dict, key=action_value_dict.get)
        #ポリシーの更新と、新しいポリシーに基づく各状態価値の更新
        while True:
            update_stable = True
            # Estimate expected rewards under current policy.
            #各状態の価値を学習し、辞書で返す
            V = self.estimate_by_policy(gamma, threshold)
            #各状態の価値をグリッド（リスト）に変換して、ログとして記録
            self.log.append(self.dict_to_grid(V))
            #全状態をループ
            for s in states:
                # Get an action following to the current policy.
                #最大確率の行動を取得
                policy_action = take_max_action(self.policy[s])
                # Compare with other actions.
                action_rewards = {}
                #全行動をループ
                for a in actions:
                    r = 0
                    #次期の各遷移確率と報酬をループ、行動の期待値を算出
                    for prob, next_state, reward in self.transitions_at(s, a):
                        r += prob * (reward + gamma * V[next_state])
                    action_rewards[a] = r
                #最大の価値を得る行動を選択
                best_action = take_max_action(action_rewards)
                #ポリシーが選択する行動と価値が最大になる行動が一致しない場合
                if policy_action != best_action:
                    update_stable = False
                # Update policy (set best_action prob=1, otherwise=0 (greedy))
                #ポリシーの更新
                for a in self.policy[s]:
                    #最大の価値を得る行動の選択確率を100%にする
                    prob = 1 if a == best_action else 0
                    self.policy[s][a] = prob
            #ポリシーの更新がなくなったら終了
            if update_stable:
                # If policy isn't updated, stop iteration
                break
        # Turn dictionary to grid
        V_grid = self.dict_to_grid(V)
        #最終的なポリシーの下での各状態価値をグリッド（リスト）で返す
        return V_grid
