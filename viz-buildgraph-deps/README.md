# BuildGraph Dependency Visualiser

This Python script uses [Graphviz](https://graphviz.org/) to visualise dependency graphs produced by the Unreal Engine's [BuildGraph](https://dev.epicgames.com/documentation/en-us/unreal-engine/buildgraph-for-unreal-engine) scripting system. This can be handy when inspecting the steps that are involved in running automation workflows.

To export a JSON file with dependency information, use BuildGraph's `-Export` flag in combination with the `-ShowDeps` flag, like so:

```bash
# Exports JSON for the specified target and its dependencies
RunUAT[.bat|.sh] BuildGraph -Script=<SCRIPT.XML> -Target=<NODE> -Export=<FILE.JSON> -ShowDeps
```

The exported JSON file can then be visualised using this script:

```bash
python3 viz-buildgraph-deps.py <FILE.JSON> <OUT.SVG>
```

The script has the following requirements:

- Python 3.x
- The PyPI packages listed in `requirements.txt` (run `pip3 install -r requirements.txt` to install them)
