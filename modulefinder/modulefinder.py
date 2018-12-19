#!/usr/bin/env python3
import argparse, glob, json, os, platform, subprocess, sys

# Executes a command and captures its output
def capture(command):
	return subprocess.run(
		command,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		check=True
	)

# If no command-line arguments were supplied then display our usage syntax
if len(sys.argv) < 2:
	sys.argv.append('--help')

# Parse our command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--all', action='store_true', help='Print the list of source files for all modules in JSON format')
parser.add_argument('sourcefile', nargs='*', help='Source file(s) to retrieve the containing module for (can be a partial filename)')
args = parser.parse_args()

# Retrieve the UE4 root directory from ue4cli
output = capture(['ue4', 'root'])
rootDir = output.stdout.decode('utf-8').strip()
print('Using UE4 installation: {}'.format(rootDir), file=sys.stderr)

# Verify that the UE4 installation is not an Installed Build
sentinel = os.path.join(rootDir, 'Engine', 'Build', 'InstalledBuild.txt')
if os.path.exists(sentinel):
	print('Error:', file=sys.stderr)
	print('The detected UE4 installation is an Installed Build, which does not include source details.', file=sys.stderr)
	print('Please point ue4cli to a source tree and run this script again.', file=sys.stderr)
	sys.exit(1)

# Use ue4cli to interrogate UBT about bundled third-party libraries, triggering a gathering build
print('Performing a gathering build...', end='', file=sys.stderr)
capture(['ue4', 'libs']) 
print('done.', file=sys.stderr)

# Determine the path to the directory containing the unity build files for all Editor modules
unrealPlatform = {
	'Darwin': 'Mac',
	'Linux': 'Linux',
	'Windows': 'Win64'
}[platform.system()]
modulesDir = os.path.join(rootDir, 'Engine', 'Intermediate', 'Build', unrealPlatform, 'UE4Editor', 'Development')

# Maintain bi-directional mappings between modules and their source files
modulesToSources = {}
sourcesToModules = {}

# Iterate over the Editor modules
print('Populating source mappings...', end='', file=sys.stderr)
modules = glob.glob(os.path.join(modulesDir, '*'))
for module in modules:
	
	# Extract the module name and the list of unity build files
	moduleName = os.path.basename(module)
	unityFiles = glob.glob(os.path.join(module, 'Module.*.cpp'))
	modulesToSources[moduleName] = []
	
	# Iterate over each of the unity build files
	for unityFile in unityFiles:
		
		# Ignore files that deal exclusively with the generated output from UnrealHeaderTool
		if unityFile.endswith('.gen.cpp') == False:
			
			# Extract the list of includes from the file
			with open(unityFile, 'rb') as f:
				includes = f.read().decode('utf-8').replace('\r\n', '\n').split('\n')
				includes = [i for i in includes if i.startswith('#include "')]
				
				# Iterate over each include and extract the filename of the included source file
				for include in includes:
						filename = include.replace('#include "', '').replace('"', '')
						filename = filename.replace(os.path.join(rootDir, 'Engine'), 'Engine')
						filename = filename.replace('\\', '/')
						
						# Add the source file to our mappings
						modulesToSources[moduleName].append(filename)
						sourcesToModules[filename] = moduleName

# Progress output
print('done.\n', file=sys.stderr)

# If `--all` was specified, print our mappings from modules to source files
if args.all == True:
	print(json.dumps(modulesToSources, indent=4))
else:
	
	# Iterate over the specified source files
	for sourcefile in args.sourcefile:
		
		# Search our mappings for the specified filename
		sourcefile = sourcefile.replace('\\', '/')
		sources = [sourcefile] if sourcefile in sourcesToModules else [s for s in sourcesToModules if sourcefile in s]
		
		# Print the containing module for each matching filename
		if len(sources) == 0:
			print('No source files matching the string "{}".'.format(sourcefile))
		else:
			for source in sources:
				print('Source filename:   {}'.format(source))
				print('Containing module: {}'.format(sourcesToModules[source]))
				print()
