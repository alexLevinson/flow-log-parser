import os
import filecmp
import shutil

import parse_flow

def run_test(testcase_name, testcase_dir, output_dir, expected_dir):
    # Define file paths for the test case
    flow_log_file = os.path.join(testcase_dir, f"{testcase_name}_flow_log.txt")
    lookup_table_file = os.path.join(testcase_dir, f"{testcase_name}_lookup_table.csv")
    
    # Define output file paths
    generated_tag_counts_file = os.path.join(output_dir, f"{testcase_name}_tag_counts.csv")
    generated_port_protocol_counts_file = os.path.join(output_dir, f"{testcase_name}_port_protocol_counts.csv")
    
    # Define expected output file paths
    expected_tag_counts_file = os.path.join(expected_dir, f"{testcase_name}_tag_counts.csv")
    expected_port_protocol_counts_file = os.path.join(expected_dir, f"{testcase_name}_port_protocol_counts.csv")
    
    # Set up file paths for main script
    lookup_filename = lookup_table_file
    flow_log_filename = flow_log_file
    tag_counts_filename = generated_tag_counts_file
    port_protocol_counts_filename = generated_port_protocol_counts_file
    
    # Run the main script
    parse_flow.main(lookup_filename, flow_log_filename, tag_counts_filename, port_protocol_counts_filename)
    
    # Compare generated files with expected files
    tag_counts_match = filecmp.cmp(generated_tag_counts_file, expected_tag_counts_file, shallow=False)
    port_protocol_counts_match = filecmp.cmp(generated_port_protocol_counts_file, expected_port_protocol_counts_file, shallow=False)
    
    return tag_counts_match, port_protocol_counts_match

def run_all_tests(testcase_dir, expected_dir, output_dir):
    # Get all test case names
    testcase_names = set()
    for filename in os.listdir(testcase_dir):
        if filename.endswith("_flow_log.txt"):
            testcase_name = filename.replace("_flow_log.txt", "")
            testcase_names.add(testcase_name)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Run all tests
    all_tests_passed = True
    for testcase_name in sorted(testcase_names):
        print(f"Running test case: {testcase_name}")
        
        tag_counts_match, port_protocol_counts_match = run_test(
            testcase_name, testcase_dir, output_dir, expected_dir
        )
        
        if tag_counts_match and port_protocol_counts_match:
            print(f"Test case '{testcase_name}' passed.")
        else:
            print(f"Test case '{testcase_name}' failed.")
            all_tests_passed = False
    
    if all_tests_passed:
        print("All test cases passed.")
    else:
        print("Some test cases failed.")

if __name__ == "__main__":
    testcase_dir = "testcases"
    expected_dir = "expected"
    output_dir = "generated"
    
    # Clear previous generated outputs
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Run all tests
    run_all_tests(testcase_dir, expected_dir, output_dir)
