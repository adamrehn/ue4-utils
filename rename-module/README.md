# UE4 Module Renamer

This Python script renames an Unreal Engine C++ source module, automating all of the necessary edits and file rename operations. The module is duplicated without modifying the original, so the process is non-destructive.

The script has the following requirements:

- Python 3.5 or newer

To run the script, simply point it to the path of a source module and specify the new module name:

```bash
# Renames OldModule to NewModule using the absolute path to the module
python3 rename-module.py "/path/to/project/or/plugin/Source/OldModule" NewModule

# Alternatively, run the command from the Source directory and use a relative path
cd "/path/to/project/or/plugin/Source"
python3 /path/to/rename-module.py OldModule NewModule
```

Limitations to note:

- This script is designed to be used with pure C++ code modules. Modules that contain Blueprints may not function correctly after being renamed.
- Name redirects are not generated to map from the old module name to the new module name.
- The module list in the descriptor JSON file for the project or plugin containing the source module is not updated to reflect the new module name.
- The dependency lists of other modules which depend on the module are not updated to reflect the new module name.
