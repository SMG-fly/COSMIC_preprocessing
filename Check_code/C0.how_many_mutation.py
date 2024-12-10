import pandas as pd
import sys

# 파일 경로 설정
file_path = sys.argv[1]  # 예: 'Cosmic_CompleteTargetedScreensMutant.tsv'

# 고유한 3번째 열 값들을 저장할 set 생성
unique_values = set()
chunk_size = 100000  # 한 번에 읽을 행 수 설정

# 파일을 chunk 단위로 읽고, '#'으로 시작하는 행은 건너뜀
for chunk in pd.read_csv(file_path, sep='\t', chunksize=chunk_size, comment='#', header=None):
    # 3번째 열(COSMIC ID)에서 고유 값을 추출
    for val in chunk.iloc[:, 2].dropna().astype(str):  # NaN 값 제거 및 문자열 변환
        COSMIC_ID = val.split('_')[0]  # '_'로 분리 후 첫 번째 값 추출
        unique_values.add(COSMIC_ID)

# 총 고유 값 개수 출력
print(f"총 고유 값의 종류: {len(unique_values)}")
