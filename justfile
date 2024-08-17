#!/usr/bin/env just --justfile

# Run pre-commit lint
lint:
    @pre-commit run --all-files
