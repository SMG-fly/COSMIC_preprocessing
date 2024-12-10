import sys
import re

def filter_vcf_by_hgvsc(input_vcf, output_vcf):
    # 정규 표현식: HGVSC=ENST00000378288.8:c.337C>T
    pattern = re.compile(r'HGVSC=ENST\d+\.\d+:c\.\d+[ATCG]?>[ATCG]?')

    with open(input_vcf, 'r') as infile, open(output_vcf, 'w') as outfile:
        for line in infile:
            # VCF 파일의 주석(#로 시작하는 행)은 그대로 출력
            if line.startswith("#"):
                outfile.write(line)
            else:
                # HGVSC 형식에 맞는 변이가 있는 행만 출력
                if pattern.search(line):
                    outfile.write(line)

if __name__ == "__main__":
    # 명령줄에서 입력 및 출력 파일 받기
    if len(sys.argv) != 3:
        print("사용법: python script.py input.vcf output.vcf")
        sys.exit(1)
    
    input_vcf = sys.argv[1] # 1.SNV.vcf
    output_vcf = sys.argv[2]
    
    filter_vcf_by_hgvsc(input_vcf, output_vcf)
