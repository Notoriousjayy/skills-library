#!/usr/bin/env python3
"""Convenience entry point: install this library (`pip install -e .`) before running."""

import sys

from security_skills.cli import main

if __name__ == "__main__":
    sys.exit(main(["normalize", *sys.argv[1:]]))
