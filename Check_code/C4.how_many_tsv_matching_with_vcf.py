import pandas as pd
import sys

# argv로 파일 경로 받기
if len(sys.argv) != 3:
    print("Usage: python script.py <tsv_file> <vcf_file>")
    sys.exit()

tsv_file = sys.argv[1]
vcf_file = sys.argv[2]

# TSV 파일 읽기
tsv_data = pd.read_csv(tsv_file, sep="\t")

# VCF 파일 읽기
vcf_data = pd.read_csv(vcf_file, sep="\t", comment='#', header=None)
vcf_data.columns = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]

# VCF의 ID에서 "_" 앞부분만 추출
vcf_data["ID_cleaned"] = vcf_data["ID"].str.split("_").str[0]

# ID 열 추출 (겹치는 기준)
tsv_ids = set(tsv_data["GENOMIC_MUTATION_ID"])
vcf_ids = set(vcf_data["ID_cleaned"])

# 교집합(겹치는 ID)
common_ids = tsv_ids & vcf_ids

# TSV에만 있는 ID
tsv_only_ids = tsv_ids - vcf_ids

# VCF에만 있는 ID
vcf_only_ids = vcf_ids - tsv_ids

# 결과 출력
print(f"겹치는 ID 개수: {len(common_ids)}")
print(f"TSV 파일에만 있는 ID 개수: {len(tsv_only_ids)}")
print(f"VCF 파일에만 있는 ID 개수: {len(vcf_only_ids)}")

# 교집합, TSV만, VCF만 데이터 저장
'''
common_data = tsv_data[tsv_data["GENOMIC_MUTATION_ID"].isin(common_ids)]
tsv_only_data = tsv_data[tsv_data["GENOMIC_MUTATION_ID"].isin(tsv_only_ids)]
vcf_only_data = vcf_data[vcf_data["ID_cleaned"].isin(vcf_only_ids)]

common_data.to_csv("common_ids.tsv", sep="\t", index=False)
tsv_only_data.to_csv("tsv_only_ids.tsv", sep="\t", index=False)
vcf_only_data.to_csv("vcf_only_ids.tsv", sep="\t", index=False)
print("결과가 'common_ids.tsv', 'tsv_only_ids.tsv', 'vcf_only_ids.tsv'에 저장되었습니다.")
'''