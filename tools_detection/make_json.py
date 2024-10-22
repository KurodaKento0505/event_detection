import pandas as pd
import argparse
import os
from collections import Counter
import json

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_id')
    parser.add_argument('--num_class')
    return parser.parse_args()

def make_json(raw_data_path, translate_event_df, num_class, match_id):

    # Read the event data
    event_path = os.path.join(raw_data_path, match_id, f'{match_id}_player_nodes.csv')
    event_df = pd.read_csv(event_path)
    output_json_path = os.path.join(raw_data_path, match_id, f'{match_id}_{num_class}_class_events.json')

    # JSONデータの基本構造
    json_data = {
        "UrlLocal": "",
        "UrlYoutube": "",
        "annotations": []
    }

    # event_df の各行に対して処理を行う
    for _, row in event_df.iterrows():
        event_type = row['event_types']  # event_typeを取得
        event_time = row['event_time']  # event_timeを取得
        event_period = row['event_period']  # event_periodを取得 (FIRST_HALF, SECOND_HALF)

        # translate_event_df から対応するイベントを探す
        matched_event = translate_event_df[translate_event_df['Event'] == str(event_type).split(' ')[0]]

        if (not matched_event.empty) and (matched_event[num_class + '_class_event'] != 'Nan').any().any():
            # 12_class_event列の値を取得
            label = matched_event[num_class + '_class_event'].values[0]

            # event_time を秒に変換し、分:秒形式に変換
            total_seconds = event_time / 1000
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)

            # "gameTime" の形式を "1 - 分:秒" または "2 - 分:秒" に変換
            if event_period == "FIRST_HALF":
                game_time = f"1 - {minutes}:{seconds:02d}"
            elif event_period == "SECOND_HALF":
                game_time = f"2 - {minutes}:{seconds:02d}"
            else:
                game_time = f"{minutes}:{seconds:02d}"  # 不明な場合は分:秒形式

            # 新しいイベントのJSONエントリを作成
            annotation = {
                "gameTime": game_time,  # ゲーム時間を設定 (形式を変換済み)
                "label": label,         # ラベルを設定
                "position": str(event_time),  # positionには元のevent_timeを格納
                "team": "",             # teamは空
                "visibility": ""        # visibilityは空
            }

            # annotationsに追加
            json_data["annotations"].append(annotation)

    # JSONファイルに書き込み
    with open(output_json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"JSONファイルを作成しました: {output_json_path}")

if __name__ == '__main__':
    # 使用例
    args = parse_arguments()
    match_ids = [str(match_id) for match_id in args.match_id.split(",")]
    num_class = str(args.num_class)
    raw_data_path = 'data'
    translate_csv_path = 'data/event_frequency.csv'
    translate_event_df = pd.read_csv(translate_csv_path)
    for match_id in match_ids:
        event_list = make_json(raw_data_path, translate_event_df, num_class, match_id)