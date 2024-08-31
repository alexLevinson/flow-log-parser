EXECUTING THE CODE
To run the project, call the "main" fucntion of parse_flow.py, with the I/O filenames as parameters

ASSUMPTIONS
1. The provided testctase/output example is incorrect, or incomplete. Despite having only 14 rows of input, the example output counts 16 total tag assignments.
2. We record a port/protocol combo in port_protocol_counts.csv regardless of whether that combo matches to a tag
3. It was unclear if "the matches should be case insensitive" referred to the protocols (e.g. "TCP" and "tcp" should be understood as the same protocol) or the tags (e.g. "email" and "Email" should be understood as the same tag). I implemented case-insensitivity for both
4. Although multiple tags can mape to the same port/protocol combo, no port/protocol combo can map to multiple tags
5. The mapping of protocol ids to protocols can be found here https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml, which I imported as "protocol_numbers.csv"
6. The program only supports the default log format provided in the example. It does not handle custom log formats or versions other than version 2.=
7. The program does not include logging or extensive error handling. It assumes that input files are well-formed and accessible, and it will terminate with an error if issues arise during file operations or data processing

TESTING
Testing is done by calling test.py. test.py takes in a directory of testcases and a directory of expected outputs. The testcases directory should have 2 files for each testcase, <tcase_name>_flow_log.txt and <tcase_name>_lookup_table.csv. The expected directory should have 2 files for each testcase, <tcase_name>tag_counts.csv and <tcase_name>_port_protocol_counts.csv.
test.py then calls parse_flow.py to generate actual output for each testcase, and compares the actual and expected outputs.

We have 5 added testcases, each of which tests a specific property of the code:
case1 - Example Given in Instructions
case2 - Case Insensitivity
case3 - Empty Lookup Table
case4 - Unusual Protocol (ICMP)
case5 - Repeated Entries in Flow Log