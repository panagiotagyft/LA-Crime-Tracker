import csv
#Utility script to extract a subset of lines from a CSV file
input_file = 'Crime_Data_from_2020_to_Present_20241112.csv'
output_file = 'Crime_Data_from_2020_to_Present_20241112_10k.csv'

lines_to_keep = 10000   #! Modify this to keep more lines

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for i, row in enumerate(reader):
        if i >= lines_to_keep:
            break
        writer.writerow(row)

print(f"First {lines_to_keep} lines written to {output_file}")
