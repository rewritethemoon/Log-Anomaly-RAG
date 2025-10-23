# src/data_preprocess.py
import pandas as pd
from pathlib import Path
from datetime import datetime

def parse_bgl_log_correct(input_path: str, output_path: str, max_lines: int = None):
    """
    Parse BGL.log đúng thứ tự cột:
    Label | UnixTS | Date | Node | Timestamp | NodeRepeat | Component | Level | Severity | Message
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = []
    skipped = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line_num, line in enumerate(f, 1):
            if max_lines and line_num > max_lines:
                break
            line = line.strip()
            if not line:
                continue

            # Tách bằng khoảng trắng, tối đa 9 phần → message là phần còn lại
            parts = line.split(None, 9)
            if len(parts) < 9:
                skipped += 1
                continue

            # Gán đúng thứ tự
            label = parts[0]
            unix_ts = parts[1]           # 1117838570
            date_str = parts[2]          # 2005.06.03
            node = parts[3]              # R02-M1-N0-C:J12-U11
            timestamp_str = parts[4]     # 2005-06-03-15.42.50.363779
            node_repeat = parts[5]
            component = parts[6]
            level = parts[7]
            severity = parts[8]
            message = parts[9] if len(parts) > 9 else ""

            # Parse Timestamp (chuỗi có microsecond)
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d-%H.%M.%S.%f')
            except ValueError:
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d-%H.%M.%S')
                except:
                    timestamp = None

            # Optional: Chuyển Unix timestamp → datetime (để kiểm tra)
            try:
                unix_dt = datetime.fromtimestamp(int(unix_ts))
            except:
                unix_dt = None

            data.append([
                label, unix_ts, date_str, node, timestamp, node_repeat,
                component, level, severity, message
            ])

    # ĐÚNG CỘT
    columns = [
        'Label', 'UnixTimestamp', 'Date', 'Node', 'Timestamp',
        'NodeRepeat', 'Component', 'Level', 'Severity', 'Message'
    ]
    df = pd.DataFrame(data, columns=columns)

    # Lưu
    df.to_csv(output_path, index=False)
    print(f"Parsed {len(df):,} lines → {output_path}")
    print(f"Skipped {skipped} lines")
    print(f"Timestamp null: {df['Timestamp'].isnull().sum()}")
    print(f"Sample Labels: {df['Label'].unique()[:5]}")
    print(f"Sample Unix TS: {df['UnixTimestamp'].iloc[0]} → {datetime.fromtimestamp(int(df['UnixTimestamp'].iloc[0]))}")

    return df

# === CHẠY ===
if __name__ == "__main__":
    RAW_PATH = "data/raw/BGL.log"
    PROCESSED_PATH = "data/processed/BGL_structured.csv"
    
    df = parse_bgl_log_correct(RAW_PATH, PROCESSED_PATH, max_lines=100_000)
    print("\nSample:")
    print(df[['Label', 'Date', 'Timestamp', 'Severity', 'Message']].head(3))