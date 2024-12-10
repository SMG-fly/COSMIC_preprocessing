import pandas as pd
import sys

def filter_by_tier_1_with_header(census_file, filtering_file, output_file):
    # Step 1: Load CancerGeneCensus.tsv
    census_data = pd.read_csv(census_file, sep='\t')

    # Step 2: Extract COSMIC_GENE_ID for Tier 1
    tier_1_ids = census_data[census_data['TIER'] == 1]['COSMIC_GENE_ID']

    # Step 3: Load 3.filtering.tsv
    filtering_data = pd.read_csv(filtering_file, sep='\t')

    # Step 4: Filter rows in 3.filtering.tsv where COSMIC_GENE_ID is in Tier 1 list
    filtered_data = filtering_data[filtering_data['COSMIC_GENE_ID'].isin(tier_1_ids)]

    # Step 5: Save the filtered data to the output file with the header
    filtered_data.to_csv(output_file, sep='\t', index=False, header=True)
    print(f"Filtered data saved to {output_file}")

if __name__ == "__main__":
    # Ensure correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <CancerGeneCensus.tsv> <3.filtering.tsv> <output_file>")
        sys.exit(1)

    # Input and output file paths from command-line arguments
    census_file = sys.argv[1]
    filtering_file = sys.argv[2]
    output_file = sys.argv[3]

    # Run the filtering function
    filter_by_tier_1_with_header(census_file, filtering_file, output_file)
