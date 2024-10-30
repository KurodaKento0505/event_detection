import pandas as pd
import argparse
import os
import json
import cv2

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_id')
    parser.add_argument('--num_class')
    return parser.parse_args()

def display_label(frame, label):
    # 画面上にラベルを表示する
    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def test_json(video_path, events_df, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    max_frames = fps * 120  # 最初の2分間（120秒間）のフレーム数
    # 動画保存の設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    current_frame = 0
    annotation_num = 0
    label_display_frames = {}
    annotations = events_df['annotations']

    while cap.isOpened() and current_frame < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # 現在のフレーム番号に一致するアノテーションを確認
        annotation = annotations[annotation_num]
        position = int(annotation['position'])
        if current_frame == position:
            label = annotation['label']
            # ラベルを表示するフレーム範囲を設定（現在のフレームから5フレーム）
            label_display_frames[position] = (label, current_frame + 5)

            # フレームにラベルを描画
            for pos, (label, end_frame) in list(label_display_frames.items()):
                if current_frame <= end_frame:
                    display_label(frame, label)
                else:
                    del label_display_frames[pos]  # 5フレームを超えたラベルは削除
            annotation_num += 1

        out.write(frame)
        current_frame += 1

    out.release()
    cap.release()

if __name__ == '__main__':
    # 使用例
    args = parse_arguments()
    match_ids = [str(match_id) for match_id in args.match_id.split(",")]
    num_class = str(args.num_class)
    for match_id in match_ids:
        video_path = f'data/{match_id}/{match_id}.mp4'
        json_path = f'data/{match_id}/{match_id}_{num_class}_class_events.json'
        output_path = f'data/{match_id}/{match_id}_label.mp4'
        with open(json_path, 'r') as f:
            events_df = json.load(f)
        test_json(video_path, events_df, output_path)