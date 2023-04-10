import sys
import csv

def match_eventsources_and_prefixes(csv_file):
    matched_sourceprefixes = set()
    unmatched_rows = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['eventsource prefix'] == row['Service Prefix']:
                matched_sourceprefixes.add(row['eventsource prefix'])
            else:
                unmatched_rows.append(row)

    matched_sourceprefixes = sorted(list(matched_sourceprefixes))

    with open('Compares/matched_sourceprefixes.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[prefix] for prefix in matched_sourceprefixes])

    unmatched_rows = sorted(unmatched_rows, key=lambda row: row['eventsource'])

    with open('Compares/unmatched_rows.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(unmatched_rows)


# Get the CSV filenames and the columns to compare from command line arguments
if len(sys.argv) != 5:
    print("Usage: python compare.py <csv1_filename> <csv2_filename> <csv1_col_index> <csv2_col_index>")
    sys.exit(1)
csv1_filename = sys.argv[1]
csv2_filename = sys.argv[2]
csv1_col_index = int(sys.argv[3])
csv2_col_index = int(sys.argv[4])

# Read in the first CSV and store it in a dictionary
csv1_dict = {}
with open(csv1_filename, newline='') as csv1_file:
    csv1_reader = csv.reader(csv1_file)
    header1 = next(csv1_reader)  # Skip header row and store it
    for row in csv1_reader:
        key = (row[csv1_col_index],)
        csv1_dict[key] = row

# Read in the second CSV and output matching rows from both CSVs
with open(csv2_filename, newline='') as csv2_file:
    csv2_reader = csv.reader(csv2_file)
    header2 = next(csv2_reader)  # Skip header row and store it
    with open('Compares/compared.csv', 'w', newline='') as compared_file:  # Open output file
        compared_writer = csv.writer(compared_file)
        compared_writer.writerow(header1 + header2)  # Write combined header row
        for row in csv2_reader:
            key = (row[csv2_col_index],)
            if key in csv1_dict:
                # Write combined row to output file
                combined_row = csv1_dict[key] + row
                compared_writer.writerow(combined_row)

# read the data from the CSV file into a list of dictionaries
with open('Compares/compared.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]

# add a new key to each dictionary with the first part of the eventsource
for row in data:
    row['eventsource prefix'] = row['eventsource'].split('.')[0]

# write the modified rows back to the file
with open('Compares/compared.csv', 'w', newline='') as f:
    fieldnames = reader.fieldnames + ['eventsource prefix']
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    writer.writerows(data)

match_eventsources_and_prefixes("Compares/compared.csv")


# # read the data from the CSV file into a list of dictionaries
# with open('Compares/compared.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     data = [row for row in reader]

# # add a new key to each dictionary with the first part of the eventsource
# for row in data:
#     row['eventsource prefix'] = row['eventsource'].split('.')[0]

# # filter the data to filter by the rows that match or don't match
# matched_prefix_eventsource = [row for row in data if row['eventsource prefix'] == row['Service Prefix']]
# unmatched_prefix_eventsource = [row for row in data if row['eventsource prefix'] != row['Service Prefix']]


# # write the filtered data to a new CSV file
# with open('Compares/matched_prefix_eventsource.csv', 'w', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=matched_prefix_eventsource[0].keys())
#     writer.writeheader()
#     writer.writerows(matched_prefix_eventsource)

# # write the filtered data to a new CSV file
# with open('Compares/unmatched_prefix_eventsource.csv', 'w', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=unmatched_prefix_eventsource[0].keys())
#     writer.writeheader()
#     writer.writerows(unmatched_prefix_eventsource)

# # read the data from the CSV file into a list of dictionaries
# with open('Compares/matched_prefix_eventsource.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     data = [row for row in reader]

# # add a new key to each dictionary with the first part of the eventsource
# for row in data:
#     row['eventsource prefix'] = row['eventsource'].split('.')[0]

# # get the unique values from the eventsource and source prefix columns
# eventsources = list(set(row['eventsource'] for row in data))
# source_prefixes = list(set(row['Service Prefix'] for row in data))

# # write the unique eventsource values to a new CSV file
# with open('Compares/unique_eventsources_matched.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['eventsource'])
#     writer.writerows([[eventsource] for eventsource in eventsources])

# # write the unique source prefix values to a new CSV file
# with open('Compares/unique_source_prefixes_matched.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Service Prefix'])
#     writer.writerows([[prefix] for prefix in source_prefixes])

# # read the data from the CSV file into a list of dictionaries
# with open('Compares/unmatched_prefix_eventsource.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     data = [row for row in reader]

# # add a new key to each dictionary with the first part of the eventsource
# for row in data:
#     row['eventsource prefix'] = row['eventsource'].split('.')[0]

# # get the unique values from the eventsource and source prefix columns
# eventsources = list(set(row['eventsource'] for row in data))
# source_prefixes = list(set(row['Service Prefix'] for row in data))

# # write the unique eventsource values to a new CSV file
# with open('Compares/unique_eventsources_unmatched.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['eventsource'])
#     writer.writerows([[eventsource] for eventsource in eventsources])

# # write the unique source prefix values to a new CSV file
# with open('Compares/unique_source_prefixes_unmatched.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Service Prefix'])
#     writer.writerows([[prefix] for prefix in source_prefixes])