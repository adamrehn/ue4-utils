# UE4 Module Finder

This Python script uses [ue4cli](https://github.com/adamrehn/ue4cli) to perform a gathering build of the `UE4Editor` target and then scans the generated files in the `Intermediate` directory to determine which source files are included in which modules. This is handy when you want to discover `.cpp` files that you are interested in and determine which module to link against in order to use the types they define, or to verify that a given source file is indeed being included in the intended module and not being ignored by UBT as a result of failing to meet the module source file search criteria.

- Python 3.5 or newer
- The [ue4cli](https://github.com/adamrehn/ue4cli) Python package
- ue4cli needs to be pointed to the root of the UE4 source tree using the [ue4 setroot](https://adamrehn.com/docs/ue4cli/configuration-commands/setroot) command. An Installed Build will not provide the required information.

To perform a search, simply specify the patterns or full filenames of the source files you are interested in. (Patterns are just substrings that filenames are matched against, not regular expressions or glob patterns.) You can specify as many patterns and/or filenames as you wish.


## Example: sanity checking

To verify that the source file `Engine/Source/Runtime/NullDrv/Private/NullDrv.cpp` is being correctly detected and included in the `NullDrv` module, you would run:

```
python3 modulefinder.py Engine/Source/Runtime/NullDrv/Private/NullDrv.cpp
```

If the output lists the `NullDrv` module as containing the source file then you know that it is being included correctly.


## Example: discovering source files

If you wanted to find the modules for all of the source files with either "PhysX" or "OpenGL" in the filename, you would run:

```
python3 modulefinder.py PhysX OpenGL
```


## Example: listing all detected source files

You can also export a JSON file containing the full mapping dictionary from all modules to their source files for you to peruse at your leisure:

```
python3 modulefinder.py --all > mappings.json
```
