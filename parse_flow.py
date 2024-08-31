import csv
import argparse
from collections import defaultdict

# Load the lookup table
def load_lookup_table(filename):
    lookup_table = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dstport = int(row['dstport'])
            protocol = row['protocol'].strip().lower()  # Convert protocol to lowercase to make the matching case-insensitive
            tag = row['tag'].strip().lower()  # Convert tag to lowercase to make the matching case-insensitive

            lookup_table[(dstport, protocol)] = tag
    return lookup_table

# Load the protocol number mappings
def load_protocol_numbers(filename):
    protocol_map = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            decimal = row['Decimal'].strip()
            protocol = row['Keyword'].strip().lower()
            protocol_map[decimal] = protocol
    return protocol_map

# Parse the flow log file
def parse_flow_log(filename, lookup_table, protocol_map):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    
    with open(filename, mode='r') as file:
        for line in file:
            parts = line.strip().split()
            dstport = int(parts[6])
            protocol_number = parts[7]
            protocol = protocol_map.get(protocol_number, 'unknown').lower()
            
            # Count port/protocol combinations
            port_protocol_counts[(dstport, protocol)] += 1
            
            # Map to a tag using the lookup table
            tag = lookup_table.get((dstport, protocol), 'untagged')  # Use lowercase 'untagged'
            tag_counts[tag] += 1
    
    return tag_counts, port_protocol_counts

# Write the tag counts to a file
def write_tag_counts(tag_counts, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tag', 'Count'])
        for tag, count in sorted(tag_counts.items()):
            writer.writerow([tag, count])

# Write the port/protocol combination counts to a file
def write_port_protocol_counts(port_protocol_counts, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Port', 'Protocol', 'Count'])
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            writer.writerow([port, protocol, count])

# Main function
def main(lookup_filename, flow_log_filename, tag_counts_filename, port_protocol_counts_filename):    
    # Load lookup table and protocol numbers
    lookup_table = load_lookup_table(lookup_filename)
    protocol_map = load_protocol_numbers('protocol-numbers.csv')  # Hardcoded filename
    
    # Parse flow log and get counts
    tag_counts, port_protocol_counts = parse_flow_log(flow_log_filename, lookup_table, protocol_map)
    
    # Write the results to output files
    write_tag_counts(tag_counts, tag_counts_filename)
    write_port_protocol_counts(port_protocol_counts, port_protocol_counts_filename)

# If this script is run from the command line, parse command-line arguments and call main()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process flow logs and lookup tables.')
    parser.add_argument('lookup_filename', help='The path to the lookup table CSV file.')
    parser.add_argument('flow_log_filename', help='The path to the flow log file.')
    parser.add_argument('tag_counts_filename', help='The path to the output file for tag counts.')
    parser.add_argument('port_protocol_counts_filename', help='The path to the output file for port/protocol counts.')
    
    args = parser.parse_args()
    main(args.lookup_filename, args.flow_log_filename, args.tag_counts_filename, args.port_protocol_counts_filename)
