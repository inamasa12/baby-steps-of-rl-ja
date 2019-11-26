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

次にニューラルネットワークで戦略を表現するケース  
最適化では価値の期待値を最大化するように行動確率を更新する  
　  
　<img src="https://latex.codecogs.com/gif.latex?J\left&space;(&space;\theta&space;\right&space;)\propto&space;\sum_{s\in&space;S}d^{\pi_{\theta&space;}}\left&space;(&space;s&space;\right&space;)\sum_{a\in&space;A}\pi_{\theta&space;}\left&space;(&space;a|s&space;\right&space;)Q^{\pi_{\theta&space;}}\left&space;(&space;s,a&space;\right&space;)" title="J\left ( \theta \right )\propto \sum_{s\in S}d^{\pi_{\theta }}\left ( s \right )\sum_{a\in A}\pi_{\theta }\left ( a|s \right )Q^{\pi_{\theta }}\left ( s,a \right )" />  
 
 ここで行動価値ではなく、状態価値を引いたAdvantageを用いることがある  
 　  
 　<img src="https://latex.codecogs.com/gif.latex?A\left&space;(&space;s,a&space;\right&space;)=Q_{w}\left&space;(&space;s,a&space;\right&space;)&space;-&space;V_{v}\left&space;(&space;s&space;\right&space;)" title="A\left ( s,a \right )=Q_{w}\left ( s,a \right ) - V_{v}\left ( s \right )" />  

* Advantage Actor Critic (A2c)  
Actor criticにおける状態価値の評価をAdvantageの評価に置き換える  
分散環境で並列的に経験を収集する手法も含む  
* DDPG (Deep Deterministic Policy Gradient)  
各行動の選択確率ではなく、行動自体を出力するモデル  
連続的な行動を表現できる  
学習にはTD誤差を使用  
Fixed Target Q-Networkを使用  
* Trust Region Policy Optimization (TRPO)  
更新で戦略が大きく振動するのを回避しながら（KL距離の制約）学習を行う方法  
特にクリッピングしたKL距離を最適化目的関数に含めたモデルをProximal Policy Optimaization (PPO)と呼ぶ  

||Valueベース|Policyベース|
|:--|:--:|:--:|
|長所|シンプル|連続的な行動を表現できる <br> 選択する行動が偏りにくい <br> 学習が早い|
|短所|離散的な行動に限定 <br> 選択する行動がどちらかに偏りやすい|過学習しやすい|


## Day5

### 強化学習 Tips

強化学習の弱点  
1. サンプル効率が悪い  
学習に大量のデータと時間を要する  
1. 局所最適、過学習  
1. 再現性が低い  
学習過程にランダム性があるため、同じパラメータ設定でも結果が異なる  
パラメータに結果が敏感  

上記の対応策  
1. テスト可能なモジュールに切り分ける  
バグの発生を前提とし、障害発生時の時間的なロスを回避する  
1. 可能な限りログを取る  
一度の学習プロセスから最大限の情報を得る  
1. 学習の自動化  
スクリプト化、パラメータの記録  
1. 公開された検証済みのアルゴリズムを活用する  

## Day6  
### 強化学習 Tips  
サンプル効率が悪い点（学習に多くのデータが必要）への対応  
大きく分けて、モデルに工夫を施すケースとデータに工夫を施すケースがある  

### モデルに工夫を施す  
更に、学習能力、転移能力及び転移学習の2つの観点に分けられる  

#### 学習能力  
与えられたデータから効率的に学習する能力  
エージェントモデル自体の工夫、データのサンプリングや最適化手法の工夫等が含まれる  

#### 転移能力  
何らかの学習経験を用いて、より短時間で学習させる  
* 学習のさせ方を学習する
エージェントモデルへのフィードバッグ（勾配）を学習させる ⇒ Learning to Optimize  
学習データへのラベル付けを学習させる ⇒ Active Learning  
* 学習の仕方を学習する  
よい初期値を学習させる ⇒ MAML  

#### 転移学習
あるタスクで学習させたモデルを別のタスクで再利用する  
移転前後のタスクが確定している場合を「ドメイン変換」と呼ぶ  

### データに工夫を施す
環境認識、探索行動、外部からの教示の3つの観点に分けられる  
  
#### 環境認識の改善  
エージェントモデルが学習しやすいように、環境（状態、報酬）を加工する    
* モデルベース    
環境自体をモデル化する  
モデルフリーの学習に対して、推定したモデル（遷移確率、報酬関数）による学習（モデルベース）を追加的に行う  
環境モデルの構築方法は様々  
1. サンプルベース  
Sample Based Planning Model: モデルの学習が終了した後に、そのモデルでモデルベースの学習  
Dyna: モデルフリーの学習を行いながら、モデルの学習とそれを使用したモデルベースの学習を平行して行う  
1. シミュレーションベース  
構築したモデルで将来の状態をシミュレーションし、その情報に基づき学習を行う  
モンテカルロ木探索: 到達回数が多い状態につき、その先から最後までのステップの情報を用いて学習を行う  
TD Search: モンテカルロ木探索につき、最後に至る前までの情報で学習を行う方法  
* 表現学習  
状態の特徴量を抽出する試み  
Word Modelsは、画像情報を圧縮するVAEと特徴量を抽出するRNNの組み合わせで表現学習を行っている  
表現学習のモデル、方法は様々  

#### 探索行動の改善  
より学習効果の高いサンプル（未知の経験）を獲得できるようにする  
* 内発的報酬、内発的動機付け  
環境に大きな変化をもたらす行動に報酬を与える  
* ランダムな試行回数の調整  
NoisyNetなど  

#### 外部からの教示  
エージェントの探索活動だけではなく、外部から望ましい学習データを与える  
* カリキュラムラーニング  
簡単なタスクから難しいタスクに移行する  
タスクを分割する  
⇒ カリキュラム自体を自動で作成する方向  

再現性の低さへの対応  
勾配法とは異なる学習アプローチ  
CPUでの処理が速くなる  
1. 進化戦略  
複数のパラメータでエピソードを実行し、評価の高いパラメータに近いものを選択していく  
1. 遺伝的アルゴリズム  
同様に、評価の高いパラメータを合成する（交叉）、パラメータに乱数を加える（突然変異）等の操作を行う  










### Python Tips  
* defaultdict  
指定したキーが存在しない場合に、初期化時の関数が実行され、値として設定される辞書  
下記で初期化した辞書について、存在しないキーの値を呼ぶと`0`が入る  
~~~ruby  
d = defaultdict(0)  
print(d[x])
~~~  
~~~ruby  
0
~~~  
* Counter  
要素をキー、出現回数を値とした辞書を作成  
~~~ruby  
c = Counter(['a', 'a', 'a', 'b', 'b', 'c'])  
print(c)
~~~  
~~~ruby  
Counter({'a': 3, 'c': 2, 'b': 1})
~~~  



