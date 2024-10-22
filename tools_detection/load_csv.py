import pandas as pd
import argparse
import os
from collections import Counter

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_id')
    return parser.parse_args()

def load_csv_to_variable(raw_data_path, match_id):

    # Read the event data
    event_path = os.path.join(raw_data_path, match_id, f'{match_id}_player_nodes.csv')
    event_df = pd.read_csv(event_path)
    # 'event_types'列の値を取得
    event_types = event_df['event_types']

    # イベントのカウント用リスト
    event_list = []
    # 各行の最初の空白スペースまでの文字列を取得してリストに追加
    for event in event_types:
        if pd.notna(event):  # NaNを避けるためのチェック
            first_word = event.split(' ')[0]  # 空白で分割して最初の要素を取得
            event_list.append(first_word)

    return event_list

if __name__ == '__main__':
    # 使用例
    args = parse_arguments()
    match_ids = [str(match_id) for match_id in args.match_id.split(",")]
    raw_data_path = 'data'
    output_csv_path = 'data/event_frequency.csv'
    all_event_list = []
    for match_id in match_ids:
        event_list = load_csv_to_variable(raw_data_path, match_id)
        all_event_list.extend(event_list)
    # 各イベントの出現回数をカウント
    all_event_counts = Counter(all_event_list)
    # 出現頻度が高い順にソート
    sorted_event_counts = sorted(all_event_counts.items(), key=lambda x: x[1], reverse=True)
    # データフレームに変換
    df = pd.DataFrame(sorted_event_counts, columns=['Event', 'Frequency'])
    # CSVファイルに保存
    df.to_csv(output_csv_path, index=False)
