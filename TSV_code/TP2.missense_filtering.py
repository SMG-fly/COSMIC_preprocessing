import pandas as pd
import sys

def filter_non_missense(input_file, output_file):
    # CSV 파일 읽기
    df = pd.read_csv(input_file, sep="\t", low_memory=False)
    
    # 필터링 조건 적용 (MUTATION_DESCRIPTION이 missense_variant가 아닌 경우)
    filtered_df = df[df["MUTATION_DESCRIPTION"] == "missense_variant"]
    
    # 필터링된 데이터 저장
    filtered_df.to_csv(output_file, sep="\t", index=False)
    print(f"Filtered data (excluding missense_variant) has been saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_non_missense.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        filter_non_missense(input_file, output_file)
