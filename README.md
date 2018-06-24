# Miscellaneous UE4 Utilities

This repository contains a collection of assorted utilities for working with or understanding the internals of Unreal Engine 4. Note that these utilities are just small, ancillary tools. Please see the following repositories for my larger UE4-related tools and projects:

- [**adamrehn/ue4cli**](https://github.com/adamrehn/ue4cli) contains my automation-friendly, platform-agnostic command-line interface for UE4.
- [**adamrehn/conan-ue4cli**](https://github.com/adamrehn/conan-ue4cli) contains the scripts and packages for my [Conan-based third-party library integration workflow](https://adamrehn.com/articles/cross-platform-library-integration-in-unreal-engine-4) for UE4.
- [**adamrehn/ue4-docker**](https://github.com/adamrehn/ue4-docker) contains my scripts and Dockerfiles for building Windows and Linux Docker containers for UE4.

Each utility is contained in its own subdirectory. The utilities are:

- **switchfinder**: a Python script that scans the UE4 source tree to discover all supported command-line switches. This is handy for discovering interesting or obscure switches.
