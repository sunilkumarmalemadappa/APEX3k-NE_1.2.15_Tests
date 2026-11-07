import re
import sys

# Read the file
filepath = r'C:\Users\smalemadappa\.copilot\repos\copilot-worktrees\APEX3k-NE_1.2.15_Tests\sunilkumarmalemadappa-fantastic-broccoli\MEDIACIPHER_SIMULCRYPT_TESTS.md'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Check current structure
lines = content.split('\n')

# Find all test case patterns
test_case_pattern = r'^### Test Case (\d+\.\d+):'
requirement_pattern = r'^## REQUIREMENT REL(\d+\.\d+\.\d+-\d+):'

test_cases_found = []
requirements_found = []

for i, line in enumerate(lines):
    tc_match = re.match(test_case_pattern, line)
    if tc_match:
        test_cases_found.append((i, line, tc_match.group(1)))
    
    req_match = re.match(requirement_pattern, line)
    if req_match:
        requirements_found.append((i, line, req_match.group(1)))

print(f"Total lines: {len(lines)}")
print(f"\nRequirements found: {len(requirements_found)}")
for line_num, line_text, req_id in requirements_found[:3]:
    print(f"  Line {line_num}: {line_text[:80]}")

print(f"\nTest cases found: {len(test_cases_found)}")
print("First 10 test cases:")
for line_num, line_text, tc_id in test_cases_found[:10]:
    print(f"  Line {line_num}: {line_text[:80]}")
