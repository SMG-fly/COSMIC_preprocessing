import sys

filename = sys.argv[1] 

def filter_snv(filename):
    with open(filename, 'r') as file:
        for line in file:
            # Skip lines starting with ##
            if line.startswith("##"):
                continue
            # Split columns by tab
            columns = line.strip().split('\t')
            # Check if 8th column contains SO_TERM=SNV
            if len(columns) >= 8 and "SO_TERM=SNV" in columns[7]:
                print(line.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filter_snv(sys.argv[1])