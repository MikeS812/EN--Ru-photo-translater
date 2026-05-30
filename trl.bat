@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python console_translator.py -trl
