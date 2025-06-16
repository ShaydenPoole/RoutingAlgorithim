import csv

# Function to standardize address by simply stripping spaces and converting to lowercase.
def minimal_standardize_location_name(location):
    return location.strip().lower()

# Function to load the distance table and map locations to their respective indices using the Address column.
def load_distance_table_with_address_matching(file_path):
    location_to_index = {}
    distance_table = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row
        cleaned_headers = [minimal_standardize_location_name(header) for header in headers[2:]]  # Skip 'Location' and 'Address' columns
        for i, row in enumerate(reader):
            cleaned_row_header = minimal_standardize_location_name(row[1])  # Use the 'Address' column for matching
            location_to_index[cleaned_row_header] = i
            distance_table.append([cell.strip() for cell in row[2:]])  # Skip 'Location' and 'Address' columns
    return location_to_index, distance_table, cleaned_headers

# Load the file and process the distance table
location_to_index, distance_table, cleaned_headers = load_distance_table_with_address_matching('WGUPS_Distance_Table_Cleaned.csv')

# Function to output all distances from each location.
def output_all_distances():
    for location, index in location_to_index.items():
        print(f"Distances from {location}:")
        for i, target_location in enumerate(cleaned_headers):
            print(f"  To {target_location}: {distance_table[index][i]} miles")
        print("\n")

# Output all distances
output_all_distances()
