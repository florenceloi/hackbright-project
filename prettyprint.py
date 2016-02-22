from sys import argv
from pprint import pprint
import json

# Read JSON string from filename given on command-line
f = open(argv[1])
json_string0 = f.readline()

# Turn into Python dictionary
json_dict = json.loads(json_string0)

# "Pretty print" it
pprint(json_dict)