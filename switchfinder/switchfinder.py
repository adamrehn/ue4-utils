#!/usr/bin/env python3
import os, re, subprocess, sys

# Check that the required arguments have been supplied
if len(sys.argv) < 2:
	print('Usage:')
	print('switchfinder.py OUTFILE [ROOTDIR]')
	print('OUTFILE is the ouput HTML file (use `-` for stdout.)')
	print('ROOTDIR is the root of the UE4 Git repo (defaults to cwd.)')
	sys.exit(0)

# If a root git repo directory was specified, use it
rootDir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

# Use git to determine which branch is checked out
branchName = subprocess.check_output(
	['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
	universal_newlines=True,
	cwd=rootDir
).strip()

# Use ack to find each command line switch supported by UE4
ack = subprocess.Popen(
	['ack', '-o', 'FCommandLine::Get\\(\\), TEXT\\(.+?\\)'],
	stdout=subprocess.PIPE,
	universal_newlines=True,
	cwd=rootDir
)

# Pre-compile our switch extraction regex
switchRegex = re.compile('TEXT\\("(.+?)"\\)')
switchIndices = {}

# Extract the source location details for each switch
print('Finding switches (this will take a while)...', file=sys.stderr)
for line in ack.stdout:
	components = line.split(':', 2)
	if len(components) == 3:
		match = switchRegex.search(components[2])
		if match != None:
			
			# Extract the details of the match
			file = components[0]
			line = components[1]
			switch = match.group(1)
			
			# If this is the first time this switch has been encountered, add it to our list
			if switch not in switchIndices:
				switchIndices[switch] = []
			
			# Add the source location details to our mapping structure
			switchIndices[switch].append({'file': file, 'line': line})

# Our HTML template code
BASEURL = 'https://github.com/EpicGames/UnrealEngine/blob/{}/'.format(branchName)
HTML_HEADER = '''<!doctype html><html><head><title>UE4 Command-Line Switches</title></head><body><h1>UE4 Command-Line Switches</h1><ul>'''
HTML_TEMPLATE = '''<li><strong>$$_SWITCH_$$</strong><ul>$$_LOCATIONS_$$</ul></li>'''
HTML_FOOTER = '''</ul></body></html>'''

# Generate our HTML output for the discovered switches
markup = HTML_HEADER
for switch in sorted(switchIndices.keys()):
	locations = list(['<li><a href="{}" target="_blank">{}:{}</a></li>'.format(
		'{}{}#L{}'.format(BASEURL, loc['file'], loc['line']),
		loc['file'],
		loc['line']
	) for loc in switchIndices[switch]])
	markup += HTML_TEMPLATE.replace('$$_SWITCH_$$', switch).replace('$$_LOCATIONS_$$', ''.join(locations))
markup += HTML_FOOTER

# Write the generated HTML to the specified output file (or stdout if requested)
filename = sys.argv[1]
if filename == '-':
	print(markup)
else:
	with open(filename, 'w') as outfile:
		outfile.write(markup)
		print('Done.')
