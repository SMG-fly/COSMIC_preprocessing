import sys
import re

def filter_tsv_by_hgvsc(input_tsv, output_tsv):
    # 정규 표현식: HGVSC=ENST00000378288.8:c.337C>T
    pattern = re.compile(r'ENST\d+\.\d+:c\.\d+[ATCG]?>[ATCG]?')

    with open(input_tsv, 'r') as infile, open(output_tsv, 'w') as outfile:
        for idx, line in enumerate(infile):
            # 첫 행(헤더)은 무조건 출력
            if idx == 0:
                outfile.write(line)
            else:
                # HGVSC 형식에 맞는 변이가 있는 행만 출력
                if pattern.search(line):
                    outfile.write(line)

if __name__ == "__main__":
    # 명령줄에서 입력 및 출력 파일 받기
    if len(sys.argv) != 3:
        print("사용법: python script.py input.tsv output.tsv")
        sys.exit(1)
    
    input_tsv = sys.argv[1] #TP2.filtering2.tsv
    output_tsv = sys.argv[2]
    
    filter_tsv_by_hgvsc(input_tsv, output_tsv)
