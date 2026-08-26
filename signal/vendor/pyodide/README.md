# Self-hosted Pyodide runtime

This directory contains the minimal browser runtime required by the image
compression demonstration:

- Pyodide 314.0.5 core runtime and Python standard library
- NumPy 2.4.6 WebAssembly wheel
- the matching Pyodide package lock file

The files are pinned and served from `/signal/vendor/pyodide/`; the deployed
demonstration does not load code from a third-party CDN. Pyodide is licensed
under MPL-2.0. The NumPy wheel retains NumPy's bundled license metadata.

Upstream: https://github.com/pyodide/pyodide
