#!/bin/bash

rm -rf .docs_tmp
cp -r docs .docs_tmp

python docs_utils_pre_build/docs_release_notes.py
python docs_utils_pre_build/resolve_exemples.py
mkdocs build --config-file .docs_tmp/mkdocs.yml
mkdocs build --config-file docs_old/v0/mkdocs.yml

rm -rf .docs_tmp