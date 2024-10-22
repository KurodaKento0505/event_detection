# Event Detection

## プロジェクト概要
サッカーの試合映像もしくはトラッキングデータからイベントを検出

### 目的
- playboxに自動タグ付け機能を付けるための技術検証
- フルピッチ動画に対してイベントを検出する精度を調査
- 追加でデータを増やしたら精度があがるのか、どのくらいデータがあればいいのかを調査

### 検出するイベント
<details>
<summary>12 class (ball action spotting)</summary>

Pass, Drive, Header, High Pass, Out, Cross, Throw In, Shot, Ball Player Block, Player Successful Tackle, Free Kick, Goal
</details>
<details>
<summary>8 class (ball action spotting)</summary>

Header, Cross, Throw In, Shot, Free Kick, Goal, Corner Kick, Goal Kick
</details>

### 手法概要
- 映像から
    - ball action spotting 2024のベースラインを使用
- トラッキングデータから

### 具体的な手法


## プロジェクト構造
```
event_detection/
├── data/             # ここにjsonファイルを格納
│   ├── 117092/
│   ├── ...
│   ├── 132877/
│   └── event_frequency.csv
├── tools_detection/
│   ├── load_csv.py
│   └── make_json.py
├── .gitignore
└── README.md
```

## event detection

## 注意点