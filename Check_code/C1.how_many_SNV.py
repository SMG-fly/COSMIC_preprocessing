import pandas as pd
import sys

# 실제 파일 경로 설정
file_path = sys.argv[1] #'Cosmic_CompleteTargetedScreensMutant.tsv'

# SO_TERM이 'SNV'인 행의 개수를 세기
snv_count = 0
chunk_size = 100000  # 한 번에 읽을 행 수 설정

# 파일을 chunk 단위로 읽으면서, '#'으로 시작하는 주석 행을 건너뛰고, 8번째 열에서 SO_TERM=SNV 조건 확인
for chunk in pd.read_csv(file_path, sep='\t', comment='#', header=None, chunksize=chunk_size):
    # 8번째 열에서 'SO_TERM=SNV' 문자열이 포함된 행 필터링
    snv_count += chunk[7].str.contains(r'SO_TERM=SNV').sum()

# 결과 출력
print(f"SO_TERM이 'SNV'인 행의 개수: {snv_count}")
