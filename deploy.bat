@echo off
python -m nuitka --onefile --follow-imports --company-name="Team IRIS" --product-name="MiniDL HashGen" --file-version=0.1 --product-version=454.66 --copyright="Team IRIS" --file-description="Hash Generator for MiniDL" --remove-output --show-progress HashGenerator.py"