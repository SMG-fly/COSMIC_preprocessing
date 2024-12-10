import sys

def process_file(input_file, output_file):
    # 고유 ID 카운트를 위한 딕셔너리
    id_counts = {}

    # 입력 파일 읽기 및 출력 파일 쓰기
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # 각 라인을 탭으로 분리
            parts = line.strip().split('\t')
            original_id = parts[2]  # 세 번째 열의 ID 가져오기

            # ID에 대한 고유 번호 증가
            if original_id in id_counts:
                id_counts[original_id] += 1
            else:
                id_counts[original_id] = 1

            # 고유 번호를 추가한 ID 생성
            parts[2] = f"{original_id}_{id_counts[original_id]}"

            # 변경된 행을 출력 파일에 기록
            outfile.write('\t'.join(parts) + '\n')

    print(f"Processed file saved to {output_file}")

if __name__ == "__main__":
    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    # 입력 및 출력 파일 경로 받기
    input_file = sys.argv[1] # M1.final_filtering.vcf
    output_file = sys.argv[2] # M2.final_filtering_divide_IDs.vcf

    # 파일 처리 실행
    process_file(input_file, output_file)
