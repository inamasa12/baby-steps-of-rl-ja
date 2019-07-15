"""
%bookmark ri4 /Users/mas/learning/baby-steps-of-rl-ja/MyObjects
%cd ri4
%bookmark ri5 /Users/mas/learning/baby-steps-of-rl-ja/DP
%cd ri5
%pwd
"""

from enum import Enum
import numpy as np

#環境を定義する

#状態クラス、行番号と列番号を保持するだけ
class State():
    def __init__(self, row=-1, column=-1):
        self.row = row
        self.column = column
    # 変数名を実行した時の返り値を規定
    def __repr__(self):
        return "<State: [{}, {}]>".format(self.row, self.column)

    def clone(self):
        return State(self.row, self.column)
    
    #　ハッシュ値の定義、行数と列数から成るタプルをハッシュ値に変換
    def __hash__(self):
        return hash((self.row, self.column))

    # 「=」 の処理を規定
    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

#行動パラメータオブジェクト
class Action(Enum):
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2

#実行環境オブジェクト
#迷路を受け取り、属性及び迷路実行メソッドを定義
class Environment():
    #状態の初期化関数
    #gridは迷路、move_probは選択した方向に行動する確率
    def __init__(self, grid, move_prob=0.8):
        # grid is 2d-array. Its values are treated as an attribute.
        # Kinds of attribute is following.
        #  0: ordinary cell
        #  -1: damage cell (game end)
        #  1: reward cell (game end)
        #  9: block cell (can't locate agent)
        #地図と状態を保有
        self.grid = grid
        self.agent_state = State()

        # Default reward is minus. Just like a poison swamp.
        # It means the agent has to reach the goal fast!
        self.default_reward = -0.04

        # Agent can move to a selected direction in move_prob.
        # It means the agent will move different direction
        # in (1 - move_prob).
        #ベースとなる行動方向の遷移確率
        self.move_prob = move_prob
        self.reset()
    #迷路の行数
    @property
    def row_length(self):
        return len(self.grid)
    #迷路の列数
    @property
    def column_length(self):
        return len(self.grid[0])    
    #選択可能な行動のリスト
    @property
    def actions(self):
        return [Action.UP, Action.DOWN,
                Action.LEFT, Action.RIGHT]
    #迷路の各セルに対応した状態クラスを有したリスト、選択可能な状態オブジェクトのリスト
    @property
    def states(self):
        states = []
        for row in range(self.row_length):
            for column in range(self.column_length):
                # Block cells are not included to the state.
                if self.grid[row][column] != 9:
                    states.append(State(row, column))
        return states

    #次の各状態に遷移する確率を辞書形式で返す
    #特定の状態オブジェクト、特定の行動オブジェクトの属性値を入力
    def transit_func(self, state, action):
        #状態別に遷移確率を収録する辞書
        transition_probs = {}
        #通常セル以外は何も返さない
        if not self.can_action_at(state):
            # Already on the terminal cell.
            return transition_probs
        #選択した行動と逆方向の行動オブジェクトの属性値
        opposite_direction = Action(action.value * -1)
        #状態（行動別）の遷移確率を作成、辞書のキーが状態、値が遷移確率
        for a in self.actions:
            prob = 0
            if a == action:
                prob = self.move_prob
            #選択した行動と真逆の方向以外は進む確率が存在する
            elif a != opposite_direction:
                prob = (1 - self.move_prob) / 2
            #選択した行動を取った時にシフトする次の状態オフジェクト
            next_state = self._move(state, a)
            if next_state not in transition_probs:
                transition_probs[next_state] = prob
            else:
                #元の状態に戻るケースがあるため
                transition_probs[next_state] += prob
        #次回の状態への遷移確率を辞書形式で返す
        return transition_probs

    #通常状態のセルの場合にTrue
    def can_action_at(self, state):
        if self.grid[state.row][state.column] == 0:
            return True
        else:
            return False
        
    #次回の状態を返す
    def _move(self, state, action):
        #通常セル以外から行動を起こすとエラー
        if not self.can_action_at(state):
            raise Exception("Can't move from here!")
        #状態を複製
        next_state = state.clone()
        #行動後の状態、行*列
        # Execute an action (move).
        if action == Action.UP:
            #UPは下方向にシフト
            next_state.row -= 1
        elif action == Action.DOWN:
            #DOWNは上方向にシフト
            next_state.row += 1
        elif action == Action.LEFT:
            next_state.column -= 1
        elif action == Action.RIGHT:
            next_state.column += 1
        #迷路の範囲を超えた場合は、動かなかったことにする
        # Check whether a state is out of the grid.
        if not (0 <= next_state.row < self.row_length):
            next_state = state
        if not (0 <= next_state.column < self.column_length):
            next_state = state
        #移動できないセルに動いた場合も、動かなかったことにする
        # Check whether the agent bumped a block cell.
        if self.grid[next_state.row][next_state.column] == 9:
            next_state = state
        #次回の状態オブジェクトを返す
        return next_state
    
    #与えられた状態の報酬値、終了フラグを返す
    def reward_func(self, state):
        reward = self.default_reward
        #終了フラグ
        done = False
        # Check an attribute of next state.
        attribute = self.grid[state.row][state.column]
        #状態がゴールの場合
        if attribute == 1:
            # Get reward! and the game ends.
            reward = 1
            done = True
        #状態が間違いのゴールの場合
        elif attribute == -1:
            # Get damage! and the game ends.
            reward = -1
            done = True
        #報酬値（スカラー）と終了フラグを返す
        return reward, done
    
    #状態のリセット、左下のセルの状態
    def reset(self):
        # Locate the agent at lower left corner.
        self.agent_state = State(self.row_length - 1, 0)
        return self.agent_state
    
    #行動に基づき、状態をシフトさせる、次の状態オブジェクト、即時報酬、終了フラグを返す
    def step(self, action):
        next_state, reward, done = self.transit(self.agent_state, action)
        if next_state is not None:
            self.agent_state = next_state
        #次の状態オブジェクト、即時報酬、終了フラグを返す
        return next_state, reward, done
    
    #次期の状態オブジェクトと報酬、終了フラグを返す
    def transit(self, state, action):
        #任意の状態及び選択した行動に対する、次の状態の遷移確率を取得
        transition_probs = self.transit_func(state, action)
        #既に状態がゴールしている場合の処理
        if len(transition_probs) == 0:
            return None, None, True
        next_states = []
        probs = []
        for s in transition_probs:
            #次の状態オブジェクトのリスト
            next_states.append(s)
            #次の状態への遷移確率のリスト
            probs.append(transition_probs[s])
        #遷移確率に応じて次の状態オブジェクトを取得
        next_state = np.random.choice(next_states, p=probs)
        #次の状態の報酬値、終了フラグを取得
        reward, done = self.reward_func(next_state)
        return next_state, reward, done
