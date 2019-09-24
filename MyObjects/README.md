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
価値定義はベルマン方程式に基づく（状態価値を戦略の期待値で定義するものと、選択可能な行動の最大価値で定義するものがある）  

　<img src="https://latex.codecogs.com/gif.latex?V_{\pi}\left&space;(&space;s&space;\right&space;)=\sum_{a}\pi\left&space;(&space;a&space;\mid&space;s&space;\right&space;)\sum_{s'}T\left&space;(&space;s'&space;\mid&space;s,&space;a\right&space;)\left&space;(&space;R\left&space;(&space;s,&space;s'&space;\right&space;)&plus;\gamma&space;V_{\pi}\left&space;(&space;s'&space;\right&space;)&space;\right&space;)">  
　<img src="https://latex.codecogs.com/gif.latex?V\left&space;(&space;s&space;\right&space;)={max}_{a}\sum_{s'}T\left&space;(&space;s'&space;\mid&space;s,&space;a\right&space;)\left&space;(&space;R\left&space;(&space;s,&space;s'&space;\right&space;)&plus;\gamma&space;V_{\pi}\left&space;(&space;s'&space;\right&space;)&space;\right&space;)">  


* 学習方法  
  * モデルベース  
  動的計画法（Dynamic Programming: DP）とも呼ぶ  
  状態遷移確率、即時報酬が事前に定義可能な場合に用いる  
  シミュレーションが不要で全ての状態価値を繰り返し計算で求める  
  仮置きした状態価値を繰り返し計算で更新していく  
  * モデルフリー  





