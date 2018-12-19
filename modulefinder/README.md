# UE4 Module Finder

This Python script uses [ue4cli](https://github.com/adamrehn/ue4cli) to perform a gathering build of the `UE4Editor` target and then scans the generated files in the `Intermediate` directory to determine which source files are included in which modules. This is handy when you need to know which module to link against in order to use the types from a specific `.cpp` file.

- Python 3.5 or newer
- The [ue4cli](https://github.com/adamrehn/ue4cli) Python package
- ue4cli needs to be pointed to the root of the UE4 source tree using the [ue4 setroot](https://adamrehn.com/docs/ue4cli/configuration-commands/setroot) command. An Installed Build will not provide the required information.

To perform a search, simply specify the filenames of the source files you are interested in. For example, to determine which module contains the file `Engine/Source/Runtime/NullDrv/Private/NullDrv.cpp` you would run:

```
python3 modulefinder.py Engine/Source/Runtime/NullDrv/Private/NullDrv.cpp
```

You can specify as many filenames as you wish. Each filename can either be a full path like in the example above, or a string against which filenames will be matched. For example, if you wanted to find the modules for all of the source files with either "PhysX" or "OpenGL" in the filename, you would run:

```
python3 modulefinder.py PhysX OpenGL
```

You can also export a JSON file containing the full mapping dictionary from all modules to their source files for you to peruse at your leisure:

```
python3 modulefinder.py --all > mappings.json
```
