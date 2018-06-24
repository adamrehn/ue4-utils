# UE4 Command-Line Switch Finder

This Python script uses the [ack](https://beyondgrep.com/) code search tool to scan the UE4 source tree and discover all supported command-line switches. The script generates a HTML file containing the list of unique switches and the source locations from which they are referenced, with hyperlinks to the relevant lines on GitHub. This is handy for discovering interesting or obscure switches.

Note that the script scans the entire source tree, which includes the code for **multiple tools**. Some of the switches will be supported by the Editor, others by UnrealFrontend, etc. Be sure to carefully read the path of the source files that reference a given switch to determine which tools support it.

The script has the following requirements:

- Python 3.x
- The `ack` and `git` commands must both be available in the system PATH
- The UE4 Git repository already needs to be cloned, the script does not perform this step

To run the script, simply point it to the root of the UE4 repo and specify an output filename:

```
python3 switchfinder.py OUTPUT.HTML /path/to/UnrealEngine
```

Usage notes:

- Specify a dash (`-`) as the filename to print the generated HTML to standard output instead of writing it to a file.
- If no UE4 root directory is specified, the script will use the current working directory.
