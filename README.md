# Miscellaneous UE4 Utilities

This repository contains a collection of assorted utilities for working with or understanding the internals of Unreal Engine 4. Note that these utilities are just small, ancillary tools. Please see the following repositories for my larger UE4-related tools and projects:

- [**adamrehn/ue4cli**](https://github.com/adamrehn/ue4cli) contains my automation-friendly, platform-agnostic command-line interface for UE4.
- [**adamrehn/conan-ue4cli**](https://github.com/adamrehn/conan-ue4cli) contains the ue4cli plugin that generates and builds packages for my [Conan-based third-party library integration workflow](https://adamrehn.com/articles/cross-platform-library-integration-in-unreal-engine-4) for UE4.
- [**adamrehn/ue4-docker**](https://github.com/adamrehn/ue4-docker) contains my Dockerfiles and build infrastructure for building Windows and Linux Docker containers for UE4.- [**adamrehn/UE4Capture**](https://github.com/adamrehn/UE4Capture) contains my plugin for performing in-Engine audio and video capture from inside NVIDIA Docker containers.

Each utility is contained in its own subdirectory. The utilities are:

- **modulefinder**: a Python script that allows you to query the UE4 source tree to find source files matching supplied patterns and determine which module contains any given source file. This is handy for discovering source files that contain functionality you are interested in and noting which module you need to link against to use them. Also useful for performing sanity checks to ensure that a source file is indeed being included in the intended module.

- **rename-module**: a Python script that non-destructively renames an Unreal Engine C++ source module, automating all of the necessary edits and file rename operations.

- **switchfinder**: a Python script that scans the UE4 source tree to discover all supported command-line switches. This is handy for discovering interesting or obscure switches.
