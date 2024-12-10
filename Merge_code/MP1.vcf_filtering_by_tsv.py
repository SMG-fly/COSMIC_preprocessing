import pandas as pd
import sys

def filter_vcf_by_genomic_mutation_id(tsv_file, vcf_file, output_vcf):
    """
    Filters a VCF file to include only the lines that match GENOMIC_MUTATION_IDs in a TSV file.

    Args:
        tsv_file (str): Path to the TSV file containing the GENOMIC_MUTATION_ID column.
        vcf_file (str): Path to the input VCF file.
        output_vcf (str): Path to the output filtered VCF file.
    """
    # Step 1: Load the GENOMIC_MUTATION_IDs from the TSV file
    tsv_data = pd.read_csv(tsv_file, sep='\t')
    genomic_mutation_ids = set(tsv_data['GENOMIC_MUTATION_ID'])

    # Step 2: Open the VCF file and filter lines
    with open(vcf_file, 'r') as infile, open(output_vcf, 'w') as outfile:
        for line in infile:
            # Write headers as-is
            if line.startswith("#"):
                outfile.write(line)
                continue
            
            # Process VCF data lines
            cols = line.strip().split("\t")
            info_field = cols[2]  # GENOMIC_MUTATION_ID is typically in the third column (ID field in VCF)
            
            # Check if the GENOMIC_MUTATION_ID matches
            if info_field in genomic_mutation_ids:
                outfile.write(line)

    print(f"Filtered VCF saved to {output_vcf}")

if __name__ == "__main__":
    # Ensure correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python filter_vcf_by_genomic_mutation_id.py <tsv_file> <vcf_file> <output_vcf>")
        sys.exit(1)

    # Input and output file paths
    tsv_file = sys.argv[1] # T4.filtering4.tsv
    vcf_file = sys.argv[2] # V2.CDS_mut_target.vcf
    output_vcf = sys.argv[3]

    # Run the filtering function
    filter_vcf_by_genomic_mutation_id(tsv_file, vcf_file, output_vcf)
