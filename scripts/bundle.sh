#! /bin/bash

# This script is used to bundle the application into a single file
poetry run pyinstaller --onefile --name="deletion-helper" deletion_helper/deletion_helper.py
