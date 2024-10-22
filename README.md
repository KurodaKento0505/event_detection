# Event Detection

## プロジェクト概要
サッカーの試合映像もしくはトラッキングデータからイベントを検出

### 目的
- playboxに自動タグ付け機能を付けるための技術検証
- フルピッチ動画に対してイベントを検出する精度を調査
- 追加でデータを増やしたら精度があがるのか、どのくらいデータがあればいいのかを調査

### 検出するイベント
<details>
<summary>12クラス（ball action spotting）</summary>


</details>
    - 
- 8クラス（play box）

### 手法概要
- 選手の画像上の座標を獲得
    - セグメンテーションすることで正確な位置座標の取得
- ピッチ座標に変換（ここではやらない）

### 具体的な手法
1. YOLOv10をファインチューニング
1. SAM2をファインチューニング
1. ファインチューニング済みのYOLOv10を用いて，最初のフレームからbboxを獲得
1. ファインチューニング済みのSAM2に最初のフレームのbboxをプロンプトとして付与
1. SAM2を用いてセグメンテーション
1. 得られたマスクから画像上の位置を推定（まだここまでできていない）

## プロジェクト構造
```
basketball/
├── basketball-video-dataset/             # ここに動画を格納
├── player_detection/
│   ├── fine_tuned_yolo/                  # ファインチューニング済みのモデルを格納
│   ├── predict_frame/                    # 予測した画像が格納
│   └── tools_detection/
│       ├── change_file_name.py
│       ├── check_annotation.py
│       ├── convert_bbox_label.py
│       ├── fine_tuning_yolo.py           # main file（ファインチューニング）
│       ├── inference_yolo.py             # main file（モデルの推論）
│       └── make_bbox.py
├── player_segmentation/
│   ├── sam2/ ...                         # sam2を動かすのに必要なファイル
│   ├── fine_tuned_sam2/                  # ファインチューニング済みのモデルを格納
│   ├── predict_frame/                    # 予測した画像が格納
│   ├── predict_video/                    # 予測した画像が格納
│   └── tools_segmentation/
│       ├── evaluate_sam2.py
│       ├── fine_tuning_sam.py
│       ├── fine_tuning_sam2.py           # main file（ファインチューニング）
│       ├── gen_annotations.py
│       ├── gen_errorbar_graph.py
│       ├── inference_sam.py
│       ├── inference_sam2_with_video.py  # main file（モデルの推論）
│       ├── inference_sam2.py             # main file（モデルの推論）
│       └── make_mask.py
├── player_tracking/
│   ├── sam2/ ...                         # sam2を動かすのに必要なファイル
│   ├── predict_frame_sam2/               # 予測した画像が格納
│   ├── predict_frame_yolo/               # 予測した画像が格納
│   ├── predict_video/                    # 予測した画像が格納
│   └── tools_tracking/
│       ├── make_video.py
│       ├── modify_tracking_id.py
│       ├── tracking_player_sam2.py       # main file（動画に対してマスクを与え続ける）
│       └── tracking_player_yolo.py       # main file（動画に対してbboxを与え続ける）
├── .gitignore
└── README.md
```


### ドキュメンテーション

#### READMEはしっかり書きましょう！
環境構築の手順やコードの実行方法は最低限記載してください。手法の説明や関連リンク（Notionのリンクでも構いません）があると助かります。

#### Docstringは分かる程度で大丈夫です！
Docstringは一行程度で構いません。型ヒントも好みで大丈夫です。私自身、これに力を入れすぎて開発速度が落ちた経験が多々ありますので、プロダクション用のコード（Playbox上で動く本番用のコード）でない限り、メンテナンスが面倒になるので適当で大丈夫です。

### 大きいファイル（データセット・モデル）の置き場所

**playbox-server-1**で開発を行う場合、可能な限り`/home/share/data`にファイルを配置し、シンボリックリンク（symlink）を作成してください。例えば、`ball_detection`プロジェクトの場合、ディレクトリ構造は以下のようになるかもしれません：

```
/home/share/data
├── ball_detection
│   ├── data
│   │   ├── external       # 外部ソースからのデータ
│   │   ├── interim        # 変換中間データ
│   │   ├── processed      # モデリング用の最終データセット
│   │   └── raw            # 元の不変データ
│   ├── weights
│   ├── outputs
```

このようにディレクトリを構築し、シンボリックリンクを作成することで、プロジェクト内でのデータ管理が容易になります。ただし、共有場所となるため、不必要なファイルを増やさないよう注意してください。


### その他、意識してほしいこと

#### なるべく[Python 3.9 以上](https://www.python.org/downloads/)を使う

Pythonのバージョンは、できるだけ新しいものを使用してください。
2024年末には3.8のサポートが終了し、2025年10月には3.9のサポートも終了する予定です。
詳細は[Status of Python versions](https://devguide.python.org/versions/)を参照してください。

#### なるべく[uv](https://astral.sh/blog/uv) を使う
可能な限り[uv](https://astral.sh/blog/uv)を使用してください。既存のコードベースがPoetryやcondaを使用しており、uvへの移行が難しい場合はそのままでも構いませんが、何らかの方法でパッケージを管理するようにしてください。これにより、[It works on my machine](https://dylanbeattie.net/2017/04/27/it-works-on-my-machine.html)問題を防ぐことができます。

#### アトムがコードを実行してツイートできるようにする
Playboxの機械学習コードは、画像や映像を入力し、可視化された結果を出力することが多いです。
ツイート可能にすることは、単に動作するだけでなく、環境構築が整い、再現性のあるコードベースと最低限のドキュメンテーションがあることを示しています。
