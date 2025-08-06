#!/usr/bin/env python3
import argparse, json, networkx, sys


# Exits with an error if the specified JSON validation condition is not satisfied
def validate(condition):
	if not condition:
		print('Error: input JSON file is malformed!', file=sys.stderr)
		sys.exit(1)


# Our supported command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('infile', help='Input JSON file to be parsed')
parser.add_argument('outfile', help='Output filename for generated SVG')
parser.add_argument(
	'--layout',
	default='dot',
	choices=['dot', 'neato', 'fdp', 'sfdp', 'circo', 'twopi'],
	help='Graphviz layout engine to use'
)

# If no command-line arguments were supplied, display the help message and exit
if len(sys.argv) < 3:
	parser.print_help()
	sys.exit(0)

# Parse the supplied command-line arguments
args, run_args = parser.parse_known_args()

# Attempt to parse the specified JSON file
print(f'Parsing "{ args.infile }"...', file=sys.stderr)
data = None
with open(args.infile, 'rb') as f:
	data = json.load(f)

# Verify that the JSON data is valid output from BuildGraph
validate('Groups' in data)
for group in data['Groups']:
	validate('Nodes' in group)
	for node in group['Nodes']:
		validate('Name' in node)
		validate('DependsOn' in node)

# Build the dependency graph for the BuildGraph nodes
graph = networkx.DiGraph()
for group in data['Groups']:
	for node in group['Nodes']:
		graph.add_node(node['Name'])
		
		# Split out the semicolon-delimited list of dependencies for the node
		if len(node['DependsOn']) > 0:
			dependencies = node['DependsOn'].split(';')
			for dependency in dependencies:
				graph.add_edge(node['Name'], dependency)

# Generate an SVG representation of the graph
print(f'Generating SVG file "{ args.outfile }"...', file=sys.stderr)
dot = networkx.drawing.nx_pydot.to_pydot(graph)
dot.write_svg(args.outfile, prog=args.layout)
