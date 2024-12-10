import sys
import re
from Bio.Seq import Seq

# 인간 코돈 사용 빈도 테이블
CODON_FREQUENCY = {
    "TTT": 17.6, "TTC": 20.3, "TTA": 7.2, "TTG": 12.9,
    "CTT": 13.2, "CTC": 19.6, "CTA": 6.9, "CTG": 39.6,
    "ATT": 16.0, "ATC": 20.8, "ATA": 7.5, "ATG": 22.0,
    "GTT": 11.0, "GTC": 14.6, "GTA": 7.1, "GTG": 28.1,
    "TCT": 15.2, "TCC": 17.5, "TCA": 12.2, "TCG": 4.4,
    "AGT": 11.9, "AGC": 19.5, "CCT": 17.5, "CCC": 20.0,
    "CCA": 16.9, "CCG": 6.9, "ACT": 13.1, "ACC": 19.3,
    "ACA": 15.1, "ACG": 6.1, "GCT": 18.0, "GCC": 27.7,
    "GCA": 15.8, "GCG": 6.9, "TAT": 12.2, "TAC": 15.3,
    "TAA": 1.0, "TAG": 0.8, "CAT": 10.4, "CAC": 15.1,
    "CAA": 12.3, "CAG": 34.2, "AAT": 16.0, "AAC": 19.1,
    "AAA": 24.4, "AAG": 32.7, "GAT": 22.2, "GAC": 25.5,
    "TGT": 10.7, "TGC": 12.3, "TGA": 1.6, "TGG": 13.2,
    "CGT": 4.7, "CGC": 10.8, "CGA": 6.2, "CGG": 11.4,
    "AGA": 12.0, "AGG": 12.0, "GGT": 10.5, "GGC": 22.2,
    "GGA": 16.2, "GGG": 16.5
}


def calculate_codon_score(seq, frame):
    """
    코돈 사용 빈도를 기반으로 프레임의 점수 계산
    """
    score = 0
    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i:i+3]
        score += CODON_FREQUENCY.get(codon, 0)  # 빈도 데이터 없는 코돈은 0점
    return score

def find_best_frame_with_codon_usage(seq):
    """
    세 가지 프레임 중 가장 적합한 프레임 선택 및 번역.
    """
    scores = {}
    translations = {}
    for frame in range(3):
        protein_seq = str(Seq(seq[frame:]).translate())
        score = calculate_codon_score(seq, frame)
        scores[frame] = score
        translations[frame] = protein_seq
    
    # 가장 높은 점수의 프레임 선택
    best_frame = max(scores, key=scores.get)
    return translations[best_frame], best_frame

def apply_mutations_and_save_aa_sequence(fasta_file, vcf_file, output_file):
    # FASTA 파일을 transcript 기준으로 저장
    sequences = {}
    strand_info = {}
    with open(fasta_file, 'r') as f:
        current_transcript = ""
        current_seq = ""
        for line in f:
            if line.startswith(">"):
                if current_transcript:
                    sequences[current_transcript] = current_seq
                header_parts = line.strip().split()
                current_transcript = header_parts[1]
                strand_match = re.search(r"\(([\+\-])\)", line)
                strand_info[current_transcript] = strand_match.group(1) if strand_match else "?"
                current_seq = ""
            else:
                current_seq += line.strip()
        if current_transcript:
            sequences[current_transcript] = current_seq

    # VCF 파일을 읽고 각 변이에 대해 아미노산 서열 추출
    with open(vcf_file, 'r') as vcf, open(output_file, 'w') as out_f:
        out_f.write("Variant_ID\tMutated_AA_Sequence\tPosition_HGVSC\tPathogenicity\n")
        for line in vcf:
            fields = line.split("\t")
            variant_id = fields[2]
            transcript = fields[7].split(";")[1].split("=")[1]
            hgvsc_info = re.search(r'HGVSC=([\w.]+):c\.(\d+)([ATCG])>([ATCG])', fields[7])
            
            if hgvsc_info and transcript in sequences:
                hgvsc_position = hgvsc_info.group(0)  # HGVSC 정보 그대로 사용
                original_pos = int(hgvsc_info.group(2)) - 1  # 변이는 0-기반 인덱스로 처리
                ref = hgvsc_info.group(3)
                alt = hgvsc_info.group(4)
                
                # 해당 transcript의 시퀀스를 복제하여 변이 적용
                original_seq = sequences[transcript]
                strand = strand_info.get(transcript, "?")
                
                # N 개수 보정
                n_count_before_pos = original_seq[:original_pos].count("N")
                corrected_pos = original_pos + n_count_before_pos
                
                # HGVSC는 원래 서열 기준으로 처리
                if corrected_pos < len(original_seq) and original_seq[corrected_pos] == ref:
                    mutated_seq = original_seq[:corrected_pos] + alt + original_seq[corrected_pos+1:]
                    
                    # strand가 "-"일 경우 역상보 서열로 변환
                    if strand == "-":
                        # 역상보 전 위치 보정
                        aa_pos = (len(mutated_seq) - corrected_pos - 1) // 3
                        # 역상보 변환
                        mutated_seq = str(Seq(mutated_seq).reverse_complement())
                    else:
                        aa_pos = corrected_pos // 3
                    
                    # 가장 적합한 프레임 찾기
                    best_protein, best_frame = find_best_frame_with_codon_usage(mutated_seq)
                    
                    # 프레임 반영 위치 계산
                    aa_pos = (aa_pos + best_frame) // 3
                    
                    # `X` 제거
                    clean_protein = best_protein.replace("X", "")
                    
                    # 변이 위치 기준으로 앞뒤 100aa 추출
                    start = max(0, aa_pos - 100)
                    end = min(len(clean_protein), aa_pos + 101)
                    mutated_aa_seq = clean_protein[start:end]
                    
                    # 병원성 여부는 항상 1
                    pathogenicity = 1
                    
                    # TSV 파일 저장
                    out_f.write(f"{variant_id}\t{mutated_aa_seq}\t{hgvsc_position}\t{pathogenicity}\n")
                else:
                    print(f"Reference base mismatch at {transcript} corrected position {corrected_pos+1} for variant {variant_id}")

if __name__ == "__main__":
    # 사용법: python script.py fasta_file vcf_file output_file
    fasta_file = sys.argv[1] # 0.Cosmic_Gene.fasta
    vcf_file = sys.argv[2] # M2.final_filtering_divide_IDs.vcf
    output_file = sys.argv[3] #M3
    apply_mutations_and_save_aa_sequence(fasta_file, vcf_file, output_file)
