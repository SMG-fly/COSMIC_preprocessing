import pandas as pd
import sys

def filter_cosmic_data(input_file, output_file):
    # CSV 파일 읽기
    df = pd.read_csv(input_file, sep="\t")
    
    # 필터링 조건 적용
    filtered_df = df[
        (df["POSITIVE_SCREEN"] == "y") &
        (df["MUTATION_SOMATIC_STATUS"] != "Variant of unknown origin")
    ]
    
    # 필터링된 데이터 저장
    filtered_df.to_csv(output_file, sep="\t", index=False)
    print(f"Filtered data has been saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_cosmic.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1] # 0.Cosmic_v100_GRCh38.tsv
        output_file = sys.argv[2] # 1.filtering.tsv
        filter_cosmic_data(input_file, output_file)
