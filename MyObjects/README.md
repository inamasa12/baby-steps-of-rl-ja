# Memo

## Day1

### 強化学習 Tips  
* マルコフ決定過程（Markov Decision Process: MDP）  
強化学習では前提とされている  
遷移先の状態は直前の状態と、そこでの行動のみに依存して決定する  
状態、行動、状態遷移確率、即時報酬の4つの構成要素で表現できる  
⇒ **これらを上手く定義、学習させていくのが強化学習プロセス**  

### Python Tips
`__hash__`:  
当該オブジェクトのハッシュ値を生成する関数（特殊メソッド）  
`@property`:  
オブジェクトが保有する非公開変数値を取得する関数  

### 参考サイト
[Python における hashable](https://qiita.com/yoichi22/items/ebf6ab3c6de26ddcc09a)  

## Day2

### 強化学習 Tips  

学習プロセスを通じてエージェントに各状態の価値を認識させる  
価値定義はベルマン方程式に基づく  
状態価値を戦略の期待値で定義するものと、選択可能な行動の最大価値で定義するものがある  

　<img src="https://latex.codecogs.com/gif.latex?V_{\pi}\left&space;(&space;s&space;\right&space;)=\sum_{a}\pi\left&space;(&space;a&space;\mid&space;s&space;\right&space;)\sum_{s'}T\left&space;(&space;s'&space;\mid&space;s,&space;a\right&space;)\left&space;(&space;R\left&space;(&space;s,&space;s'&space;\right&space;)&plus;\gamma&space;V_{\pi}\left&space;(&space;s'&space;\right&space;)&space;\right&space;)">  
　<img src="https://latex.codecogs.com/gif.latex?V\left&space;(&space;s&space;\right&space;)={max}_{a}\sum_{s'}T\left&space;(&space;s'&space;\mid&space;s,&space;a\right&space;)\left&space;(&space;R\left&space;(&space;s,&space;s'&space;\right&space;)&plus;\gamma&space;V_{\pi}\left&space;(&space;s'&space;\right&space;)&space;\right&space;)">  


* 学習方法  
  * モデルベース  
  動的計画法（Dynamic Programming: DP）とも呼ぶ  
  状態遷移確率、即時報酬が事前に定義可能な場合に用いる  
  シミュレーションが不要で全ての状態価値を繰り返し計算で求める  
  仮置きした状態価値を繰り返し計算で更新していく  
    * Policy Iteration  
    状態価値を戦略の期待値で更新  
    状態価値の更新に併せて、価値が最大の行動を選択するように戦略を更新していく必要がある  
    * Value Iteration  
    状態価値を選択可能な行動の最大価値で更新  
  * モデルフリー  
  シミュレーションを通じて状態価値を更新していく  
  

## Day3

### 強化学習 Tips  

モデルフリーの学習  
* シミュレーションの方法  
Epsilon-Greedy法: 
 探索と活用のトレードオフ  
 シミュレーションで、多様な状態に関する経験を蓄積するための行動と、正しい行動を学習するための最適化行動をブレンドして行う方法  
* 各状態価値の学習方法  
既存の各状態における各行動の価値をシミュレーションの結果得られた報酬で更新していく  
両者の差分に学習率を乗じた値を既存の状態価値に加算していく  
加算値が閾値を下回った時点で学習を終了させる  
  * モンテカルロ法（Monte Carlo Methods）  
  エピソードを最後まで実行した結果、得られた報酬の現在価値  
  一つのエピソード結果の影響が大きくなる  
  * TD法（Temporal Difference Learning）
  λステップ先の状態価値とそこまでに得られた報酬の現在価値  
  目標値に仮置きの状態価値が含まれる  
  ⇒ 両者の折衷案としてMulti-step Learningがある  
モデルベース同様にPolicyベースとValueベースがある
  * On Policy  
  モデルベースのPolicy Iterationに相当  
  翌期の状態価値は戦略が選択する行動の価値
  SARSAが相当  
  Qテーブルを用いる場合は価値が最大の行動を選択する戦略となるため、戦略と価値評価は一体となる  
  Epsilon-Greedy法で戦略にランダム要素を含めるのが一般的  
  戦略を行動選択確率で表す場合等、戦略と価値評価は分離して定義することが可能  
  戦略担当をActor、価値評価担当をCriticとして定義 ⇒ Actor Critic法  
  * Off Policy  
  モデルベースのValue Iterationに相当  
  翌期の状態価値は最大の行動価値  
  Q-Learningが相当  


## Day4

### 強化学習 Tips  

ニューラルネットワークで価値評価を行う  
Deep Q Networkが相当  
* Value Function Approximation  
インプットを状態、アウトプットを各行動の価値とするニューラルネットワークモデル  
教師データを報酬と翌期の状態から推定した行動価値の最大値を割引いた金額の合計額とする
* Policy Gradient（方策勾配法）  
状態別に各行動の選択確率を出力するモデル  
出力する各行動の選択確率に基づく下記の戦略の期待値が最大となるようにパラメータを学習  
  
  　<img src="https://latex.codecogs.com/gif.latex?E_{\pi&space;_{\theta&space;}}\left&space;[&space;log\pi&space;_{\theta&space;}\left&space;(&space;a|s&space;\right&space;)Q^{\pi&space;_{\theta&space;}}\left&space;(&space;s,a&space;\right&space;)&space;\right&space;]" title="E_{\pi _{\theta }}\left [ log\pi _{\theta }\left ( a|s \right )Q^{\pi _{\theta }}\left ( s,a \right ) \right ]" />  
行動価値Qを別のモデルで計算する場合 ⇒ Actor Critic  
行動価値と状態価値の差分で価値を表現する場合 ⇒ Advantage  
  * A2CとA3C  
  ともにActor CriticとAdvantageを使用  
  A3Cは学習を分散させて（Asynchronous）、定期的に結果を集約する  
  
学習安定化の工夫  
* Experience Replay  
蓄積した経験からサンプリングして学習データを作成する  
学習データの偏りを防ぐ  
* Fixed Target Q-Network  
別途用意した価値推定用のニューラルネットワークモデルで翌期の状態における行動価値を推定する  
価値推定用のモデルは一定期間経過後に学習モデルに同期される  
一定期間固定したパラメータで価値推定を行うことで学習の安定化を図る  
* 報酬のClipping  
報酬額を規格化し、学習結果を安定させる  
* Raibow  
Deep Mindによる強化学習モデル  
7つの工夫を組み込む（DQNと6つの工夫）  
  1. Double DQN  
  通常のDQNでは価値が最大の行動をとることを前提に価値推定を行うため、価値を過大推定してしまう  
  価値推定用のモデルを別途用意し、メインのモデルは行動選択のみ行う  
  Fixed Target Q-Networkと同じ考え方  
  1. Prioritized Replay  
  TD誤差が大きいデータを優先的にサンプリングして学習に用いる方法  
  1. Dueling Network  
  状態だけに依存する価値と行動だけに依存する価値の合計で各行動の価値を評価するモデル  
  状態だけで決まる価値を推定する部分の学習が高速化、安定する  
  1. Multi-step Learning  
  TD法と同義  
  1. Distributional RL  
  報酬を期待値だけではなく、分布として扱う  
  例えば、報酬のばらつきを考慮して行動選択をモデリングする  
  1. Noisy Nets  
  ニューラルネットワークの重みとバイアスにランダム要素を加えて探索領域の拡張を試みるもの  

次に戦略をニューラルネットワークで表現する  
最適化では価値の期待値を最大化するように行動確率を更新する  
　  
　<img src="https://latex.codecogs.com/gif.latex?V_{\pi}\left(s\right)&space;=\sum_{a}\pi\left(a|s\right)\sum_{s'}T\left(s'|s,a\right)\left(R\left(s,s'\right)&plus;\gamma&space;V_{\pi}\left(s'\right)&space;\right&space;)\right)" title="V_{\pi}\left(s\right) =\sum_{a}\pi\left(a|s\right)\sum_{s'}T\left(s'|s,a\right)\left(R\left(s,s'\right)+\gamma V_{\pi}\left(s'\right) \right )\right)" />  
 
 
