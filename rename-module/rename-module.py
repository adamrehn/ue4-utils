#!/usr/bin/env python3
import glob, os, re, shutil, sys
from os.path import abspath, basename, dirname, join


# Reads data from a file
def readFile(filename):
	with open(filename, 'rb') as f:
		return f.read().decode('utf-8')

# Writes data to a file
def writeFile(filename, data):
	with open(filename, 'wb') as f:
		f.write(data.encode('utf-8'))

# Applies the supplied list of replacements to one or more files
def patchFiles(filenames, replacements):
	for filename in filenames:
		patched = readFile(filename)
		for key in replacements:
			patched = re.sub(key, replacements[key], patched)
		writeFile(filename, patched)


# Check that the required arguments have been supplied
if len(sys.argv) < 3:
	print('Usage:')
	print('rename-module.py MODULE_PATH NEW_NAME')
	print('MODULE_PATH is the path to the original code module.')
	print('NEW_NAME is the new name for the code module.')
	sys.exit(0)

# Parse our arguments, resolving the absolute path to the input code module
sourceDir = dirname(abspath(sys.argv[1]))
oldName = basename(sys.argv[1])
newName = sys.argv[2]

# Duplicate the module directory
oldDir = join(sourceDir, oldName)
newDir = join(sourceDir, newName)
shutil.copytree(oldDir, newDir)

# Rename the module's rules file (.Build.cs)
rulesFile = shutil.move(
	join(newDir, '{}.Build.cs'.format(oldName)),
	join(newDir, '{}.Build.cs'.format(newName))
)

# Update the module name in the rules file
patchFiles([rulesFile], {
	'public class {}'.format(oldName): 'public class {}'.format(newName),
	'public {}\\('.format(oldName): 'public {}('.format(newName),
})

# Update any MODULENAME_API macros in the module's header files
headerFiles = glob.glob(join(newDir, '**', '*.h'), recursive=True)
oldMacro = '{}_API'.format(oldName.upper())
newMacro = '{}_API'.format(newName.upper())
patchFiles(headerFiles, {oldMacro: newMacro})

# Update the IMPLEMENT_MODULE() macro in the source file for the module interface class
sourceFiles = glob.glob(join(newDir, '**', '*.cpp'), recursive=True)
patchFiles(sourceFiles, {
	'IMPLEMENT_MODULE\\((.+), {}\\)'.format(oldName): 'IMPLEMENT_MODULE(\\1, {})'.format(newName)
})
